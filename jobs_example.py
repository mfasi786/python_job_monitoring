# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 21:08:38 2021

@author: Back4
"""

import json
import os.path
import datetime
import requests

from jobs_log_settings import custom_logger

myJsonFile = open('jobs_JSON.json')

JOB_NAMES = ["CE_BATCH", "CE_RECON_BATCH", "CE_MTRS_FL", "CE_MTRS_RCRP", "CE_ACHP_BATCH"]
CE_BATCH_DAYS = []
CE_BATCH_TIME = ''
CE_BATCH_DIR = ''

today = datetime.datetime.now()

json_dict = json.load(myJsonFile)
myJsonFile.close()

custom_logger.info('')
custom_logger.info('*********************************************************************')
custom_logger.info('')

for i in json_dict['mminds_jobs']:

    job_dict = i

    custom_logger.info(i['job_name'])
    custom_logger.info(i['job_name'] in JOB_NAMES)

    if(i['job_name'] in JOB_NAMES):
        CE_BATCH_DAYS = i["days_of_week"]
        CE_BATCH_TIME = i["start_time"]
        CE_BATCH_DIR = i["directory"]
        HOLIDAY_DATES = i["holidays"]
        dirCreated = os.path.isdir(CE_BATCH_DIR+today.strftime("%Y%m%d")) 
        
        if(today.strftime("%A") in CE_BATCH_DAYS):
            custom_logger.info(f"{i['job_name']} IS EXPECTED TO RUN TODAY")

            if(today.strftime("%Y-%m-%d") not in HOLIDAY_DATES):

                custom_logger.info('Current day is NOT a holiday')
                custom_logger.info(f"Is current time {today.strftime('%H.%M')} greater than expected time {CE_BATCH_TIME} for the batch {i['job_name']} - {today.strftime('%H.%M')>CE_BATCH_TIME}")

                if(today.strftime("%H.%M")>CE_BATCH_TIME):
                    if(dirCreated):
                        custom_logger.info("Directory exists, job started already, no action required")
                    else:
                        custom_logger.info(f"Directory exists? - {dirCreated}")
                        custom_logger.info('!!! Immediate Action Required  !!!')
                        custom_logger.info('!!! Initiating X-Matters Alert !!!')
                        jsonRequest = requests.post('https://reqbin.com/echo/post/json', data={"login":"my_login","password":"my_password"})
                        custom_logger.info(f" MS Response is - {jsonRequest.text}")
                        jsonResponse = jsonRequest.json()

                        if(jsonResponse['success']):
                            custom_logger.info(f"Successfully sent the X-Matters Alert for the job {i['job_name']} at {today.strftime('%H.%M')}") 
                else:
                    custom_logger.info(f"Not the time for {i['job_name']} to run yet - No action required currently")

    custom_logger.info('')
    custom_logger.info('*********************************************************************')
    custom_logger.info('')
