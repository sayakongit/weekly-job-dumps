from jobs_updater.celery import app
from .launcher import run_naukri_scrapper, run_foundit_scrapper
from celery import shared_task

@app.task
def naukri_scrapper_automation():
    run_naukri_scrapper()

@app.task
def foundit_scrapper_automation():
    run_foundit_scrapper()
    
@shared_task(bind=True)
def test_func(self):
    print('Under shared task')
    return "Done"