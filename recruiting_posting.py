#!/usr/bin/env python
import boto3
import time

mturk = boto3.client('mturk',region_name = 'us-east-1') 
# For MTurk sandbox instead
# mturk = boto3.client('mturk',region_name = 'us-east-1',endpoint_url='https://mturk-requester-sandbox.us-east-1.amazonaws.com') 

#################################################################################################################################################################################################################################
# Create Qualification HIT
#################################################################################################################################################################################################################################

questions = open(file='question_answer/test.xml', mode='r').read()
answers = open(file='question_answer/answer.xml', mode='r').read()

qual_response = mturk.create_qualification_type(Name="Qualification_NAME",Keywords="",Description="", QualificationTypeStatus="Active", AutoGranted=False)
print(qual_response['QualificationType']['QualificationTypeId']) 
new_qual_id = qual_response['QualificationType']['QualificationTypeId']

workers_with_qual = mturk.list_workers_with_qualification_type(QualificationTypeId=new_qual_id,MaxResults=100)['Qualifications']
num_workers_with_qual = len(workers_with_qual)

#################################################################################################################################################################################################################################
# Posting Recruiting HITS
#################################################################################################################################################################################################################################

group_assignment = 0
time_for_hit = 8

while num_workers_with_qual <= 50:
    print(num_workers_with_qual)
    post_expiration_time = time.time()+time_for_hit*60
    reward = '0.05'
    hit = mturk.create_hit(
            Reward=reward,
            LifetimeInSeconds=time_for_hit*60,
            AssignmentDurationInSeconds=200,
            MaxAssignments=15,
            Title='RecruitingHIT',
            Question=questions,
            Description='Recruiting HIT',
            Keywords='boto, qualification, test',
            AutoApprovalDelayInSeconds=1,
            QualificationRequirements=[{'QualificationTypeId': '3J9ZK359J5FEO93SM3BO82G1FM813O', 'Comparator': 'DoesNotExist', 'ActionsGuarded': "DiscoverPreviewAndAccept"}, 
                                       {'QualificationTypeId': new_qual_id, 'Comparator': 'DoesNotExist', 'ActionsGuarded': "DiscoverPreviewAndAccept"}]
            )
    hitid = hit['HIT']['HITId']
    while (time.time()<post_expiration_time):
        time.sleep(1)
        num_assignments = len(mturk.list_assignments_for_hit(HITId=hitid, MaxResults=100)['Assignments'])
        correct_answer = "iwltp_100"
        workers_with_qual = []
        num_workers_with_qual = len(mturk.list_workers_with_qualification_type(QualificationTypeId=new_qual_id,MaxResults=100)['Qualifications'])
        for j in range(0, num_workers_with_qual):
            workers_with_qual.append(mturk.list_workers_with_qualification_type(QualificationTypeId=new_qual_id,MaxResults=100)['Qualifications'][j]['WorkerId'])
        for j in range(0,num_assignments):
            cur_worker_id = mturk.list_assignments_for_hit(HITId=hitid, MaxResults=100)['Assignments'][j]['WorkerId']
            if (correct_answer in mturk.list_assignments_for_hit(HITId=hitid, MaxResults=100)['Assignments'][j]['Answer']) and (cur_worker_id not in workers_with_qual):
                group_assignment = (group_assignment) % 4 + 1
                mturk.associate_qualification_with_worker(QualificationTypeId=new_qual_id, WorkerId=cur_worker_id, IntegerValue=group_assignment, SendNotification=True)

