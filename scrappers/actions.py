from urllib.parse import urlencode
from .constants import NAUKRI_JOB_DETAILS_HEADERS, NAUKRI_ALL_JOBS_HEADERS, MONSTER_API_HEADERS, MONSTER_PAYLOAD, MONSTER_JOB_SEARCH_ENDPOINT, MONSTER_JOB_DETAILS_ENDPOINT
import requests
import re

def cleanhtml(raw_html):
    CLEANR = re.compile('<.*?>')
    cleantext = re.sub(CLEANR, '', raw_html)
    return cleantext

def foundit_search_by_id(job_id):
    url = MONSTER_JOB_DETAILS_ENDPOINT + str(job_id)
    
    try:
        search_details = requests.get(url, headers=MONSTER_API_HEADERS).json()
    except Exception as e:
        print(e)
        return {'error': 'Could not fetch data'}
    
    return search_details['jobDetailResponse']

def naukri_search_by_id(job_id):
    url = "https://www.naukri.com/jobapi/v4/job/" + job_id
    
    response = requests.get(url, headers=NAUKRI_JOB_DETAILS_HEADERS)
    data = {}
    status = response.status_code
    search_details = response.json()

    return search_details['jobDetails']

def naukri_search_by_keyword(keyword, location, sort_by):
    url = "https://www.naukri.com/jobapi/v3/search?"
    payload = {
        "urlType": "search_by_keyword",
        "searchType": "adv",
        "keyword": keyword,
        "location": location,
        "sort": sort_by,
        "noOfResults": 100
    }
    
    response = requests.get(url, params=urlencode(payload),  headers=NAUKRI_ALL_JOBS_HEADERS)
    search_results = response.json()
    status = response.status_code
    all_jobs = []
    if status == 200 and 'jobDetails' in search_results:
        for job in search_results['jobDetails']:
            data = {}
            data['title'] = job['title']
            data['company_name'] = job['companyName']
            
            for placeholder in job['placeholders']:
                if placeholder['type'] == 'experience':
                    data['experience'] = placeholder['label']
                if placeholder['type'] == 'salary':
                    data['salary'] = placeholder['label']
                if placeholder['type'] == 'location':
                    data['location'] = placeholder['label']
                    
            data['time_created'] = job['footerPlaceholderLabel']
            try:
                data['review_count'] = job['ambitionBoxData']['ReviewsCount']
                data['ratings'] = job['ambitionBoxData']['AggregateRating']
            except:
                data['review_count'] = 'NA'
                data['ratings'] = 'NA'
                
            try:
                job_details = naukri_search_by_id(job['jobId'])
                data['industry'] = job_details['roleCategory']
            except:
                data['industry'] = 'NA'
                
            data['posted_by'] = 'NA'
            all_jobs.append(data)

        return all_jobs
    return {'error': 'No data found'}
    
    
def foundit_search_by_keyword(keyword, location, sort_by):
    url = MONSTER_JOB_SEARCH_ENDPOINT
    MONSTER_PAYLOAD['query'] = keyword
    
    if location != '':
        MONSTER_PAYLOAD['locations'] = location
    if sort_by != '':
        MONSTER_PAYLOAD['sort'] = "2"
    
    try:
        search_results = requests.get(url, params=urlencode(MONSTER_PAYLOAD),  headers=MONSTER_API_HEADERS).json()
    except Exception as e:
        print(e)
        return {'error': 'Could not fetch data'}
    
    jobs = []
    try:
        if search_results['jobSearchStatus'] == 200 and len(search_results['jobSearchResponse']['data']) > 0:

            for job in search_results['jobSearchResponse']['data']:
                if len(job) > 3:
                    data = {}
                    data['title'] = job['title']
                    data['company_name'] = job['companyName']
                    try:
                        data['skills'] = job['skills'].split(',')
                    except:
                        data['skills'] = []
                    
                    data['experience'] = job['exp'] if job['exp'] != '' else 'Not disclosed'
                    data['salary'] = job['salary'] if job['salary'] != '' else 'Not disclosed'
                    data['location'] = job['locations']
                            
                    data['time_created'] = job['postedBy']

                    data['review_count'] = 'NA'
                    data['ratings'] = 'NA'
                
                    
                    try:
                        job_details = foundit_search_by_id(job['jobId'])
                        data['industry'] = ",".join(job_details['industries'])
                    except:
                        data['industry'] = 'NA'
                        
                    data['posted_by'] = 'NA'
                    
                    
                    jobs.append(data)
        else:
            return {'error': 'No data found'}
    except Exception as e:
        print(e)
        return {'error': 'Error'}
    return jobs
    
    
    