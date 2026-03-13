"""
setup_auth.py
─────────────
Run this ONCE before starting the main application.
It will open a browser authorization flow for BOTH accounts and cache the
tokens so the main app never needs to ask for them again.

Usage:
    python setup_auth.py

Required credential files (place in project root before running):
    mail_credentials.json  — OAuth client secret for the MAIL (Gmail) account
    cal_credentials.json   — OAuth client secret for the CALENDAR account
"""

from auth import get_mail_creds, get_calendar_creds

if __name__ == "__main__":
    print("\n" + "═" * 60)
    print("  AutomatedManager — Dual Account Setup")
    print("═" * 60)

    # ── Step 1: Mail account ───────────────────────────────────────
    print("\n[1/2] Authorizing MAIL account (Gmail read access)…")
    print("      Credential file: mail_credentials.json")
    print("      Token will be saved to: mail_token.json\n")
    try:
        mail_creds = get_mail_creds()
        print("✅  Mail account authorized successfully!")
    except FileNotFoundError as e:
        print(f"❌  {e}")
        print("    → Download OAuth credentials for your MAIL account from")
        print("      Google Cloud Console and save as 'mail_credentials.json'")
        exit(1)

    # ── Step 2: Calendar account ───────────────────────────────────
    print("\n[2/2] Authorizing CALENDAR account (Google Calendar read/write)…")
    print("      Credential file: cal_credentials.json")
    print("      Token will be saved to: cal_token.json\n")
    try:
        cal_creds = get_calendar_creds()
        print("✅  Calendar account authorized successfully!")
    except FileNotFoundError as e:
        print(f"❌  {e}")
        print("    → Download OAuth credentials for your CALENDAR account from")
        print("      Google Cloud Console and save as 'cal_credentials.json'")
        exit(1)

    print("\n" + "═" * 60)
    print("  Both accounts are authorized. You can now run:")
    print("      python main.py")
    print("═" * 60 + "\n")
