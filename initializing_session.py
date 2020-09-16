#!/usr/bin/env python
import boto3
import time
import requests

mturk = boto3.client('mturk',region_name = 'us-east-1')
# For Sandbox instead
# mturk = boto3.client('mturk',region_name = 'us-east-1',endpoint_url='https://mturk-requester-sandbox.us-east-1.amazonaws.com')

#################################################################################################################################################################################################################################
# Initializing Session in MTurk via REST API
#################################################################################################################################################################################################################################

SERVER_URL = 'https://yourapp.herokuapp.com'
REST_KEY = 'your_key' # See https://otree.readthedocs.io/en/latest/misc/rest_api.html

def csess(**payload):
    return requests.post(SERVER_URL + '/api/v1/sessions/', json=payload,
        headers={'otree-rest-key': REST_KEY}
    )

mturk_hit_settings_out1 = {
    'keywords': ['bonus', 'choice', 'study'],
    'title': 'MExpK',
    'description': '',
    'frame_height': 500,
    'template': 'global/mturk_template.html',
    'minutes_allotted_per_assignment': 60,
    'expiration_hours': 2,  # 7 days
    'grant_qualification_id': 'YOUR_RETAKE_BLOCKER_QUALIFICATION_ID',# to prevent retakes
    'qualification_requirements': [
        {
            'QualificationTypeId': "YOUR_RETAKE_BLOCKER_QUALIFICATION_ID",
            'Comparator': "DoesNotExist",
            'ActionsGuarded': "DiscoverPreviewAndAccept"
        },
        {
            'QualificationTypeId': new_qual_id,
            'Comparator': "EqualTo",
            'IntegerValues': [2],
            'ActionsGuarded': "DiscoverPreviewAndAccept"
        },
    ]
}
resp = csess(session_config_name='TREATMENT_NAME', num_participants=40, is_mturk=True, modified_session_config_fields = dict(mturk_hit_settings=mturk_hit_settings_out1))
print(resp.text) # returns the session code
