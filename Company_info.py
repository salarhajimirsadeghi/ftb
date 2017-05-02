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

#list of all the companies that all vcs have invested in
company_list = {}


############ Database Information ######### 
HOST = "localhost"
USER = "root"
PASSWD = "012394"
DATABASE = "VCs"

cnx = mysql.connector.connect(host=HOST, user=USER, passwd=PASSWD, database=DATABASE)
cursor = cnx.cursor()


############ Storing API data into MYSQL ############
def store_company_data(COMPANY_NAME, PERMA_LINK, IMAGE, DESCRIPTION, URL, UUID, TOTAL_FUNDING, CID):
	print("COMPANY_NAME: " + str(type(COMPANY_NAME)) + COMPANY_NAME)
	print("PERMA_LINK: " + str(type(PERMA_LINK)) + PERMA_LINK)
	print("DESCRIPTION: " + str(type(DESCRIPTION)) + DESCRIPTION)
	print("URL: " + str(type(URL)) + URL)
	print("UUID: " + str(type(UUID)) + UUID)
	print("TOTAL_FUNDING: " + str(type(TOTAL_FUNDING)) + TOTAL_FUNDING)
	print("CID: " + str(type(CID)) + CID)

	print("inside store_company_data: " + str(COMPANY_NAME))
	insert_query = ("INSERT INTO COMPANIES (CID, COMPANY_NAME, PERMA_LINK, IMAGE, DESCRIPTION, URL, UUID, TOTAL_FUNDING) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
	print ("about to cursor.execute")

	cursor.execute(insert_query, (CID, COMPANY_NAME, PERMA_LINK, IMAGE, DESCRIPTION, URL, UUID, TOTAL_FUNDING))
	cnx.commit()
	print ("cnx.commit() finished.")


	return

# def store_vc_company(company, investors):
# 	cnx2 = mysql.connector.connect(host=HOST, user=USER, passwd=PASSWD, database=DATABASE)
# 	cursor2 = cnx2.cursor()
# 	cnx3 = mysql.connector.connect(host=HOST, user=USER, passwd=PASSWD, database=DATABASE)	
# 	cursor3 = cnx3.cursor()
# 	cnx4 = mysql.connector.connect(host=HOST, user=USER, passwd=PASSWD, database=DATABASE)	
# 	cursor4 = cnx4.cursor()

# 	for investor in investors:
# 		query = ("SELECT VID FROM VCs WHERE VC_NAME = %s")	
# 		cursor2.execute(query, investor)
# 		query2 = ("SELECT CID FROM COMPANIES WHERE COMPANY_NAME = %s")
# 		cursor3.execute(query2, company)
# 		for (VID) in cursor2:
# 			insert_query = ("INSERT INTO VC_COMPANY(VID, VC_NAME, CID, COMPANY_NAME) VALUES \
# 				(%s, %s, %s, %s)")
# 			cursor4.execute(insert_query, (VID, investor, CID, company))


# 	cnx2.commit()
# 	cnx3.commit()
# 	cnx4.commit()
# 	cursor2.close()
# 	cursor3.close()
# 	cursor4.close()
# 	cnx2.close()
# 	cnx3.close()
# 	cnx4.close()


####### Need to link VID and CID ####
# def store_vc_company(VC_NAME, COMPANY_NAME):
# 	insert_query = ("INSERT INTO VC_COMPANY (VC_NAME, COMPANY_NAME) VALUES \
# 									(%s, %s)")
# 	cursor.execute(insert_query, (VC_NAME, COMPANY_NAME))
#     cnx.commit()

#     return
#########################################################


CID = 1
vc_url = 'https://api.crunchbase.com/v/3/organizations?categories=Venture%20Capital&locations=United%20States&user_key=4c3b3f5bc197608d9e93bfbda7be32e2'

########### first page of API ##########

r = requests.get(vc_url)
jsonResponse = r.json()
organizations_list = jsonResponse["data"]["items"]

for y in range (1, 3):
	print("Wer're on page [VCs]: " + str(y)	) 
	print ("next page url is: " + jsonResponse["data"]["paging"]["next_page_url"])
	r = requests.get(jsonResponse["data"]["paging"]["next_page_url"] + "&user_key=4c3b3f5bc197608d9e93bfbda7be32e2")		
	jsonResponse = r.json()
	for item in jsonResponse["data"]["items"]:
		organizations_list.append(item)

# try:
# number_of_pages = jsonResponse["data"]["paging"]["number_of_pages"]		
#going through all the VCs

for org in organizations_list:

	companies = {}
	VC_name = org["properties"]["name"]
	# print (VC_name)
	url = 'https://api.crunchbase.com/v/3/organizations/'+ org["properties"]["permalink"] +'/investments?user_key=4c3b3f5bc197608d9e93bfbda7be32e2'
	requ = requests.get(url)
	jsonTemp = requ.json()

	number_of_investments = jsonTemp["data"]["paging"]["total_items"]
	#skips if there is no investments
	if number_of_investments == 0:
		continue
	# print ("HERE 1")

	try:
		#looking at all the companies that a specific VC has invested in 
		for company in jsonTemp["data"]["items"]:
			# print ()
			# print ("HERE 2")
			#all the info we need is under the needed_data path
			needed_data = company["relationships"]["funding_round"]["relationships"]["funded_organization"]

			###### All the information we need #######
			uuid = needed_data["uuid"]
			permalink = needed_data["properties"]["permalink"]
			api_link = needed_data["properties"]["api_path"]
			name = needed_data["properties"]["name"]
			short_description = needed_data["properties"]["short_description"]
			profile_image_url = needed_data["properties"]["profile_image_url"]
			total_funding = str(needed_data["properties"]["total_funding_usd"])
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
				# print (investor["properties"])
				# print ("HERE 3")
				try: 
					investor_name = investor["properties"]["name"]
					investors.append(investor_name)
				except: 
					continue
	
			# print (uuid, permalink, api_link, name, short_description, profile_image_url, total_funding, homepage_url, investors)
			#adds that company(as a dictionary) into a dictionary of all the companies that a specific VC has invested in
			#dictionary within a dictionary
			# (company_name: (#0 name, #1 permalink, #2 profile_image, #3 description, #4 homepage_url, #5 uuid,
							  #6 total_funding, #7 investors))
			print ("HERE 4")
			# print(len(companies))
			# print (companies)
			######## THIS IS THROWING AN ERROR #######
			# default_data.update({'item3': 3})
			# print(type(name))
			# print(type(permalink))
			# print(type(profile_image_url))
			# print(type(short_description))
			# print(type(homepage_url))
			# print(type(uuid))
			# print(type(total_funding))
			# print(type(investors))


			companies[name] = (name, permalink, profile_image_url, short_description, homepage_url, uuid, str(total_funding), investors)	
			print ("HERE 5")
			# print (companies[name])
			######## THIS IS THROWING AN ERROR #######

		####### (VC: [all companies they invested in])	
		print ("HERE 6")
		VC_Investments[VC_name] = companies


		######## Writing to Database #########
		print ("length of [companies]: " + str(len(companies)))
				
		for company in companies:
			# print (len(organizations[vc]))
			print ("company name: " + company)
			if company in company_list:
				continue
			else:				
				company_list[company] = CID
				data = companies[company]
				store_company_data(data[0],data[1],data[2],data[3],data[4],data[5],data[6], str(CID))
				CID += 1
		
			print ("CID:" + str(CID))
			
			# store_vc_company(VC_NAME, company)
			
		######################################

	except:
		continue
print("finished all work")

# except requests.exceptions.RequestException as e: 
#     print (e)
#     sys.exit(1)


cursor.close()
cnx.close()			


