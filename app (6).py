import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

SHEET_NAME = "EasyReply_Users"

def connect_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("gspread_service_account.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open(SHEET_NAME).sheet1
    return sheet

def fetch_users():
    sheet = connect_sheet()
    data = sheet.get_all_records()
    return pd.DataFrame(data)

def update_credits(email, new_credits):
    sheet = connect_sheet()
    users = sheet.get_all_records()
    for i, user in enumerate(users):
        if user["Email"] == email:
            sheet.update_cell(i + 2, 4, new_credits)  # row + 1 (header), col 4 = Credits
            break
