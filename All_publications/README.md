# All_publications
This folder contains all of the information required to update the [covid publication database](https://publications-covid19.scilifelab.se/).
This repository contains 1 python script and 1 requirements file.

<br>

### pmc_fetch_all_pubs.py

A script that queries Europe PMC using its REST API with predefined criteria and the found publications are saved in a html file for easier manual curation. This script generates a html file named 'all_publication_list.html'.

**Usage:**
```
python pmc_fetch_all_pubs.py.py
```
**Note:** Make sure the variable `main_query_string` in [line 45](https://github.com/ScilifelabDataCentre/covid-portal-scripts/blob/main/All_publications/pmc_fetch_all_pubs.py#L45) is set appropriately to get relevant publications.

<br>

### The publication list and manual filterting process 

The all_publication_list.html needs to be processed to determine which publications should be added to the covid publication database. While going through the file, mark the publication of interest with the 'Include' checkbox and finally click the "Selected DOIs" button to get the list of DOIs for the selected publications. Then these DOIs are maually used to fetch the article into covid publication database.

**Note:** The 'Include' checkmark on the left side of the publication_list.html does not persist once the HTML file is closed or refreshed.
