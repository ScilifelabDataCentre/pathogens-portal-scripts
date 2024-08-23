"""
    This script is used to update JSON file used by EBI to index pathogens portal.
    At every release, the triggered workflow will run this to update relevant info.
"""

import json
import requests
import os
from datetime import datetime
from index_json_template import json_templete

def get_data_from_url(url, field=None):
    response = requests.get(url)
    rjson = response.json()
    if field:
        return rjson[field]
    else:
        return rjson

if __name__ == "__main__":
    # get release info from github
    release_info = get_data_from_url("https://api.github.com/repos/ScilifelabDataCentre/pathogens-portal/releases/latest")
    info_to_update = {
        "release" : release_info["tag_name"],
        "release_date" : release_info["published_at"][:10]
    }
    
    # dataset for which frequent updates are made
    info_urls = {
        "dataset1" : "https://blobserver.dc.scilifelab.se/blob/Serology-testing-statistics-dataset-20202021.csv/info.json",
        "dataset2" : "https://blobserver.dc.scilifelab.se/blob/CSSS_estimates_mostrecent.csv/info.json",
        "dataset3" : "https://raw.githubusercontent.com/ScilifelabDataCentre/pathogens-portal/main/data/publications.json",
        "dataset6" : "https://blobserver.dc.scilifelab.se/blob/accompdiag_table_swe.json/info.json",
        "dataset7" : "https://blobserver.dc.scilifelab.se/blob/swedishpop_subplot_button.json/info.json",
        "dataset8" : "https://blobserver.dc.scilifelab.se/blob/lineage_four_recent.json/info.json",
        "dataset10" : "https://blobserver.dc.scilifelab.se/blob/wastewater_data_gu_allviruses.xlsx/info.json",
        "dataset12" : "https://blobserver.dc.scilifelab.se/blob/stockholm_wastewater_method_Sep_2021.xlsx/info.json",
        "dataset14" : "https://blobserver.dc.scilifelab.se/blob/SLU_wastewater_data.csv/info.json",
        "dataset16" : "https://blobserver.dc.scilifelab.se/blob/wastewater_data_gu_allviruses.xlsx/info.json",
        "dataset18": "https://blobserver.dc.scilifelab.se/blob/SLU_wastewater_data.csv/info.json",
        "dataset19" : ["https://blobserver.dc.scilifelab.se/blob/KTH-produced-antigens.xlsx/info.json",
                       "https://blobserver.dc.scilifelab.se/blob/External-PLP-proteinlist.xlsx/info.json"]
    }

    # Iterate thorugh the above dict and get recent modifed dates. For all files
    # in blobserver, the info.json should have modified field in speciifc format
    for key, url in info_urls.items():
        # for dataset3 (publication data), the key is different
        field_to_get = "timestamp" if key == "dataset3" else "modified"
        # for dataset19 (multi-disease serology), we have two file to check the data
        if key == "dataset19":
            u_dates = []
            for u in url:
                u_dates.append(datetime.strptime(get_data_from_url(u, field=field_to_get)[2:10], "%y-%m-%d"))
            info_to_update[key + "_modified"] = max(u_dates).strftime("%y-%m-%d")
        else:
            info_to_update[key + "_modified"] = get_data_from_url(url, field=field_to_get)[2:10]
    new_index_data = json_templete.format(**info_to_update)

    # Check and update blob only the data is changed
    index_file_url = "https://blobserver.dc.scilifelab.se/blob/pathogens_portal_EBI_index.json"
    old_index_data = get_data_from_url(index_file_url)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    if json.loads(new_index_data) == old_index_data:
        print(timestamp + " - No new data to update")
    else:
        headers = {"x-accesskey": os.getenv("ACCESS_KEY")}
        response = requests.put(index_file_url, headers=headers, data=new_index_data.encode('utf-8'))
        if response.status_code == 200:
            print(timestamp + " - Successfully updated EBI index file")
        else:
            print(timestamp + " - Failed to update EBI index file with reason - " + response.reason)
