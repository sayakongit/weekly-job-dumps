from .actions import naukri_search_by_keyword, foundit_search_by_keyword
from utils.actions import read_sheet_data, insert_data_row, add_headers
from .constants import KEYWORD, LOCATION, SORT_BY, SHEET_NAME, NAUKRI_TAB, MONSTER_TAB, HEADERS

def run_naukri_scrapper():
    try:
        jobs_one = naukri_search_by_keyword(KEYWORD, LOCATION, SORT_BY, "1")
        jobs_two = naukri_search_by_keyword(KEYWORD, LOCATION, SORT_BY, "2")
        jobs = jobs_one + jobs_two
        data, sheet = read_sheet_data(SHEET_NAME, NAUKRI_TAB)
        sheet.clear()
        add_headers(sheet, HEADERS)
        insert_data_row(sheet, jobs)
    except Exception as e:
        print(f'Error in Naurki search automation --> {e}')

def run_foundit_scrapper():
    try:
        jobs = foundit_search_by_keyword(KEYWORD, LOCATION, SORT_BY)
        data, sheet = read_sheet_data(SHEET_NAME, MONSTER_TAB)
        sheet.clear()
        add_headers(sheet, HEADERS)
        insert_data_row(sheet, jobs)
    except Exception as e:
        print(f'Error in Monster search automation --> {e}')