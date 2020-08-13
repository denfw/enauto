import requests
import tabulate
import json

# stop warnings that come from accepting self signed SSL certificates
requests.packages.urllib3.disable_warnings()

# device information
device = {"address": "sandboxsdwan.cisco.com",
	      "port": "8443",
          "user": "devnetuser",
          "pass": "C1sco123!"}

# api calls 
sd_wan_apis = {"login": "j_security_check",
               "get_devs": "dataservice/device",
               "get_templates": "dataservice/template/device"}

# login credentials - specifically for auth on vManage
login_creds = {"j_username": "devnetuser", "j_password": "Cisco123!"}

# header information - what to accept
headers = {"Accept": "application/yang-data+json"}

# the url - formatted using the {} 
u = "https://{}:{}/{}"

u1 = u.format(device["address"], device["port"] ,sd_wan_apis["login"])

# create TCP session, so that you won't have to pass cookies around
sess = requests.session()
login = sess.post(u1,
		     headers = headers, 
             data=login_creds,
		     verify=False)

# simply check if the login is ok or not - if the response code is 200OK or the reponse has a lot of text = no login
if not login.ok or login.text:
    print("Login failed")
    import sys
    sys.exit(1)

# get list of devices in the overlay
u2 = u.format(device["address"], device["port"], sd_wan_apis["get_devs"])

# use the existing session to get list
device_resp = sess.get(u2, verify=False)

# # if the response is 200 OK, print the output as a json output
# if device_resp.ok:
#         devices = device_resp.json()["data"]
#         print(json.dumps(devices, indent=2))

# store response as json object
json_response = json.loads(device_resp.text)
items = json_response['data']

# create table headers for tabulate to print out
device_headers = ["Host-Name", "Device-type", "Device ID", "System IP", "Site ID", "Version", "Device Model"]

# create initial table
table = []

# iterate through json object and find specific items then append them to the table
for i in items:
    tr = [ i["host-name"], i["uuid"], i["system-ip"], i["site-id"], i["version"], i["device-model"]]
    table.append(tr)

# print out the appended table using tabulate
print(tabulate.tabulate(table, device_headers, tablefmt='fancygrid'))

# format url to get list of templates
u3 = u.format(device["address"], device["port"], sd_wan_apis["get_templates"])

# use the existing session to get list
device_templates = sess.get(u3, verify=False)

template_response = json.loads(device_templates.text)
templates = template_response['data']
template_headers = ["Device-type", "Template Name", "Devices Attached", "Template Description", "Template ID"]

for i in templates:
    tr = [ i["deviceType"], i["templateName"], i["devicesAttached"], i["templateDescription"], i["templateId"]]
    table.append(tr)

print(tabulate.tabulate(table, template_headers, tablefmt='fancygrid'))
