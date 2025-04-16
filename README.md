# pathogens-portal-scripts
This repository holds the scripts produced for the [Swedish Pathogens Portal](https://pathogens.se) that are not directly associated with visualisations or the underlying code used to generate the Portal itself. Those scripts can instead be found in our [visualisations repository](https://github.com/ScilifelabDataCentre/pathogens-portal-visualisations) and our [main web repository](https://github.com/ScilifelabDataCentre/pathogens-portal).

#### Available data
This folder contains all of the scripts and associated files used to update the [available data table](https://www.pathogens.se/datasets/all/) on the Portal. Instructions on the use of the scripts and files, as well as how they could potentially be changed to be used for other purposes.

#### All publications

This folder contains all of the scripts used to update the [covid publications database](https://publications-covid19.scilifelab.se/). Instructions on the use of the scripts can be found in the directory.

#### EBI Indexing

This folder contains all of the scripts used to update [EBI index JSON](https://blobserver.dc.scilifelab.se/blob/pathogens_portal_EBI_index.json/info) file. This will be run as a dialy cronjob in `dc-dynamic`. The index file is parsed by EBI (on regular basis) and the info about dataset/dashboards are put up in the main EU pathogens portal.

#### Ongoing Projects

This directory contains scripts and data related to fetching and processing information about ongoing research projects funded by the Swedish Research Council (Vetenskapsrådet).

##### `getOngoingProjects.py`

This script fetches project data from the SweCRIS API (`https://swecris-api.vr.se/v1/projects`). It performs the following steps:

1.  **Loads API Token:** Reads the `SWECRIS_API_TOKEN` from environment variables. For local development, create a `.env` file in the project root and add the token like this:
    ```
    SWECRIS_API_TOKEN="your_actual_token"
    ```
2.  **Fetches Projects:** Retrieves all project data from the API.
3.  **Filters Ongoing Projects:** Filters the projects to include only those whose start and end dates encompass the current date.
4.  **Matches Topics:** Identifies projects related to specific scientific topics (e.g., Antibiotic resistance, COVID-19, Influenza) based on keywords found in the project title or abstract.
5.  **Formats Output:** Structures the relevant information for each matched project (funder, title, funding amount, principal investigator, dates, URL).
6.  **Saves Data:** Saves the filtered and formatted project data into `Ongoing_projects/data/ongoing_research_projects.json` JSON file.


