# This is an example using MSAL and it's device code flow to login
# https://github.com/Azure-Samples/ms-identity-python-devicecodeflow

import msal
from msdrive import OneDrive

AUTHORITY_URL = "https://login.microsoftonline.com/{tenant_id_or_name}"
CLIENT_ID = "xxx-xxx-xx"


def get_access_token():
    app = msal.PublicClientApplication(authority=AUTHORITY_URL, client_id=CLIENT_ID)

    # Start the device flow and print instructions to screen
    flow = app.initiate_device_flow(scopes=["Files.Read.All"])
    print(flow["message"])

    # Block until user logs in
    result = app.acquire_token_by_device_flow(flow)

    if "access_token" in result:
        return result["access_token"]
    else:
        raise Exception(result["error"])


token = get_access_token()
drive = OneDrive(token)
print(drive.list_items())
