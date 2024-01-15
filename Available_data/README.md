# Available data
This folder contains all of the information required to update the [available data table](https://www.pathogens.se/datasets/all/) on the Pathogens Portal.
This repository contains 2 python scripts, 1 json template file and 1 requirements file. Follow the next steps in chronological order.

<br>

### pmc_available_data.py

A script that queries Europe PMC using its REST API with predefined criteria and the found publications are saved in a html file for easier manual curation. This script generates a html file named 'publication_list.html'.

**Usage:**
```
python pmc_available_data.py
```
**Note:** Make sure the variable `main_query_string` in [line 45](https://github.com/ScilifelabDataCentre/covid-portal-scripts/blob/main/Available_data/pmc_available_data.py#L45) is set appropriately to get relevant publications.

<br>

### The publication list and manual filterting process 
The publication_list.html needs to be processed to determine which publications should be added to the available data table. Keep in mind that the 'Read' checkmark on the left side of the publication_list.html does not persist once the HTML file is closed. 
The 'Has Data' column exists because articles are labeled with either 'Y' or 'N' depending on the information provided by the author/submitter. Occasionally, authors may forget to indicate 'Data available' even when they have data to share, resulting in an 'N' designation. To address this, it is recommended to manually search for keywords like GitHub or Figshare in the article. If these keywords are present, check if they relate to data or were mentioned in another relevant context.

<br>

### mdata.json

This file includes the basic template to be filled in manually with the filtered publications from the publication_list.html. You should list all of the data and code items in the 'available items' list for each publication, which is represented in the DOI for each item in the 'dataset'.
Possible item types are code, repository and script. The possible data types can be seen on the [available data table](https://www.pathogens.se/datasets/all/) on the Portal. One item can contain several data types.
Example:
```json
{
            "doi": "10.3389/fimmu.2023.1166924",
            "available_items": [
                {
                    "type": "data",
                    "repo_name": "Protein Data Bank",
                    "accession_number": "7KRR",
                    "description": "Protein structures in PDBe",
                    "data_type": ["Protein data"],
                    "data_url": "https://www.ebi.ac.uk/pdbe/entry/pdb/7KRR"
                },
                {
                    "type": "data",
                    "repo_name": "GenBank",
                    "accession_number": "NC_045512.2",
                    "description": "RefSeq - NCBI Reference Sequence Database",
                    "data_type": ["Genomics & transcriptomics data"],
                    "data_url": "https://www.ncbi.nlm.nih.gov/nuccore/NC_045512.2"
                }
            ]
        }
```
<br>

### doi_to_info.py

This script will fill in the required information about each publication for the [available data table](https://www.pathogens.se/datasets/all/). Once the mdata.json file is filled as needed, it can be renamed as required (e.g. to "dec_data.json"). It can then be passed to this script immediately. This will produce a file named 'new_data_info.json'. The contents can then be copied into the [available data file](https://github.com/ScilifelabDataCentre/covid-portal/blob/develop/data/available_datasets.json) as needed.

**Usage:**
```
python doi_to_info.py
```

**Note:** Make sure the filename in [line 7](https://github.com/ScilifelabDataCentre/covid-portal-scripts/blob/main/Available_data/doi_to_info.py#L7) is set to mdata.json, or whatever you renamed this file to be.
