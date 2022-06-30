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

## Authentication
The SDK does not handle authentication, it presumes you already have a Microsoft access token which you pass into the constructor.

Here is an example using [MSAL](https://pypi.org/project/msal/) to handle authentication:

```
import msal
from msdrive import MSDrive

def acquire_token():
    authority_url = 'https://login.microsoftonline.com/{tenant_id_or_name}'
    app = msal.ConfidentialClientApplication(
        authority=authority_url,
        client_id='{client_id}',
        client_credential='{client_secret}'
    )
    token = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    return token


access_token = acquire_token()
drive = MSDrive(access_token)
```

## OneDrive example use
```
from msdrive import MSDrive

drive = MSDrive("access_token_here")

# List files and folders in root directory:
drive.list_items(drive_id="me")

# List files and folders in sub-directory:
drive.list_items(drive_id="me", folder_path="/Documents")

# Download an existing file
drive.download_item(drive_id="me", item_path="/Documents/my-data.csv", file_path="my-data.csv")
drive.download_item(drive_id="me", item_id="01...", file_path="my-data.csv") # if you know the item ID

# Upload a new or existing file
drive.upload_item(drive_id="me", item_path="/Documents/new-or-existing-file.csv", file_path="new-or-existing-file.csv")
drive.upload_item(drive_id="me", item_id="01...", file_path="existing-file.csv") # if you know the item ID
```

## Local development

```
pip install -e .[tests]
pytest # run unit tests
```