import os
from requests import Session
from urllib.parse import quote
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from .constants import BASE_GRAPH_URL, SIMPLE_UPLOAD_MAX_SIZE, CHUNK_UPLOAD_MAX_SIZE


class MSDrive:
    """Class for accessing files stored in OneDrive and SharePoint (known as DriveItems).

    A DriveItem resource represents a file, folder, or other item stored in a drive.

    All file system objects in OneDrive and SharePoint are returned as DriveItem resources (see https://bit.ly/3HAAxrh).

    OneDrive example use::

        from msdrive.drive import MSDrive
        drive = MSDrive()

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

    SharePoint example use::

        # Note: a drive ID is required for most methods (a drive being a document library in SharePoint)
        # and this can sometimes be difficult to figure out. You can use some of the helper methods below
        # to work out the drive ID:

        from msdrive.drive import MSDrive
        drive = MSDrive()

        # List the SharePoint sites that you follow:
        drive.list_followed_sites()

        # Search for a SharePoint site:
        drive.search_for_site("my sharepoint site")

        # Once you have found the site you are looking for, take the site ID and pass it to the method below to list it's drives:
        drive.list_site_drives("XXX-XXX-XXX")

        # Once you have found the drive you are looking for (usually 1 called "Documents") take the drive ID for use below:

        # List files and folders in root directory:
        drive.list_items(drive_id="b!...")

        # List files and folders in sub-directory:
        drive.list_items(drive_id="b!...", folder_path="/General")

        # Download an existing file
        drive.download_item(drive_id="b!...", item_path="/General/shared-data.csv", file_path="shared-data.csv")
        drive.download_item(drive_id="b!...", item_id="01...", file_path="shared-data.csv") # if you know the item ID

        # Upload a new or existing file
        drive.upload_item(drive_id="b!...", item_path="/General/new-or-existing-file.csv", file_path="new-or-existing-file.csv")
        drive.upload_item(drive_id="b!...", item_id="01...", file_path="existing-file.csv") # if you know the item ID

    """

    def __init__(self, access_token: str) -> None:
        """Class constructor that accepts a Microsoft access token for use with the OneDrive/SharePoint API

        Args:
            access_token (str): The Microsoft access token
        """
        self.access_token = access_token

    def get_item_data(self, **kwargs) -> dict:
        """Get metadata for a DriveItem.

        Args:
            drive_id (str): The drive ID (or "me" for your own OneDrive)
            item_id (str): [EITHER] The item ID
            item_path (str): [EITHER] The item path

        Returns:
            dict: JSON representation of a DriveItem resource
        """
        r = self._session().get(self._get_drive_item_url(**kwargs))

        return r.json()

    def list_items(self, **kwargs) -> dict:
        """List the DriveItems in a specific folder path.

        Args:
            drive_id (str): The drive ID (or "me" for your own OneDrive)
            folder_path (str): The folder path (or leave out for root)

        Returns:
            dict: JSON representation of a collection of DriveItem resources
        """
        r = self._session().get(self._get_drive_children_url(**kwargs))

        return r.json()

    def download_item(self, **kwargs) -> None:
        """Download a DriveItem file to a specific local path.

        Args:
            drive_id (str): The drive ID (or "me" for your own OneDrive)
            item_id (str): [EITHER] The item ID
            item_path (str): [EITHER] The item path
            file_path (str): Local path to save the file to (e.g. /tmp/blah.csv)
        """
        if not kwargs.get("file_path"):
            raise ValueError("Missing file_path argument")

        data = self.get_item_data(**kwargs)

        with Session().get(data["@microsoft.graph.downloadUrl"], stream=True) as r:
            r.raise_for_status()

            with open(kwargs["file_path"], "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

    def upload_item(self, **kwargs) -> None:
        """Upload a local file to an existing or new DriveItem.

        Specify the item_path for a new file.
        Specify the item_path or item_id for an existing file.

        Args:
            drive_id (str): The drive ID (or "me" for your own OneDrive)
            item_id (str): [EITHER] The item ID
            item_path (str): [EITHER] The item path
            file_path (str): Local path to upload the file from (e.g. /tmp/blah.csv)
        """
        if not kwargs.get("file_path"):
            raise ValueError("Missing file_path argument")

        file_size = os.stat(kwargs["file_path"]).st_size

        if file_size <= SIMPLE_UPLOAD_MAX_SIZE:
            self._upload_item_small(**kwargs)
        else:
            self._upload_item_large(**kwargs)

    def list_followed_sites(self) -> dict:
        """List the SharePoint sites that you follow.

        Returns:
            dict: JSON representation of a collection of site resources
        """
        r = self._session().get(f"{BASE_GRAPH_URL}/me/followedSites")

        return r.json()

    def search_for_site(self, search_query: str) -> dict:
        """Search for a SharePoint site.

        Args:
            search_query (str): The search query

        Returns:
            dict: JSON representation of a collection of site resources
        """
        r = self._session().get(
            f"{BASE_GRAPH_URL}/sites", params={"search": search_query}
        )

        return r.json()

    def list_site_drives(self, site_id: str) -> dict:
        """List a SharePoint site's drives.

        Args:
            site_id (str): The site ID

        Returns:
            dict: JSON representation of a collection of drive resources
        """
        r = self._session().get(f"{BASE_GRAPH_URL}/sites/{site_id}/drives")

        return r.json()

    def _session(self) -> Session:
        # Raise HTTPError for non-200 status codes
        raise_status_hook = (
            lambda response, *args, **kwargs: response.raise_for_status()
        )

        s = Session()
        s.hooks["response"] = [raise_status_hook]
        s.headers.update({"Authorization": "Bearer " + self.access_token})

        return s

    def _session_upload(self) -> Session:
        # Raise HTTPError for non-200 status codes
        raise_status_hook = (
            lambda response, *args, **kwargs: response.raise_for_status()
        )

        # Retry on failure (https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/)
        retries = Retry(
            total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504]
        )

        adapter = HTTPAdapter(max_retries=retries)

        s = Session()
        s.mount("http://", adapter)
        s.mount("https://", adapter)
        s.hooks["response"] = [raise_status_hook]

        return s

    def _get_drive_item_url(self, **kwargs) -> str:
        if kwargs.get("drive_id") and kwargs.get("item_id"):
            if kwargs["drive_id"] == "me":
                return f"{BASE_GRAPH_URL}/me/drive/items/{kwargs['item_id']}"
            else:
                return f"{BASE_GRAPH_URL}/drives/{kwargs['drive_id']}/items/{kwargs['item_id']}"

        if kwargs.get("drive_id") and kwargs.get("item_path"):
            path = quote(kwargs["item_path"].lstrip("/"))

            if kwargs["drive_id"] == "me":
                return f"{BASE_GRAPH_URL}/me/drive/root:/{path}"
            else:
                return f"{BASE_GRAPH_URL}/drives/{kwargs['drive_id']}/root:/{path}"

        raise ValueError(
            "Missing arguments: drive_id + item_id or drive_id + item_path"
        )

    def _get_drive_children_url(self, **kwargs) -> str:
        if not kwargs.get("drive_id"):
            raise ValueError("Missing drive_id argument")

        if not kwargs.get("folder_path"):
            if kwargs["drive_id"] == "me":
                return f"{BASE_GRAPH_URL}/me/drive/root/children"
            else:
                return f"{BASE_GRAPH_URL}/drives/{kwargs['drive_id']}/root/children"
        else:
            path = quote(kwargs["folder_path"].lstrip("/").rstrip("/"))

            if kwargs["drive_id"] == "me":
                return f"{BASE_GRAPH_URL}/me/drive/root:/{path}:/children"
            else:
                return f"{BASE_GRAPH_URL}/drives/{kwargs['drive_id']}/root:/{path}:/children"

    def _upload_item_small(self, **kwargs) -> None:
        url = self._get_drive_item_url(**kwargs)
        file_data = open(kwargs["file_path"], "rb")

        if kwargs.get("item_id"):
            url += "/content"
        else:
            url += ":/content"

        try:
            self._session().put(url, data=file_data)
        finally:
            file_data.close()

    def _upload_item_large(self, **kwargs) -> None:
        upload_url = self._get_upload_url(**kwargs)
        file_size = os.stat(kwargs["file_path"]).st_size

        with open(kwargs["file_path"], "rb") as f:
            chunk_size = CHUNK_UPLOAD_MAX_SIZE
            chunk_number = file_size // chunk_size
            chunk_leftover = file_size - chunk_size * chunk_number
            chunk_data = f.read(chunk_size)
            i = 0

            while chunk_data:
                start_index = i * chunk_size
                end_index = start_index + chunk_size

                if i == chunk_number:
                    end_index = start_index + chunk_leftover

                s = self._session_upload()

                # Setting the header with the appropriate chunk data location in the file
                headers = {
                    "Content-Length": str(chunk_size),
                    "Content-Range": "bytes {}-{}/{}".format(
                        start_index, end_index - 1, file_size
                    ),
                }

                s.headers.update(headers)
                s.put(upload_url, data=chunk_data)

                i = i + 1
                chunk_data = f.read(chunk_size)

    def _get_upload_url(self, **kwargs) -> str:
        url = self._get_drive_item_url(**kwargs)

        if kwargs.get("item_id"):
            url += "/createUploadSession"
        else:
            url += ":/createUploadSession"

        r = self._session().post(url)

        return r.json()["uploadUrl"]
