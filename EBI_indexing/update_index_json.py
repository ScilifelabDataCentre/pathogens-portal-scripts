# """
#     This script is used to update JSON file used by EBI to index pathogens portal.
#     At every release, the triggered workflow will run this to update relevant info.
# """

import json
import requests
import os
from datetime import datetime
from index_json_template import json_template
import logging

def get_data_from_url(url, field=None):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        rjson = response.json()
        return rjson[field] if field else rjson
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data from {url}: {e}")
        return None
    except json.JSONDecodeError as e:
        logging.error(f"Error parsing JSON response from {url}: {e}")
        return None


def get_latest_commit_date_from_github(url):
    """
    Fetches the latest commit date from the GitHub API response.
    
    :param url: URL to fetch commit data from GitHub API
    :return: The date of the latest commit in YYYY-MM-DD format or None if error occurs
    """
    try:
        commits = get_data_from_url(url)
        if commits and isinstance(commits, list) and len(commits) > 0:
            commit_date = commits[0]['commit']['committer']['date']
            return commit_date[:10]  # Return only the date in YYYY-MM-DD format
        else:
            logging.error("No commits found or unexpected response structure.")
            return None
    except Exception as e:
        logging.error(f"Error fetching commit date from GitHub: {e}")
        return None

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        # Get release info from GitHub
        release_info = get_data_from_url("https://api.github.com/repos/ScilifelabDataCentre/pathogens-portal/releases/latest")
        if not release_info:
            logging.error("Failed to fetch release information.")
            exit(1)
            
        info_to_update = {
            "release": release_info["tag_name"],
            "release_date": release_info["published_at"][:10]
        }
        
        # Dataset URLs and updates
        info_urls = {
            "dataset7": "https://blobserver.dc.scilifelab.se/blob/swedishpop_subplot_button.json/info.json",
            "dataset8": "https://blobserver.dc.scilifelab.se/blob/lineage_four_recent.json/info.json",
            "dataset10": "https://blobserver.dc.scilifelab.se/blob/wastewater_data_gu_allviruses.xlsx/info.json",
            "dataset14": "https://blobserver.dc.scilifelab.se/blob/SLU_wastewater_data.csv/info.json",
            "dataset16": "https://blobserver.dc.scilifelab.se/blob/wastewater_data_gu_allviruses.xlsx/info.json",
            "dataset18": "https://blobserver.dc.scilifelab.se/blob/SLU_wastewater_data.csv/info.json",
            "dataset20": "https://api.github.com/repos/MurrellGroup/lineages/commits?path=plots&page=1&per_page=1"
        }
        
        for key, url in info_urls.items():
            if key == "dataset20":
                modified_date = get_latest_commit_date_from_github(url)
            else:
                modified_date = get_data_from_url(url, field="modified")
                if modified_date:
                    modified_date = modified_date[2:10]  # Format date to 'YYYY-MM-DD'
            
            if modified_date:
                info_to_update[f"{key}_modified"] = modified_date
            else:
                logging.warning(f"Failed to get modified date for {key} from {url}")

        new_index_data = json_template.format(**info_to_update)
        
        # Fetch current index file data
        index_file_url = "https://blobserver.dc.scilifelab.se/blob/pathogens_portal_EBI_index.json"
        old_index_data = get_data_from_url(index_file_url)
        
        if not old_index_data:
            logging.error("Failed to fetch current index data.")
            exit(1)
            
        # Check for updates
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        if json.loads(new_index_data) == old_index_data:
            logging.info(f"{timestamp} - No new data to update")
        else:
            headers = {"x-accesskey": os.getenv("ACCESS_KEY")}
            response = requests.put(index_file_url, headers=headers, data=new_index_data.encode('utf-8'))
            if response.status_code == 200:
                logging.info(f"{timestamp} - Successfully updated EBI index file")
            else:
                logging.error(f"{timestamp} - Failed to update EBI index file: {response.reason}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")