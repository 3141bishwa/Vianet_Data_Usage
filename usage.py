import requests
from os import path
import time
import pandas as pd
import config

post_data = config.post_data

url ="https://customers.vianet.com.np"
session_requests = requests.session()


# Connection must be made to Vianet in order to make POST request for usage data.
login = path.join(url, "customers/login")
result = session_requests.get(login)
result = session_requests.post(
	login, 
	data = post_data, 
	headers = dict(referer=login)
)

new_url = path.join("https://customers.vianet.com.np/services/consumer_broadband/get/graph/token",post_data['service_id'])

#Converting cookie dict to String for POST request
cookies = "; ".join([str(x)+"="+str(y) for x,y in session_requests.cookies.items()])

header_info = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Content-Length': '16',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': cookies,
    'DNT': '1',
    'Host': 'customers.vianet.com.np',
    'Origin': 'https://customers.vianet.com.np',
    'Referer': path.join("https://customers.vianet.com.np/services/consumer_broadband/detail",post_data['service_id']),
    'X-Requested-With': 'XMLHttpRequest'
}

payload= {'usageType' : '_daily'}

result = session_requests.post(
	new_url,
    data = payload,
	headers = header_info
)

data = result.json()['data']    

df = pd.DataFrame([[x['t']/1000, "{0:.2f} MB".format(float(x['download']/1024.0)), "{0:.2f} MB".format(float(x['upload']/1024.0))] for x in data])
# df = pd.DataFrame([[time.strftime("%b-%d %H:%M", time.localtime(x['t']/1000)), "{0:.2f} MB".format(float(x['download']/1024.0)), "{0:.2f} MB".format(float(x['upload']/1024.0))] for x in data])
df.columns = ['Date', 'Downloaded', 'Uploaded']
df['Date'] = pd.to_datetime(df['Date'], unit="s")
df.set_index('Date', inplace=True)



print df

