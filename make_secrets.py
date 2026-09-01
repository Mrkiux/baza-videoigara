import json
from pathlib import Path

json_file = Path("service-account.json")
secrets_file = Path(".streamlit/secrets.toml")

with open(json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

sheet_url = input("https://docs.google.com/spreadsheets/d/1-oW_HaLu0b9D3ABJRMhlmu5hJBY_bI0rK2L4AurJaa4/edit?gid=0#gid=0 ").strip()

toml = f'''[connections.gsheets]
spreadsheet = {json.dumps(sheet_url)}
worksheet = "Sheet1"
type = "service_account"
project_id = {json.dumps(data["project_id"])}
private_key_id = {json.dumps(data["private_key_id"])}
private_key = {json.dumps(data["private_key"])}
client_email = {json.dumps(data["client_email"])}
client_id = {json.dumps(data["client_id"])}
auth_uri = {json.dumps(data["auth_uri"])}
token_uri = {json.dumps(data["token_uri"])}
auth_provider_x509_cert_url = {json.dumps(data["auth_provider_x509_cert_url"])}
client_x509_cert_url = {json.dumps(data["client_x509_cert_url"])}
universe_domain = {json.dumps(data.get("universe_domain", "googleapis.com"))}
'''

secrets_file.parent.mkdir(exist_ok=True)
secrets_file.write_text(toml, encoding="utf-8")

print("secrets.toml je uspjesno napravljen!")