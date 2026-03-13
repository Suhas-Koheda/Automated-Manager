import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Scopes for each account role
MAIL_SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.modify",
]

CALENDAR_SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/calendar",
]


def _authenticate(creds_file: str, token_file: str, scopes: list) -> Credentials:
    """
    Core OAuth2 authentication helper.

    Args:
        creds_file: Path to the OAuth2 credentials JSON file (downloaded from Google Cloud Console).
        token_file: Path to store/load the access + refresh token.
        scopes:     List of OAuth2 scopes to request.

    Returns:
        Valid Google Credentials object.
    """
    if not os.path.exists(creds_file):
        raise FileNotFoundError(
            f"Credentials file not found: '{creds_file}'\n"
            "Download it from Google Cloud Console → APIs & Services → Credentials → OAuth 2.0 Client IDs."
        )

    creds = None
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, scopes)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                creds_file,
                scopes,
                redirect_uri="urn:ietf:wg:oauth:2.0:oob",
            )
            auth_url, _ = flow.authorization_url(prompt="consent")

            print("\n" + "=" * 60)
            print(f"Authorizing: {creds_file}")
            print("Please visit this URL in your browser to authorize:")
            print(f"\n  {auth_url}\n")
            print("=" * 60)

            code = input("Enter the authorization code: ").strip()
            flow.fetch_token(code=code)
            creds = flow.credentials

        with open(token_file, "w") as token:
            token.write(creds.to_json())
        print(f"Token saved to '{token_file}'")

    return creds


def get_mail_creds() -> Credentials:
    """
    Returns credentials for the MAIL account (Gmail read/modify).

    Credential files:
        - mail_credentials.json  → OAuth client secret for the mail account
        - mail_token.json        → Cached tokens (auto-created after first login)
    """
    return _authenticate(
        creds_file="mail_credentials.json",
        token_file="mail_token.json",
        scopes=MAIL_SCOPES,
    )


def get_calendar_creds() -> Credentials:
    """
    Returns credentials for the CALENDAR account (Google Calendar read/write).

    Credential files:
        - cal_credentials.json  → OAuth client secret for the calendar account
        - cal_token.json        → Cached tokens (auto-created after first login)
    """
    return _authenticate(
        creds_file="cal_credentials.json",
        token_file="cal_token.json",
        scopes=CALENDAR_SCOPES,
    )


# ---------------------------------------------------------------------------
# Backwards-compatibility shim — keeps old code working during migration
# ---------------------------------------------------------------------------
def check_auth() -> Credentials:
    """
    Legacy helper. Returns combined credentials using the original credentials.json.
    Kept for backwards compatibility; prefer get_mail_creds() / get_calendar_creds().
    """
    return _authenticate(
        creds_file="credentials.json",
        token_file="token.json",
        scopes=MAIL_SCOPES + CALENDAR_SCOPES,
    )