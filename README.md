# mycase-scraper

mycase-scraper is a Python tools for getting case data.

## Installation

Use git to clone

```bash
git clone git@github.com:indy-tenants/mycase-scraper.git
```

## Setup

You'll need to configure an .env if you want to send the data to 

```env
# Select persistance strategy, options are [SUPABASE, SQLITE (default), GOOGLE_SHEETS]
PERSISTENCE_STRATEGY=SUPABASE

# Configuration for google
GOOGLE_SERVICE_ACCOUNT_PATH=/path/to/service_account.json
GOOGLE_SPREADSHEETS_ID=<spreadsheet_id_from_url>
PRIMARY_SHEET_NAME=primary
ARCHIVE_SHEET_NAME=archive

# Configuration for Supabase
SUPABASE_URL=<https://example.supabase.co>
SUPABASE_KEY=<secret_key>
SUPABASE_SERVICE_ROLE_SECRET=<service_role_secret>

# Selenium options
CHROME_HEADLESS=False
```

## Usage

```bash
$ mycase-scraper --court 49K01 --month 3 --year 2020 
```

## License
[MIT](https://choosealicense.com/licenses/mit/)