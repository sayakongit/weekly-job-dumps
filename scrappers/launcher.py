from .actions import naukri_search_by_keyword, foundit_search_by_keyword
from utils.actions import read_sheet_data, insert_data_row
from .constants import KEYWORD, LOCATION, SORT_BY, SHEET_NAME, NAUKRI_TAB, MONSTER_TAB

def run_naukri_scrapper():
    try:
        jobs = naukri_search_by_keyword(KEYWORD, LOCATION, SORT_BY)
        data, sheet = read_sheet_data(SHEET_NAME, NAUKRI_TAB)
        insert_data_row(sheet, jobs)
    except Exception as e:
        print(f'Error in Naurki search automation --> {e}')

def run_foundit_scrapper():
    try:
        jobs = foundit_search_by_keyword(KEYWORD, LOCATION, SORT_BY)
        data, sheet = read_sheet_data(SHEET_NAME, MONSTER_TAB)
        insert_data_row(sheet, jobs)
    except Exception as e:
        print(f'Error in Monster search automation --> {e}')