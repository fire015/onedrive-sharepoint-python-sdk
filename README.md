# OneDrive and SharePoint Python SDK
A Python SDK for accessing files in OneDrive & SharePoint using the [Microsoft Graph API](https://docs.microsoft.com/en-us/onedrive/developer/rest-api/?view=odsp-graph-online).

Functionality includes:
* Upload and download files
* List files and folders in directories
* List the SharePoint sites that you follow
* Search for a SharePoint site and it's drives

## Installation
Requires Python 3.7+

```
pip install onedrive-sharepoint-python-sdk
```

## Examples
See the [examples](https://github.com/fire015/onedrive-sharepoint-python-sdk/tree/master/examples) folder for more.

### OneDrive
```python
from msdrive import OneDrive

drive = OneDrive("access_token_here")

drive.download_item(item_path="/Documents/my-data.csv", file_path="my-data.csv")
drive.upload_item(item_path="/Documents/new-or-existing-file.csv", file_path="new-or-existing-file.csv")
```

### SharePoint
```python
from msdrive import SharePoint

drive = SharePoint("access_token_here")

drive.download_item(drive_id="b!...", item_path="/General/shared-data.csv", file_path="shared-data.csv")
drive.upload_item(drive_id="b!...", item_path="/General/new-or-existing-file.csv", file_path="new-or-existing-file.csv")
```

## Authentication
The SDK does not handle authentication, it presumes you already have a Microsoft access token which you pass into the constructor (see [auth example](https://github.com/fire015/onedrive-sharepoint-python-sdk/blob/master/examples/auth.py)).

Use a library like [MSAL](https://pypi.org/project/msal/) or [Azure Identity](https://pypi.org/project/azure-identity/) to handle this.

## Local Development
```
pip install -e .[tests]
pytest # run unit tests
```

## Deployment
Bump the version in `pyproject.toml` and `src/msdrive/__init__.py` and then run the `Upload Python Package` pipeline.