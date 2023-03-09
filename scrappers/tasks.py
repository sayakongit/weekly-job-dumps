from jobs_updater.celery import app
from .launcher import run_naukri_scrapper, run_foundit_scrapper

@app.task
def naukri_scrapper_automation():
    run_naukri_scrapper()

@app.task
def foundit_scrapper_automation():
    run_foundit_scrapper()