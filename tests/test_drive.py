import pytest
from requests_mock import Mocker
from msdrive import MSDrive
from msdrive.constants import BASE_GRAPH_URL

ACCESS_TOKEN = "token123"
REQUEST_HEADERS = {"Authorization": "Bearer " + ACCESS_TOKEN}


@pytest.fixture
def drive() -> MSDrive:
    return MSDrive(ACCESS_TOKEN)


def test_missing_drive_arguments(drive: MSDrive):
    with pytest.raises(ValueError):
        drive.get_item_data()

    with pytest.raises(ValueError):
        drive.get_item_data(drive_id="me")


def test_get_item_data(drive: MSDrive, requests_mock: Mocker):
    payload = {"name": "test.csv"}

    requests_mock.get(
        f"{BASE_GRAPH_URL}/me/drive/items/123",
        request_headers=REQUEST_HEADERS,
        json=payload,
    )

    assert payload == drive.get_item_data(drive_id="me", item_id="123")

    requests_mock.get(
        f"{BASE_GRAPH_URL}/me/drive/root:/Documents/test.csv",
        request_headers=REQUEST_HEADERS,
        json=payload,
    )

    assert payload == drive.get_item_data(
        drive_id="me", item_path="/Documents/test.csv"
    )

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
