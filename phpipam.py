import requests
import json
import pprint

# server = "http://172.17.74.64/"
# app_id = "123"
# username = "admin"
# password = ""
#
# baseurl = server + "/api/" + app_id
#
# res = requests.post(baseurl + '/user/', auth=(username, password))
# print(res.status_code)
# print(res.content)
# token = json.loads(res.content)['data']['token']
#
# res = requests.get(baseurl + '/sections/', headers={'token': token})
# print(res.status_code)
# print(res.content)
#
# res = requests.get(baseurl + '/sections/3/subnets/', headers={'token': token})
# print(res.status_code)
# print(res.content)
# url = 'http://172.17.74.64/'
# r = requests.post('http://api/172.17.74.64/admin/')
# print(r.status_code)

url = 'http://172.17.74.64/index.php?page=administration&section=api'
headers = {
  'Authorization': 'dJxA-42FQJTfx8f_u8uk4m_dhju_VfRD',
}
result = requests.post(url=url, headers=headers)
print(result.status_code)
pprint.pprint(result.text)
