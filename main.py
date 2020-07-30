import requests
import pprint
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
               "get_devs": "dataservice/device"}

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

# if the response is 200 OK, print the output as a json output
if device_resp.ok:
        devices = device_resp.json()["data"]
        print(json.dumps(devices, indent=2))