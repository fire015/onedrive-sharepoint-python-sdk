from msdrive import OneDrive

drive = OneDrive("access_token_here")

# List files and folders in root directory:
drive.list_items()

# List files and folders in sub-directory:
drive.list_items(folder_path="/Documents")

# Get file or folder metadata:
drive.get_item_data(item_path="/Documents/my-data.csv")
drive.get_item_data(item_id="01...") # if you know the item ID

# Download an existing file
drive.download_item(item_path="/Documents/my-data.csv", file_path="my-data.csv")
drive.download_item(item_id="01...", file_path="my-data.csv") # if you know the item ID

# Upload a new or existing file
drive.upload_item(item_path="/Documents/new-or-existing-file.csv", file_path="new-or-existing-file.csv")
drive.upload_item(item_id="01...", file_path="existing-file.csv") # if you know the item ID