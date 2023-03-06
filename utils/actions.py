import gspread
from oauth2client.service_account import ServiceAccountCredentials
from .constants import creds_file_location, scope

def read_sheet_data(sheet_name, tab_name):
    """
    This function returns data present in sheet and sheet instance.
    """
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file_location, scope)

    client = gspread.authorize(creds)

    sheet = client.open(sheet_name).worksheet(tab_name)
    data = sheet.get_all_records()

    return data, sheet

def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return len(str_list)+1