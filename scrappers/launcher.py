from .actions import naukri_search_by_keyword, foundit_search_by_keyword
from utils.actions import read_sheet_data, insert_data_row
from .constants import KEYWORD, LOCATION, SORT_BY

def run_naukri_scrapper():
    jobs = naukri_search_by_keyword(KEYWORD, LOCATION, SORT_BY)
    data, sheet = read_sheet_data(sheet_name, tab_name)
    insert_data_row(sheet, jobs)

def run_foundit_scrapper():
    jobs = foundit_search_by_keyword(KEYWORD, LOCATION, SORT_BY)
    data, sheet = read_sheet_data(sheet_name, tab_name)
    insert_data_row(sheet, jobs)
    
    
