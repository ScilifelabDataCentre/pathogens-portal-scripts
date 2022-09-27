# covid-portal-scripts
This repository holds the scripts produced for the Swedish COVID-19 Data Portal

#### pmc_pub_seeker.py

A script that queries Europe PMC using its REST API with predefined criteria and the found publications are saved in a html file for easier manual curation.

**Usage:**
```
python pmc_pub_seeker.py
```

**Note:** Make sure the variable `main_query_string` in [line 33](https://github.com/ScilifelabDataCentre/covid-portal-scripts/blob/main/pmc_pub_seeker.py#L33) is set appropriatly to get relevant publications.
