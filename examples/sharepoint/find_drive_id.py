# A drive ID is required for most SharePoint methods (a drive being a document library in SharePoint)
# and this can sometimes be difficult to figure out. You can use the code below to find the drive ID:

from msdrive import SharePoint


def find_drive_id(access_token, site_name):
    # Invoke the class
    drive = SharePoint(access_token)

    # Search for the site
    sites = drive.search_for_site(site_name)

    # No sites found!
    if len(sites["value"]) == 0:
        return

    # Assume the first result is the site you want
    site_id = sites["value"][0]["id"]

    # List the site's drives
    site_drives = drive.list_site_drives(site_id)

    # No drives found!
    if len(site_drives["value"]) == 0:
        return

    drive_id = site_drives["value"][0]["id"]

    return drive_id
