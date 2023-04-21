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
        
def clean_number(number):
    new = number.translate({ord(i): None for i in '() -+'})
    return new

def is_indian(number):
    if len(number) > 10:
        return False
    Pattern = re.compile("(0|91)?[6-9][0-9]{9}")
    return Pattern.match(number)
        

        
def banking():
    o_data, o_sheet = read_sheet_data('Employer Database KK', 'Banking and Insurance')
    n_data, n_sheet = read_sheet_data('Employer DB', 'Banking and Insurance')

    headers = [
        'client_first_name',
        'client_middle_name',
        'client_last_name',
        'client_email',
        'client_email_second',
        'client_mobile_number',
        'client_phone_number',
        'client_recorded_line',
        'client_linkedin',
        'job_title',
        'company_name',
        'client_role_short',
        'client_role',
        'client_role_type',
        'client_city',
        'client_state',
        'client_country'
    ]
    
    n_sheet.clear()
    col = 1
    cells = []
    for header in headers:
        cells.append(Cell(row=1, col=col, value=header))
        col += 1
        
    n_sheet.update_cells(cells)
    
    data = []
    
    for d in o_data:
        number = clean_number(str(d['client_phone_number']))
        if is_indian(number):
            # print(number)
            temp = {
                'client_first_name': d['client_first_name'],
                'client_middle_name': d['client_middle_name'],
                'client_last_name': d['client_last_name'],
                'client_email': d['client_email'],
                'client_email_second': d['client_email_second'],
                'client_mobile_number': clean_number(d['client_mobile_number']),
                'client_phone_number': number if len(number) > 10 else f'91{number}',
                'client_recorded_line': f'91{clean_number(d["client_recorded_line"])}' if clean_number(d["client_recorded_line"]) != '' else '',
                'client_linkedin': d['client_linkedin'],
                'job_title': d['job_title'],
                'company_name': d['company_name'],
                'client_role_short': d['client_role_short'],
                'client_role': d['client_role'],
                'client_role_type': d['client_role_type'],
                'client_city': d['client_city'],
                'client_state': d['client_state'],
                'client_country': d['client_country'],
            
            }
            data.append(temp)
            
    insert_data_row(n_sheet, data)
    
def pharma():
    tab_name = 'Retail'
    o_data, o_sheet = read_sheet_data('Employer Database KK', tab_name)
    n_data, n_sheet = read_sheet_data('Employer DB', tab_name)
    
    headers = [
        'client_first_name',
        'client_middle_name',
        'client_last_name',
        'client_email',
        'client_email_second',
        'client_mobile_number',
        'client_phone_number',
        'client_recorded_line',
        'client_linkedin',
        'job_title',
        'company_name',
        'client_role_short',
        'client_role',
        'client_role_type',
        'client_city',
        'client_state',
        'client_country'
    ]
    
    n_sheet.clear()
    col = 1
    cells = []
    for header in headers:
        cells.append(Cell(row=1, col=col, value=header))
        col += 1
        
    n_sheet.update_cells(cells)
    
    data = []
    
    for d in o_data:
        number = clean_number(str(d['phone']))
        if is_indian(number):
            # print(number)
            area = d['city'].split(",")
            city = state = country = ''
            if len(area) == 3:
                city, state, country = area
            elif len(area) == 2:
                state, country = area
            elif len(area) == 1:
                country = area[0]
            temp = {
                'client_first_name': d['first_name'],
                'client_middle_name': d['middle_name'],
                'client_last_name': d['last_name'],
                'client_email': d['email_first'],
                'client_email_second': d['email_second'],
                'client_mobile_number': '',
                'client_phone_number': number if len(number) > 10 else f'91{number}',
                'client_recorded_line': f'91{clean_number(d["company_phone"])}' if clean_number(d["company_phone"]) != '' else '',
                'client_linkedin': d['url'],
                'job_title': d['job_title'],
                'company_name': d['company_name'],
                'client_role_short': f"{d['job_title']} @ {d['company_name']}",
                'client_role': f"{d['job_title']} @ {d['company_name']}",
                'client_role_type': '',
                'client_city': city,
                'client_state': state,
                'client_country': country,
            
            }
            data.append(temp)
            
    insert_data_row(n_sheet, data)
    