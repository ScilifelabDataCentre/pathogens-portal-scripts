# Available data
This folder contains all of the information required to update the [available data table](https://www.covid19dataportal.se/datasets/all/) on the Portal.

#### pmc_pub_seeker.py

A script that queries Europe PMC using its REST API with predefined criteria and the found publications are saved in a html file for easier manual curation. This script generates a html file named 'publication_list.html'. This can be processed to determine which publications should be added to the available data table. 

**Usage:**
```
python pmc_pub_seeker.py
```

**Note:** Make sure the variable `main_query_string` in [line 33](https://github.com/ScilifelabDataCentre/covid-portal-scripts/blob/main/pmc_pub_seeker.py#L33) is set appropriately to get relevant publications.

#### mdata.json

This file includes the basic template to be filled in to add publications (and the associated shared data and code) into the available data table on the Portal. You should list all of the data and code items in the 'available items' list for each publication, which is represented in the DOI for each item in the 'dataset'. 

#### doi_to_info.py

This script will fill in the required information about each publication for the [available data table](https://www.covid19dataportal.se/datasets/all/). Once the mdata.json file is filled as needed, it can be renamed as required (e.g. to "dec_data.json"). It can then be passed to this script immediately. This will produce a file named 'new_data_info.json'. The contents can then be copied into the [available data file](https://github.com/ScilifelabDataCentre/covid-portal/blob/develop/data/available_datasets.json) as needed.

**Usage:**
```
python doi_to_info.py
```

**Note:** Make sure the filename in [line 7](https://github.com/ScilifelabDataCentre/covid-portal-scripts/Available data/blob/main/doi_to_info.py#L7) is set to mdata.json, or whatever you renamed this file to be.
