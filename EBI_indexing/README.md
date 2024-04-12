## EBI indexing

This folder contains

* `pathogens_portal_index.json` - a JSON file which is used by EBI to index provided information/datset from our website.
* `update_index_json.py` - a python script that is used to generate the JSON file with recent "updated date" for some dashboards.
* `index_json_template.py` - a python script with a JSON template that is imported and used in the `update_index_json.py` script. This file should be updated if new dataset is to be added.