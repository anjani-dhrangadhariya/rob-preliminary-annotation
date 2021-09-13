import requests,json
from requests import get
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
import urllib
import itertools
from collections import defaultdict

def get_combinations(l):
    yield from itertools.product(l, l)

project_name = 'RoB_preliminary_annotation'
owner = 'anjDhr'
users = ['rahel-caliesch', 'roger-annotation', 'martin-annotation', 'katia-giacomino', 'simone-annotation']
all_user_combinations = list(itertools.combinations(users, 2)) 
all_user_combinations = get_combinations(users)
all_user_combinations = list( all_user_combinations )

'''
exact_v1 = Stringent inter-annotator agreement
overlapping_v1 = Relaxed inter-annotator agreement
'''
metrics = ['exact_v1', 'overlapping_v1'] 


# Get all the entities
all_annotations_data = 'https://www.tagtog.net/-api/metrics/v0/search_stats?project=RoB_preliminary_annotation&owner=anjDhr&search=*'
all_annotations_data_response = get(all_annotations_data, auth=('anjDhr', '9J@NiScMhUy9LbR'))
print('The response for query is: ', all_annotations_data_response)
all_annotations_data_response = json.loads(all_annotations_data_response.text)


# Get the IAA metrics
# IAA_hardcoded = 'https://www.tagtog.net/-api/metrics/v0/iaa?project=RoB_preliminary_annotation&owner=anjDhr&member1=rahel-caliesch&member2=roger-annotation&anntaskId=e_109&metric=exact_v1'
IAA = 'https://www.tagtog.net/-api/metrics/v0/iaa?'

user_agreement = dict() # what users have constant high agreement (relaxed agreement) between entities

for eachEntry in all_annotations_data_response:
    
    if 'e_' in eachEntry:

        entry_name =  all_annotations_data_response[eachEntry]['name']
        entity_IAA = {}

        for eachUserPair in all_user_combinations:

            member1 = eachUserPair[0]
            member2 = eachUserPair[1]

            if member1 != member2:

                params = (('project',project_name),('owner', owner), ('member1', member1), ('member2', member2), ('anntaskId', eachEntry), ('metric', metrics[1])) # metrics[1] = overlapping_v1
                parameters = urllib.parse.urlencode(params)
                entire_command = IAA + parameters
                response = get(entire_command, auth=('anjDhr', '9J@NiScMhUy9LbR'))
                my_json_data = json.loads(response.text)

                if eachUserPair not in entity_IAA and tuple(reversed(eachUserPair)) not in entity_IAA:
                    entity_IAA[eachUserPair] = my_json_data['f1']

        print( entry_name )

        for (mem1, mem2), value in entity_IAA.items():
            if str((mem1, mem2)) not in user_agreement:
                user_agreement[(mem1, mem2)] = [value]
            elif str((mem1, mem2)) in user_agreement:
                user_agreement[(mem1, mem2)].append(value)

        print('--------------------------------------------------------------------')