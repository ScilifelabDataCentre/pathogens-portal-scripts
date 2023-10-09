"""This script uses Eurpoe PMC API to retrieve publications of interest to update in publication DB"""

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
        yield [result.get("id"), result.get("source"), result.get("title"), result.get("hasData"), result.get("doi")]
    if 'nextPageUrl' in response_dict.keys():
        yield from pmc_get_publications(response_dict['nextPageUrl'])

# Truncate long title to fit in the table
def fit_title(title):
    if len(title) > 150:
        title = title[:147] + "..."
    return title

def pprint(dobj):
    print(json.dumps(dobj, indent=4))

main_query_string = '(ABSTRACT:"SARS-CoV-2" OR ABSTRACT:"COVID-19" OR ABSTRACT:"Covid-19") AND AFF:"Sweden" AND CREATION_DATE:[2023-09-01 TO 2023-09-30]'
#main_query_string = '("SARS-CoV-2" OR "COVID-19" OR "Covid-19") AND AFF:"Sweden" AND PUB_YEAR:2022'

article_web_base = 'https://europepmc.org/article'

pub_collection = {}
pub_summary = {'total': 0, 'data_y': 0, 'data_n': 0, 'db_total': 0}


# query again with words of interest and populate it in publications info
wqurl = build_pmc_query_url(query_string=main_query_string)
for pub in pmc_get_publications(wqurl):
    if pub[0] not in pub_collection:
        pub_collection[pub[0]] = ((article_web_base + '/' + pub[1] + '/' + pub[0]), pub[2], pub[3], pub[4])
        pub_summary['total'] += 1
        pub_summary['data_' + pub[3].lower()] += 1

# write the output file
with open("all_publication_list.html", "w") as outfile:
    outfile.write(
    """
        <!DOCTYPE html>
        <html>
        <head>
            <base target='_blank'>
            <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css' rel='stylesheet' 
                  integrity='sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65' crossorigin='anonymous'>
            <script src='https://code.jquery.com/jquery-3.6.3.js' integrity='sha256-nQLuAZGRRcILA+6dMBOvcRh5Pe310sBpanc6+QBmyVM=' crossorigin='anonymous'></script>
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
                    padding:8px 10px;
                  }}
    
                table th {{
                    background-color: #EAECEE;
                    cursor: pointer;
                    position: sticky;
                    top: 0;
                  }}
                
                table tr > td:not(:first-child) {{
                      text-align: center;
                  }}
                
                table tr:hover {{
                      background-color: #F8F9F9;
                  }}
                    
                a {{
                    color: #2874A6;
                    text-decoration: none;
                }}
    
                #TableContainer {{
                    max-height: 1500px;
                    overflow: auto;
                }}
                
                div#doiModal ul {{
                  list-style-type: none;
                }}
                
                .stat {{
                  padding: 6px;
                }}
                
                .btn-doi {{
                  color: #fff;
                  background-color: #4c979f;
                  font-size: 0.9em;
                }}

                .btn-doi:hover {{
                  color: #3f3f3f;
                  background-color: #4c979f;
                }}
                
                svg:hover {{
                  cursor: pointer;
                  background-color: #e5e5e5;
                  box-shadow: #a6a6a6 0px 0px 10px;
                }}
            </style>
        </head>
        <body>
        <div class='d-flex justify-content-between mb-4'>
            <div class='stat'>Total publications: {}</div>
            <div class='stat'>Publications with Data 'Y': {}</div>
            <div class='stat'>Publications with Data 'N': {}</div>
            <div>
              <button id='seeDOI' type='button' class='btn btn-doi' data-bs-toggle='modal' data-bs-target='#doiModal'>
                Selected DOIs
              </button>
            </div>
            <div class='modal fade' id='doiModal' tabindex='-1' aria-labelledby='doiModalLabel' aria-hidden='true'>
                <div class='modal-dialog'>
                  <div class='modal-content'>
                    <div class='modal-header'>
                      <h5 class='modal-title pe-2' id='doiModalLabel'>Selected DOIs</h5>
                      <svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' fill='currentColor' class='bi bi-copy' viewBox='0 0 16 16'>
                        <path fill-rule='evenodd' d='M4 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V2Zm2-1a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H6ZM2 5a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1v-1h1v1a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h1v1H2Z'/>
                      </svg>
                      <button type='button' class='btn-close' data-bs-dismiss='modal' aria-label='Close'></button>
                    </div>
                    <div class='modal-body'>
                    </div>
                  </div>
                </div>
            </div>
        </div>
        <div id='TableContainer'>
        <table class='sortable'>
        <tr><th>Title</th><th>Has Data</th><th>Include</th></tr>
    """.format(pub_summary['total'], pub_summary['data_y'], pub_summary['data_n'])
    )
    for pid, pub_info in pub_collection.items():
        outfile.write(
        """
            <tr id='{}'>
                <td><a href='{}'>{}</a></td>
                <td>{}</td>
                <td><input type='checkbox' id='{}' value='{}'></td>
            </tr>
        """.format(pid, pub_info[0], fit_title(pub_info[1]), pub_info[2], pid, pub_info[3])
        )
    outfile.write(
    """
        </table>
        </div>
        <script src='https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js' 
                integrity='sha384-kenU1KFdBIe4zVF0s0G1M5b4hcpxyD9F7jL+jjXkk+Q2h455rYXK/7HAuoJl+0I4'
                crossorigin='anonymous'></script>
        <script>
            // Show selected DOI on button click
    
            $('button#seeDOI').on('click', function(){
                var selectedDoi = $('input:checkbox:checked');
                if (selectedDoi.length == 0){
                    $('svg').hide();
                    var htmlText = 'No publication is selected';
                } else {
                    $('svg').show();
                    var liText = '';
                    selectedDoi.each(function(){
                        liText += `<li>${this.value}</li>`;
                    });
                    var htmlText = `<ul>${liText}</ul>`;
                };
                $('div#doiModal div.modal-body').html(htmlText);
            });
    
            // Cop to clipboard function
            $('svg').on('click', function(){
                navigator.clipboard.writeText(
                  $('div#doiModal li').map(function () { return this.innerText }).get().join('\\n')
                );
            });
    
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
