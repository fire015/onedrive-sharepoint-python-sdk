import os
import pytest
from requests_mock import Mocker
from msdrive import SharePoint
from msdrive.constants import BASE_GRAPH_URL

ACCESS_TOKEN = "token123"
REQUEST_HEADERS = {"Authorization": "Bearer " + ACCESS_TOKEN}


@pytest.fixture
def drive() -> SharePoint:
    return SharePoint(ACCESS_TOKEN)


def test_get_item_data_missing_values(drive: SharePoint):
    with pytest.raises(ValueError):
        drive.get_item_data()

    with pytest.raises(ValueError):
        drive.get_item_data(drive_id="b!1abc")


def test_get_item_data(drive: SharePoint, requests_mock: Mocker):
    payload = {"name": "test.csv"}

    requests_mock.get(
        f"{BASE_GRAPH_URL}/drives/b!1abc/items/123",
        request_headers=REQUEST_HEADERS,
        json=payload,
    )

    assert payload == drive.get_item_data(drive_id="b!1abc", item_id="123")

    requests_mock.get(
        f"{BASE_GRAPH_URL}/drives/b!1abc/root:/Documents/test.csv",
        request_headers=REQUEST_HEADERS,
        json=payload,
    )

    assert payload == drive.get_item_data(
        drive_id="b!1abc", item_path="/Documents/test.csv"
    )


def test_list_items_missing_values(drive: SharePoint):
    with pytest.raises(ValueError):
        drive.list_items()


def test_list_items(drive: SharePoint, requests_mock: Mocker):
    payload = {"value": [{"name": "test.csv"}]}

    requests_mock.get(
        f"{BASE_GRAPH_URL}/drives/b!1abc/root/children",
        request_headers=REQUEST_HEADERS,
        json=payload,
    )

    assert payload == drive.list_items(drive_id="b!1abc")

    requests_mock.get(
        f"{BASE_GRAPH_URL}/drives/b!1abc/root:/Some%20Files:/children",
        request_headers=REQUEST_HEADERS,
        json=payload,
    )

    assert payload == drive.list_items(drive_id="b!1abc", folder_path="/Some Files/")


def test_download_item_missing_values(drive: SharePoint):
    with pytest.raises(ValueError):
        drive.download_item()

    with pytest.raises(ValueError):
        drive.download_item(drive_id="b!1abc")

    with pytest.raises(ValueError):
        drive.download_item(drive_id="b!1abc", item_id="123")

    with pytest.raises(ValueError):
        drive.download_item(drive_id="b!1abc", item_path="test.csv")


def test_upload_item_missing_values(drive: SharePoint):
    with pytest.raises(ValueError):
        drive.upload_item()

    with pytest.raises(ValueError):
        drive.upload_item(drive_id="b!1abc")

    with pytest.raises(ValueError):
        drive.upload_item(drive_id="b!1abc", item_id="123")

    with pytest.raises(ValueError):
        drive.upload_item(drive_id="b!1abc", item_path="test.csv")


def test_upload_item_small(drive: SharePoint, requests_mock: Mocker):
    file_path = os.path.join(os.path.dirname(__file__), "upload_test.txt")

    requests_mock.put(
        f"{BASE_GRAPH_URL}/drives/b!1abc/items/123/content",
        request_headers=REQUEST_HEADERS,
    )

    drive.upload_item(drive_id="b!1abc", item_id="123", file_path=file_path)

    requests_mock.put(
        f"{BASE_GRAPH_URL}/drives/b!1abc/root:/Documents/test.csv:/content",
        request_headers=REQUEST_HEADERS,
    )

    drive.upload_item(
        drive_id="b!1abc", item_path="/Documents/test.csv", file_path=file_path
    )


def test_list_followed_sites(drive: SharePoint, requests_mock: Mocker):
    payload = {"value": [{"displayName": "Test site"}]}

    requests_mock.get(
        f"{BASE_GRAPH_URL}/me/followedSites",
        request_headers=REQUEST_HEADERS,
        json=payload,
    )

    assert payload == drive.list_followed_sites()


def test_search_for_site(drive: SharePoint, requests_mock: Mocker):
    payload = {"value": [{"displayName": "Test site"}]}

    requests_mock.get(
        f"{BASE_GRAPH_URL}/sites?search=test+site",
        request_headers=REQUEST_HEADERS,
        json=payload,
    )

    assert payload == drive.search_for_site("test site")


def test_list_site_drives(drive: SharePoint, requests_mock: Mocker):
    payload = {"value": [{"name": "Documents"}]}

    requests_mock.get(
        f"{BASE_GRAPH_URL}/sites/123/drives",
        request_headers=REQUEST_HEADERS,
        json=payload,
    )

    assert payload == drive.list_site_drives("123")
