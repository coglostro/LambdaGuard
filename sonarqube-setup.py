"""
asdf
Copyright 2020 Skyscanner Ltd

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
import requests 
import json
from time import sleep
from sys import stdout

curl = requests.Session()
curl.auth = ('admin', 'admin')

API = 'http://localhost:9000'

# Wait for SQ to start
stdout.write('Waiting for SonarQube to start')
stdout.flush()
while True:
    try:
        ret = curl.get(f'{API}/api/system/status')
        assert ret.status_code == 200
        assert '"status":"UP"' in ret.text
        break
    except:
        stdout.write('.')
        stdout.flush()
        sleep(3)

# Configure SQ instance
print('\nConfiguring SonarQube')
for language in ['py', 'js', 'java']:
    try:
        profile = json.loads(
            curl.post(f'{API}/api/qualityprofiles/create', data={
                'language': language,
                'name': 'lambdaguard'
            }).text
        )['profile']
        curl.post(f'{API}/api/qualityprofiles/set_default', data={
            'key': profile['key']
        })
        curl.post(f'{API}/api/qualityprofiles/activate_rules', data={
            'targetKey': profile['key'],
            'types': 'VULNERABILITY,BUG',
            'severities': 'CRITICAL,BLOCKER'
        })
    except:
        continue
