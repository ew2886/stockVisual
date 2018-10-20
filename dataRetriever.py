import requests
import json
import sys
import pandas as pd
import numpy as np

class dataRetriever:
	def __init__(self, startDate, endDate, tickers):
		self.startDate = startDate
		self.endDate = endDate
		self.tickers = tickers
		print(self.tickers)

	# retrieve the data
	def getData(self):
		client_id = r'ad28ca9011264914a08e94295a7a2039'
		client_secret = r'1cd76fc9f05d73bd9699be938e07f0bb69a0a3a4b879ed399970ede69212088f'
		guid = r'ab92dddfb3ca4e7ca511b09ff1c14f2b'

		auth_data = {
		    'grant_type'    : 'client_credentials',
		    'client_id'     : client_id,
		    'client_secret' : client_secret,
		    'scope'         : 'read_content read_financial_data read_product_data read_user_profile'
		}

		# create session instance
		session = requests.Session()

		# make a POST to retrieve access_token
		auth_request = session.post('https://idfs.gs.com/as/token.oauth2', data = auth_data)
		access_token_dict = json.loads(auth_request.text)
		access_token = access_token_dict['access_token']

		# update session headers
		session.headers.update({'Authorization':'Bearer '+ access_token})

		payload = {
		    "startDate": self.startDate,
		    "endDate": self.endDate,
		    "where": {
		        "ticker": self.tickers
		    }
		}

		request_url = 'https://api.marquee.gs.com/v1/data/USCANFPP_MINI/query'
		request = session.post(url=request_url, json = payload)
		results = json.loads(request.text)
		data = results['data']
		return data


if __name__ == '__main__':
	args = sys.argv
	print(args)
	startDate = args[1]
	endDate = args[2]
	tickers = [ticker for ticker in args[3:]]
	dr = dataRetriever(startDate, endDate, tickers)
	data = pd.DataFrame(dr.getData()).sample(frac=1)
	print(data)
