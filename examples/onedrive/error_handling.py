from msdrive import OneDrive
from msdrive.exceptions import (
    DriveException,
    InvalidAccessToken,
    ItemNotFound,
    RateLimited,
)

# Catch generic errors
try:
    drive = OneDrive("access_token_here")
    drive.list_items()
except DriveException as err:
    print("Something went wrong:", err)


# Catch invalid access token
try:
    drive = OneDrive("access_token_here")
    drive.list_items()
except InvalidAccessToken as err:
    print("Invalid access token:", err)


# Catch item not found
try:
    drive = OneDrive("access_token_here")
    drive.list_items()
except ItemNotFound as err:
    print("Item not found:", err)


# Catch rate limit exceeded
try:
    drive = OneDrive("access_token_here")
    drive.list_items()
except RateLimited as err:
    print("Rate limited:", err)
