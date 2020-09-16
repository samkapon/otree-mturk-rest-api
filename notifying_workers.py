#!/usr/bin/env python
import boto3

mturk = boto3.client('mturk',region_name = 'us-east-1') 
# For Sandbox instead
# mturk = boto3.client('mturk',region_name = 'us-east-1',endpoint_url='https://mturk-requester-sandbox.us-east-1.amazonaws.com') 

new_qual_id = 'YOUR_QUALIFICATION_ID'

#################################################################################################################################################################################################################################
### Notifying workers
#################################################################################################################################################################################################################################
workers_with_qual = mturk.list_workers_with_qualification_type(QualificationTypeId=new_qual_id,MaxResults=100)['Qualifications']
num_workers = len(workers_with_qual)
worker_ids = []
for j in range(0,num_workers):
    worker_ids.append(workers_with_qual[j]['WorkerId'])

mturk.notify_workers(Subject='Interactive HIT - 10 Minutes!', MessageText='The HIT titled HIT_TITLE will be posted at X PM.', WorkerIds=worker_ids)
