from .drive import MSDrive
from urllib.parse import quote
from .constants import BASE_GRAPH_URL


class SharePoint(MSDrive):
    """Class for accessing DriveItems stored in SharePoint.

    A DriveItem resource represents a file, folder, or other item stored in a drive (a drive being a document library in SharePoint).

    All file system objects in SharePoint are returned as DriveItem resources (see https://bit.ly/3HAAxrh).

    """

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

    def _get_drive_item_url(self, **kwargs) -> str:
        if not kwargs.get("drive_id"):
            raise ValueError("Missing drive_id argument")

        if kwargs.get("item_id"):
            return f"{BASE_GRAPH_URL}/drives/{kwargs['drive_id']}/items/{kwargs['item_id']}"

        if kwargs.get("item_path"):
            path = quote(kwargs["item_path"].lstrip("/"))
            return f"{BASE_GRAPH_URL}/drives/{kwargs['drive_id']}/root:/{path}"

        raise ValueError("Missing arguments: item_id or item_path")

    def _get_drive_children_url(self, **kwargs) -> str:
        if not kwargs.get("drive_id"):
            raise ValueError("Missing drive_id argument")

        if not kwargs.get("folder_path"):
            return f"{BASE_GRAPH_URL}/drives/{kwargs['drive_id']}/root/children"
        else:
            path = quote(kwargs["folder_path"].lstrip("/").rstrip("/"))
            return (
                f"{BASE_GRAPH_URL}/drives/{kwargs['drive_id']}/root:/{path}:/children"
            )
