import os
import pytest
from requests_mock import Mocker
from msdrive import OneDrive
from msdrive.constants import BASE_GRAPH_URL

ACCESS_TOKEN = "token123"
REQUEST_HEADERS = {"Authorization": "Bearer " + ACCESS_TOKEN}


@pytest.fixture
def drive() -> OneDrive:
    return OneDrive(ACCESS_TOKEN)


def test_get_item_data_missing_values(drive: OneDrive):
    with pytest.raises(ValueError):
        drive.get_item_data()


def test_get_item_data(drive: OneDrive, requests_mock: Mocker):
    payload = {"name": "test.csv"}

    requests_mock.get(
        f"{BASE_GRAPH_URL}/me/drive/items/123",
        request_headers=REQUEST_HEADERS,
        json=payload,
    )

    assert payload == drive.get_item_data(item_id="123")

    requests_mock.get(
        f"{BASE_GRAPH_URL}/me/drive/root:/Documents/test.csv",
        request_headers=REQUEST_HEADERS,
        json=payload,
    )

    assert payload == drive.get_item_data(item_path="/Documents/test.csv")


def test_list_items(drive: OneDrive, requests_mock: Mocker):
    payload = {"value": [{"name": "test.csv"}]}

    requests_mock.get(
        f"{BASE_GRAPH_URL}/me/drive/root/children",
        request_headers=REQUEST_HEADERS,
        json=payload,
    )

    assert payload == drive.list_items()

    requests_mock.get(
        f"{BASE_GRAPH_URL}/me/drive/root:/Some%20Files:/children",
        request_headers=REQUEST_HEADERS,
        json=payload,
    )

    assert payload == drive.list_items(folder_path="/Some Files/")


def test_download_item_missing_values(drive: OneDrive):
    with pytest.raises(ValueError):
        drive.download_item()

    with pytest.raises(ValueError):
        drive.download_item(item_id="123")

    with pytest.raises(ValueError):
        drive.download_item(item_path="test.csv")


def test_upload_item_missing_values(drive: OneDrive):
    with pytest.raises(ValueError):
        drive.upload_item()

    with pytest.raises(ValueError):
        drive.upload_item(item_id="123")

    with pytest.raises(ValueError):
        drive.upload_item(item_path="test.csv")


def test_upload_item_small(drive: OneDrive, requests_mock: Mocker):
    file_path = os.path.join(os.path.dirname(__file__), "upload_test.txt")

    requests_mock.put(
        f"{BASE_GRAPH_URL}/me/drive/items/123/content",
        request_headers=REQUEST_HEADERS,
    )

    drive.upload_item(item_id="123", file_path=file_path)

    requests_mock.put(
        f"{BASE_GRAPH_URL}/me/drive/root:/Documents/test.csv:/content",
        request_headers=REQUEST_HEADERS,
    )

    drive.upload_item(item_path="/Documents/test.csv", file_path=file_path)
