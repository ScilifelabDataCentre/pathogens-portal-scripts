# pathogens-portal-scripts
This repository holds the scripts produced for the [Swedish Pathogens Portal](https://pathogens.se) that are not directly associated with visualisations or the underlying code used to generate the Portal itself. Those scripts can instead be found in our [visualisations repository](https://github.com/ScilifelabDataCentre/pathogens-portal-visualisations) and our [main web repository](https://github.com/ScilifelabDataCentre/pathogens-portal).

#### Available data
This folder contains all of the scripts and associated files used to update the [available data table](https://www.pathogens.se/datasets/all/) on the Portal. Instructions on the use of the scripts and files, as well as how they could potentially be changed to be used for other purposes.

#### All publications

This folder contains all of the scripts used to update the [covid publications database](https://publications-covid19.scilifelab.se/). Instructions on the use of the scripts can be found in the directory.

#### EBI Indexing

This folder contains all of the scripts used to update [EBI index JSON](https://blobserver.dc.scilifelab.se/blob/pathogens_portal_EBI_index.json/info) file. This will be run as a dialy cronjob in `dc-dynamic`.
