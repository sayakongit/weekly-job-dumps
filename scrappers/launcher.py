from .actions import naukri_search_by_keyword, foundit_search_by_keyword
from utils.actions import read_sheet_data

def run_naukri_scrapper():
    jobs = naukri_search_by_keyword(keyword, location, sort_by)
    read_sheet_data(sheet_name, tab_name)
