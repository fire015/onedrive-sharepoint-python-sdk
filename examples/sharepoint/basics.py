from msdrive import SharePoint

drive = SharePoint("access_token_here")

# List the SharePoint sites that you follow:
drive.list_followed_sites()

# Search for a SharePoint site:
drive.search_for_site("my sharepoint site")

# List a SharePoint site's drives:
drive.list_site_drives("XXX-XXX-XXX")

# List files and folders in root directory:
drive.list_items(drive_id="b!...")

# List files and folders in sub-directory:
drive.list_items(drive_id="b!...", folder_path="/General")

# Get file or folder metadata:
drive.get_item_data(drive_id="b!...", item_path="/Documents/my-data.csv")
drive.get_item_data(drive_id="b!...", item_id="01...") # if you know the item ID

# Download an existing file
drive.download_item(drive_id="b!...", item_path="/General/shared-data.csv", file_path="shared-data.csv")
drive.download_item(drive_id="b!...", item_id="01...", file_path="shared-data.csv") # if you know the item ID

# Upload a new or existing file
drive.upload_item(drive_id="b!...", item_path="/General/new-or-existing-file.csv", file_path="new-or-existing-file.csv")
drive.upload_item(drive_id="b!...", item_id="01...", file_path="existing-file.csv") # if you know the item ID