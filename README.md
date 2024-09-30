# splunk_apps_props

This repository contains a data set of Splunk app properties. The data set is in JSON. Information from each application is retrieved directly from SplunkBase.

## Workflow

The two workflows bring this repository to life by automatically collecting information from the applications.

### Workflow 1: Collecting Splunk App Properties

From the apps.csv file, the `update_data.yml` workflow collects the properties of each application with the help of `app_props.py` and stores them in a JSON file.

### Workflow 2: Content Update

The `list_contents.yml` workflow lists the contents of the `data` directory and updates the `contents-data.csv` file with the latest information.