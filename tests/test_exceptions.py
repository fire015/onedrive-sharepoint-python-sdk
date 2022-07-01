import pytest
from msdrive import OneDrive
from msdrive.constants import BASE_GRAPH_URL
from msdrive.exceptions import *
from requests.exceptions import HTTPError
from requests_mock import Mocker

ACCESS_TOKEN = "token123"
REQUEST_HEADERS = {"Authorization": "Bearer " + ACCESS_TOKEN}


@pytest.fixture
def drive() -> OneDrive:
    return OneDrive(ACCESS_TOKEN)


def test_exception_with_no_response(drive: OneDrive, requests_mock: Mocker):
    requests_mock.get(
        f"{BASE_GRAPH_URL}/me/drive/root:/none.csv",
        request_headers=REQUEST_HEADERS,
        status_code=404,
    )

    with pytest.raises(HTTPError):
        drive.get_item_data(item_path="/none.csv")


def test_exception_with_missing_json(drive: OneDrive, requests_mock: Mocker):
    requests_mock.get(
        f"{BASE_GRAPH_URL}/me/drive/root:/none.csv",
        request_headers=REQUEST_HEADERS,
        status_code=404,
        json={"error": None},
    )

    with pytest.raises(HTTPError):
        drive.get_item_data(item_path="/none.csv")


def test_invalid_access_token_exception(drive: OneDrive, requests_mock: Mocker):
    requests_mock.get(
        f"{BASE_GRAPH_URL}/me/drive/root:/none.csv",
        request_headers=REQUEST_HEADERS,
        status_code=401,
        json={"error": {"message": "Invalid token"}},
    )

    with pytest.raises(InvalidAccessToken, match="Invalid token"):
        drive.get_item_data(item_path="/none.csv")


def test_item_not_found_exception(drive: OneDrive, requests_mock: Mocker):
    requests_mock.get(
        f"{BASE_GRAPH_URL}/me/drive/root:/none.csv",
        request_headers=REQUEST_HEADERS,
        status_code=404,
        json={"error": {"message": "Item not found"}},
    )

    with pytest.raises(ItemNotFound, match="Item not found"):
        drive.get_item_data(item_path="/none.csv")


def test_rate_limited_exception(drive: OneDrive, requests_mock: Mocker):
    requests_mock.get(
        f"{BASE_GRAPH_URL}/me/drive/root:/none.csv",
        request_headers=REQUEST_HEADERS,
        status_code=429,
        json={"error": {"message": "Rate limited"}},
    )

    with pytest.raises(RateLimited, match="Rate limited"):
        drive.get_item_data(item_path="/none.csv")


def test_drive_exception(drive: OneDrive, requests_mock: Mocker):
    requests_mock.get(
        f"{BASE_GRAPH_URL}/me/drive/root:/none.csv",
        request_headers=REQUEST_HEADERS,
        status_code=500,
        json={"error": {"message": "Ambiguous error"}},
    )

    with pytest.raises(DriveException, match="Ambiguous error"):
        drive.get_item_data(item_path="/none.csv")
