from urllib.request import urlopen
from urllib.error import HTTPError
import requests
import json
import sys
import math
from operator import add
from os.path import join, isfile, dirname




VC_Investments = {}


vc_url = 'https://api.crunchbase.com/v/3/organizations?categories=Venture%20Capital&locations=United%20States&user_key=4c3b3f5bc197608d9e93bfbda7be32e2'

########### first page of API ##########
try:	
	r = requests.get(vc_url)
	jsonResponse = r.json()

	number_of_pages = jsonResponse["data"]["paging"]["number_of_pages"]	
	organizations_list = jsonResponse["data"]["items"]

	
	#going through all the VCs
	for org in organizations_list:

		companies = {}
		VC_name = org["properties"]["name"]
		print (VC_name)
		url = 'https://api.crunchbase.com/v/3/organizations/'+ org["properties"]["permalink"] +'/investments?user_key=4c3b3f5bc197608d9e93bfbda7be32e2'
		requ = requests.get(url)
		jsonTemp = requ.json()

		number_of_investments = jsonTemp["data"]["paging"]["total_items"]
		#skips if there is no investments
		if number_of_investments == 0:
			continue


		try:
			#looking at all the companies that a specific VC has invested in 
			for company in jsonTemp["data"]["items"]:
				#all the info we need is under the needed_data path
				needed_data = company["relationships"]["funding_round"]["relationships"]["funded_organization"]

				###### All the information we need #######
				uuid = needed_data["uuid"]
				permalink = needed_data["properties"]["permalink"]
				api_link = needed_data["properties"]["api_path"]
				name = needed_data["properties"]["name"]
				short_description = needed_data["properties"]["short_description"]
				profile_image_url = needed_data["properties"]["profile_image_url"]
				total_funding = needed_data["properties"]["total_funding_usd"]
				homepage_url = needed_data["properties"]["homepage_url"]
				investors = []


				###### opening up a request to the company page API so we can grab all their investors ########
				company_url = 'https://api.crunchbase.com/v/3/organizations/'+permalink+'?user_key=4c3b3f5bc197608d9e93bfbda7be32e2'
				req = requests.get(company_url)
				jsonTemporary = req.json()

				#grabs the name of all the VCs that have invested in the specific company
				all_investors = jsonTemporary["data"]["relationships"]["investors"]["items"]
				if len(all_investors) == 0:
					continue

				for investor in all_investors:
					print (investor["properties"])
					try: 
						investor_name = investor["properties"]["name"]
						investors.append(investor_name)
					except: 
						continue


				# (company_name: (#0 uuid, #1 short_descr, #2 profile_image, #3 total_fund, #4 homepage_url, #5 name))
				companies[name] = (uuid, permalink, short_description, profile_image_url, total_funding, homepage_url, investors)

				#adds that company(as a dictionary) into a dictionary of all the companies that a specific VC has invested in
				#dictionary within a dictionary

			####### (VC: [all companies they invested in])	
			VC_Investments[VC_name] = companies
		except:
			continue

except requests.exceptions.RequestException as e: 
    print (e)
    sys.exit(1)




######### WRITE FILE to txt  ######


	# fileHandle = open('Company_Info.txt', 'w')	
		
	# for vc in organizations:
	# 	fileHandle.write(str(vc) + str(organizations[vc]) + "\n")

	# fileHandle.close()

	# print ("finished writing file")




