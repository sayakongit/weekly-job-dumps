from urllib.parse import urlencode
from .constants import NAUKRI_JOB_DETAILS_HEADERS, NAUKRI_ALL_JOBS_HEADERS, MONSTER_API_HEADERS, MONSTER_PAYLOAD, MONSTER_JOB_SEARCH_ENDPOINT
import requests
import re

def cleanhtml(raw_html):
    CLEANR = re.compile('<.*?>')
    cleantext = re.sub(CLEANR, '', raw_html)
    return cleantext

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
            data['skills'] = job['tagsAndSkills'].split(',')
            
            for placeholder in job['placeholders']:
                if placeholder['type'] == 'experience':
                    data['experience'] = placeholder['label']
                if placeholder['type'] == 'salary':
                    data['salary'] = placeholder['label']
                if placeholder['type'] == 'location':
                    data['location'] = placeholder['label']
                    
            data['jd_url'] = 'www.naukri.com' + job['jdURL']
            data['job_highlights'] = cleanhtml(job['jobDescription'])
            data['time_created'] = job['footerPlaceholderLabel']
            try:
                data['review_count'] = job['ambitionBoxData']['ReviewsCount']
                data['ratings'] = job['ambitionBoxData']['AggregateRating']
            except:
                data['review_count'] = ''
                data['ratings'] = ''
            all_jobs.append(data)

        return all_jobs
    return {'error': 'No data found'}
    
    
def foundit_search_by_keyword(keyword, location, sort_by):
    url = MONSTER_JOB_SEARCH_ENDPOINT
    MONSTER_PAYLOAD['query'] = keyword
    
    print('SORT', sort_by)
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

                    data['review_count'] = ''
                    data['ratings'] = ''
                    
                    jobs.append(data)
        else:
            return {'error': 'No data found'}
    except Exception as e:
        print(e)
        return {'error': 'Error'}
    return jobs