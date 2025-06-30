import os
import sys
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

def resource_path(relative_path):
    """Get absolute path to resource (for PyInstaller or dev run)"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)

def get_gmail_service():
    creds = None

    # Use actual file for token (don't embed inside app)
    token_path = os.path.join(os.getcwd(), "token.pickle")

    if os.path.exists(token_path):
        with open(token_path, "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            resource_path("credentials.json"), SCOPES
        )
        creds = flow.run_local_server(port=0)

        # Save token for future use
        with open(token_path, "wb") as token:
            pickle.dump(creds, token)

    return build("gmail", "v1", credentials=creds)
