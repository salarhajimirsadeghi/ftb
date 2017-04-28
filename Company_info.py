from __future__ import print_function
from urllib.request import urlopen
from urllib.error import HTTPError
import requests
import json
import sys
import math
from operator import add
from os.path import join, isfile, dirname
from datetime import date, datetime, timedelta
import mysql.connector

VC_Investments = {}


############ Database Information ######### 
HOST = "localhost"
USER = "root"
PASSWD = "root"
DATABASE = "VCs"
 
cnx = mysql.connector.connect(host=HOST, user=USER, passwd=PASSWD, database=DATABASE)
cursor = cnx.cursor()

############ Storing API data into MYSQL ############
def store_vc_data(COMPANY_NAME, PERMA_LINK, IMAGE, DESCRIPTION, URL, UUID, TOTAL_FUNDING):

    insert_query = ("INSERT INTO COMPANIES (VID, VC_NAME, PERMA_LINK, IMAGE, DESCRIPTION, URL, UUID, \
    								TOTAL_FUNDING) VALUES \
									(%i, %s, %s, %s, %s, %s, %i, %f)")
    cursor.execute(insert_query, (COMPANY_NAME, PERMA_LINK, IMAGE, DESCRIPTION, URL, UUID, 
					TOTAL_FUNDING))

    cnx.commit()
    
    return


####### Need to link VID and CID ####
def store_vc_company(VC_NAME, COMPANY_NAME):

	insert_query = ("INSERT INTO VC_COMPANY (VC_NAME, COMPANY_NAME) VALUES \
									(%s, %s)")
    cursor.execute(insert_query, (VC_NAME, COMPANY_NAME))

    cnx.commit()
    
    return
#########################################################



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
		
		
				#adds that company(as a dictionary) into a dictionary of all the companies that a specific VC has invested in
				#dictionary within a dictionary
				# (company_name: (#0 name, #1 permalink, #2 profile_image, #3 description, #4 homepage_url, #5 uuid,
								  #6 total_funding, #7 investors))
				companies[name] = (name, permalink, image, short_description,homepage_url, uuid, total_funding, investors)			

			####### (VC: [all companies they invested in])	
			VC_Investments[VC_name] = companies

			######## Writing to Database #########
			for company in companies:
				# print (len(organizations[vc]))
				data = companies[company]
				store_vc_data(data[0],data[1],data[2],data[3],data[4],data[5],data[6])
				store_vc_company(VC_NAME, company)
			######################################
	


		except:
			continue

except requests.exceptions.RequestException as e: 
    print (e)
    sys.exit(1)


cursor.close()
cnx.close()			


