"""This script uses Eurpoe PMC API to retrieve publications of interest"""

import json
import requests

# Method to build url that will be used to make the API request
def build_pmc_query_url(query_string, result_type="core", page_size=100, return_format="json"):
    pmc_api_base = "https://www.ebi.ac.uk/europepmc/webservices/rest/search?"
    query_url = pmc_api_base + "query={}".format(query_string)
    query_url += "&resultType={}".format(result_type)
    query_url += "&pageSize={}".format(page_size)
    query_url += "&format={}".format(return_format)
    return query_url

# A generator that makes the API call and yields the publication
def pmc_get_publications(query_url):
    response = requests.get(query_url)
    response_dict = response.json()
    for result in response_dict['resultList']['result']:
        yield [result.get("id"), result.get("source"), result.get("title"), result.get("hasData")]
    if 'nextPageUrl' in response_dict.keys():
        yield from pmc_get_publications(response_dict['nextPageUrl'])

# Truncate long title to fit in the table
def fit_title(title):
    if len(title) > 120:
        title = title[:117] + "..."
    return title

def pprint(dobj):
    print(json.dumps(dobj, indent=4))

main_query_string = '("SARS-CoV-2" OR "COVID-19" OR "Covid-19") AND AFF:"Sweden" AND CREATION_DATE:[2022-08-01 TO 2022-08-31]'
#main_query_string = '("SARS-CoV-2" OR "COVID-19" OR "Covid-19") AND AFF:"Sweden" AND PUB_YEAR:2022'
article_web_base = 'https://europepmc.org/article'
words_of_interest = {'Figshare' : 'figshare*', 'Zenodo' : 'zenodo*', 'Github' : 'github*', 'Dryad': 'dryad',
                     'Gene Expression Omnibus' : 'gse*', 'Protein Data Bank' : 'PDB*', 'Proteome Xchange' : '(PXD* OR ProteomeXchange)',
                     'SASBDB' : 'SASD*', 'Electron Microscopy DB' : '(EMD AND NOT serono)', 'ENA' : '(PRJE* OR PRJD* OR PRJN*)',
                     'Open Science Framework' : '("Open Science Framework" OR osf*)', 'Experimental Factor Ontology' : 'EFO'}
#words_of_interest = {'Figshare' : 'figshare', 'Zenodo' : 'zenodo', 'Github' : 'github'}
pub_collection = {}
pub_summary = {'total': 0, 'data_y': 0, 'data_n': 0, 'db_total': 0}

# collect publication with primary query, not needed, but kept here for reference/debug etc
# qurl = build_pmc_query_url(query_string="{} AND HAS_DATA:y".format(main_query_string))
# for pub in pmc_get_publications(qurl):
#     if pub[0] in pub_collection:
#         continue
#     pub_collection[pub[0]] = ((article_web_base + '/' + pub[1] + '/' + pub[0]), pub[2], pub[3], [])
#     pub_summary['total'] += 1
#     pub_summary['data_' + pub[3].lower()] += 1
# print("Done collecting all Publications")

# query again with words of interest and populate it in publications info
for db, search_word in words_of_interest.items():
    wqurl = build_pmc_query_url(query_string="{} AND {}".format(main_query_string, search_word))
    for pub in pmc_get_publications(wqurl):
        if pub[0] not in pub_collection:
            #print("Strange!! Article '{}' has word of interest '{}' but not in main search".format((article_web_base + '/' + pub[1] + '/' + pub[0]), db))
            pub_collection[pub[0]] = ((article_web_base + '/' + pub[1] + '/' + pub[0]), pub[2], pub[3], [])
            pub_summary['total'] += 1
            pub_summary['data_' + pub[3].lower()] += 1
        pub_collection[pub[0]][-1].append(db)
    print("Done checking for DB {}".format(db))

# write the output file
with open("publication_list.html", "w") as outfile:
    outfile.write(
    """
        <!DOCTYPE html>
        <html>
        <head>
            <base target='_blank'>
            <script src='https://www.kryogenix.org/code/browser/sorttable/sorttable.js'></script>
            <style>
                body {{
                    font-family: 'Helvetica Neue', Helvetica, Arial, Verdana, sans-serif;
                    max-width: 1200px;
                    padding: 20px;
                    margin:0 auto;
                    font-size:10pt;
                    color: #333;
                }}
    
                table {{
                    width:100%;
                    border:1px solid #D9D9D9;
                    border-spacing: 0;
                    border-collapse: collapse;
                  }}
    
                table th, table td {{
                    border:0.8px solid #D9D9D9;
                    padding:8px;
                  }}
    
                table th {{
                    background-color: #EAECEE;
                    cursor: pointer;
                    position: sticky;
                    top: 0;
                  }}
                
                table tr:hover {{
                      background-color: #F8F9F9;
                  }}
                    
                a {{
                    color: #2874A6;
                    text-decoration: none;
                }}
    
                li {{
                    float: left;
                    margin: 0px 60px;
                }}
    
                #TableContainer {{
                    max-height: 1500px;
                    overflow: auto;
                }}
            </style>
        </head>
        <body>
        <ul style="padding-left:160px;">
            <li>Total publications: {}</li>
            <li>Publications with Data 'Y': {}</li>
            <li>Publications with Data 'N': {}</li>
        </ul><br><br>
        <div id='TableContainer'>
        <table class='sortable'>
        <tr><th>Read</th><th>Title</th><th>Has Data</th><th>Mentioned DB of interest</th></tr>
    """.format(pub_summary['total'], pub_summary['data_y'], pub_summary['data_n'])
    )
    for pid, pub_info in pub_collection.items():
        outfile.write(
        """
            <tr id='{}'>
                <td><input type='checkbox' id='{}'></td>
                <td><a href='{}'>{}</a></td>
                <td>{}</td>
                <td>{}</td>
            </tr>
        """.format(pid, pid, pub_info[0], fit_title(pub_info[1]), pub_info[2], ", ".join(pub_info[3]))
        )
    outfile.write(
    """
        </table>
        </div>
        <script>
            // Cookies saving and retrieving functions taken from internet
    
            function createCookie(name, value, days) {
                var expires;
                if (days) {
                    var date = new Date();
                    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
                    expires = '; expires=' + date.toGMTString();
                }
                else {
                    expires = '';
                }
                document.cookie = name + '=' + value + expires;
            }

            function getCookie(c_name) {
                if (document.cookie.length > 0) {
                    c_start = document.cookie.indexOf(c_name + '=');
                    if (c_start != -1) {
                        c_start = c_start + c_name.length + 1;
                        c_end = document.cookie.indexOf(';', c_start);
                        if (c_end == -1) {
                            c_end = document.cookie.length;
                        }
                        return unescape(document.cookie.substring(c_start, c_end));
                    }
                }
                return '';
            }
        </script>
        </body>
        </html>
    """
    )    
