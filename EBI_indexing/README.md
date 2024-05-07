## EBI indexing

This folder contains all of the scripts used to update [EBI index JSON](https://blobserver.dc.scilifelab.se/blob/pathogens_portal_EBI_index.json/info) file. The index file is parsed by EBI (on regular basis) and the info about dataset/dashboards are put up in the main EU pathogens portal.

* `update_index_json.py` - a python script that is used to generate the JSON file with recent "updated date" for some dashboards. This will be run as a [dialy cronjob](https://github.com/ScilifelabDataCentre/dc-dynamic/blob/master/runner_daily.sh#L5) in `dc-dynamic`.
* `index_json_template.py` - a python script with a JSON template that is imported and used in the `update_index_json.py` script. This file should be updated if new dataset is to be added.
