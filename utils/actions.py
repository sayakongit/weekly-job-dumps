import gspread
from oauth2client.service_account import ServiceAccountCredentials
from .constants import creds_file_location, scope
from gspread import Cell

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

def insert_data_row(sheet, data_to_write):
    headers = sheet.row_values(1)
    master_data = []
    for data in data_to_write:
        row_data = []
        for header in headers:
            try:
                row_data.append(data[header.lower()])
            except KeyError as k:
                row_data.append('')
        master_data.append(row_data)
    sheet.append_rows(master_data)
    return True

def add_headers(sheet, headers):
    row = 1
    col = 1
    
    cells = []
    for header in headers:
        cells.append(Cell(row=row, col=col, value=header.upper()))
        col += 1
    sheet.update_cells(cells)