import json
import gspread

# Učitaj Service Account
with open("service-account.json", "r", encoding="utf-8") as f:
    credentials = json.load(f)

print("Service Account:", credentials["client_email"])

# Prijava
gc = gspread.service_account(filename="service-account.json")

# URL tvog Google Sheeta
url = input("Zalijepi URL Google Sheeta: ").strip()

print("\nPokušavam otvoriti Google Sheet...")

try:
    spreadsheet = gc.open_by_url(url)

    print("✅ GOOGLE SHEET JE OTVOREN!")
    print("Naziv:", spreadsheet.title)

    worksheet = spreadsheet.worksheet("Sheet1")

    print("✅ SHEET1 JE OTVOREN!")
    print("Broj redova:", len(worksheet.get_all_values()))

except Exception as e:
    print("❌ GREŠKA:")
    print(type(e).__name__)
    print(e)