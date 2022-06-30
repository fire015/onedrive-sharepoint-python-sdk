# OneDrive and SharePoint Python SDK
A Python SDK for accessing files in OneDrive & SharePoint using the [Microsoft Graph API](https://docs.microsoft.com/en-us/onedrive/developer/rest-api/?view=odsp-graph-online).

Functionality includes:
* Upload and download files
* List files and folders in directories
* List the SharePoint sites that you follow
* Search for a SharePoint site and it's drives

## Installation

Requires Python 3.5+

```
pip install onedrive-sharepoint-python-sdk
```

## Authentication
The SDK does not handle authentication, it presumes you already have a Microsoft access token which you pass into the constructor.

## Local development

```
pip install -e .[tests]
pytest # run unit tests
```