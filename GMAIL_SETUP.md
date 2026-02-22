# Gmail OAuth Setup Guide

## Prerequisites

- Google account with Gmail
- Friday AI running

## Step 1: Google Cloud Console

### Create Project

1. Go to: https://console.cloud.google.com/
2. Click "New Project"
3. Name: "Friday AI Assistant"
4. Click "Create"

### Enable Gmail API

1. In your project, go to "APIs & Services" → "Library"
2. Search for "Gmail API"
3. Click "Enable"

## Step 2: Create OAuth Credentials

### Configure OAuth Consent Screen

1. Go to "APIs & Services" → "OAuth consent screen"
2. Choose "External" (for personal use)
3. Click "Create"
4. Fill in:
   - App name: "Friday AI"
   - User support email: Your email
   - Developer contact: Your email
5. Click "Save and Continue"
6. Scopes: Skip (click "Save and Continue")
7. Test users: Add your email
8. Click "Save and Continue"

### Create Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. Application type: "Desktop app"
4. Name: "Friday Desktop Client"
5. Click "Create"
6. Click "Download JSON"

## Step 3: Install Credentials

### Save credentials file:

```bash
# Create credentials directory
mkdir "%USERPROFILE%\OneDrive\Desktop\Code Hub\Pro Friday\credentials"

# Move downloaded file
move "%USERPROFILE%\Downloads\client_secret_*.json" "%USERPROFILE%\OneDrive\Desktop\Code Hub\Pro Friday\credentials\gmail_credentials.json"
```

## Step 4: Install Dependencies

```bash
cd "%USERPROFILE%\OneDrive\Desktop\Code Hub\Pro Friday"

# Install Gmail API libraries
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

# Install PDF support
pip install PyPDF2
```

## Step 5: First Run Authorization

```bash
# Start Friday
python run.py

# Say: "Friday, check my emails"
# Browser will open for authorization
# Login with your Google account
# Click "Allow"
# Token saved to ~/.friday/gmail_token.pickle
```

## Security

- ✅ OAuth (no passwords stored)
- ✅ Token stored locally (~/.friday/)
- ✅ Scopes: read, modify, compose only
- ✅ Revoke access anytime: https://myaccount.google.com/permissions

## Troubleshooting

### "Credentials not found"

- Ensure `gmail_credentials.json` is in `credentials/` folder

### "Access denied"

- Check OAuth consent screen settings
- Add your email as test user

### "Token expired"

- Delete `~/.friday/gmail_token.pickle`
- Re-authorize

## Usage Commands

```
"Friday, check my emails"
→ Lists recent unread emails

"Friday, summarize important emails"
→ AI identifies and summarizes

"Friday, draft a reply saying thanks"
→ Creates draft in Gmail

"Friday, read this PDF"
→ Extracts text from PDF
```

## Done! 🚀

Friday can now manage your emails intelligently!
