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
 
# Can be seen by entire program
organizations = {}
VC_Investments = {}
global investor_counter
all_investments = set()



############ Database Information ######### 
HOST = "localhost"
USER = "root"
PASSWD = "012394"
DATABASE = "VCs"
 
cnx = mysql.connector.connect(host=HOST, user=USER, passwd=PASSWD, database=DATABASE)
cursor = cnx.cursor()

############ Storing API data into MYSQL ############
def store_vc_data(VC_NAME, PERMA_LINK, IMAGE, DESCRIPTION, URL, UUID, 
				ADDRESS, CITY, ZIPCODE, STATE, VID):
    
	try:
	    insert_query = ("INSERT INTO VCs (VID, VC_NAME, PERMA_LINK, IMAGE, DESCRIPTION, URL, UUID, \
	    								ADDRESS, CITY, ZIPCODE, STATE) VALUES \
										(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
	    cursor.execute(insert_query, (VID, VC_NAME, PERMA_LINK, IMAGE, DESCRIPTION, URL, UUID, ADDRESS, CITY, ZIPCODE, STATE))

	    cnx.commit()
	    return
	
	except:
		return
#########################################################



#Function that just adds to our VC organization dictionary (used since more than 1 page of VCs)
def add_to_dictionary(organizations_list):
	
	print("got to add_to_dictionary function") 
	for org in organizations_list:
		# global investor_counter
		# investor_counter += 1	
		# print (org["properties"])
		# print ('\n')
		# print(org["properties"]["permalink"])
		try: 
			url = 'https://api.crunchbase.com/v/3/organizations/'+ org["properties"]["permalink"] +'?user_key=4c3b3f5bc197608d9e93bfbda7be32e2'
			r = requests.get(url)
			jsonTemp = r.json()

			# print (jsonTemp)
			link = jsonTemp["data"]["properties"]
			link1 = jsonTemp["data"]["relationships"]["headquarters"]["item"]["properties"]


			number_of_investments = link["number_of_investments"]
			#skips if there is no investments
			if number_of_investments == 0:
				continue

			# builds a dictionary (VC name : ([0]uuid,[1]permalink, [2]description, [3]image, [4]url, [5]address, [6]zip, [7]city, [8]state, [9]id))
			organizations[link["name"]] = (jsonTemp["data"]["uuid"], link["permalink"], link["description"], link["profile_image_url"], 
				link["homepage_url"], link1["street_2"], link1["postal_code"],link1["city"],link1["region_code2"], investor_counter)
		except:
			continue
						


	print("finished add_to_dictionary function"	) 


#adds all the investments (the company name) in the list
#don't need to return because our dictionary is a global variable
def add_investments(key, items):
	companies = []
	for company in items:
		companies.append(company["relationships"]["funding_round"]["relationships"] \
					["funded_organization"]["properties"]["name"])
	
	#add the passed in companies to the overall investments list
	all_investments.update(companies)

	#dictionary with name of VC and the companies they've invested
	VC_Investments[key] = companies		
		



######################################
########### PROGRAM STARTS ###########
######################################


url = 'https://api.crunchbase.com/v/3/organizations?categories=Venture%20Capital&locations=United%20States&user_key=4c3b3f5bc197608d9e93bfbda7be32e2'
# request = urlopen()

try:	
	r = requests.get(url)
	jsonResponse = r.json()

	# # number_of_pages = jsonResponse["data"]["paging"]["number_of_pages"]	
	organizations_list = jsonResponse["data"]["items"]
	investor_counter = 1

	
	# for org in organizations_list:

	# 	url = 'https://api.crunchbase.com/v/3/organizations/'+ org["properties"]["permalink"] +'?user_key=4c3b3f5bc197608d9e93bfbda7be32e2'
	# 	r = requests.get(url)
	# 	jsonTemp = r.json()

	# 	#link has some information (uuid, permalink, ...)
	# 	#link1 has access to address information
	# 	link = jsonTemp["data"]["properties"]
	# 	link1 = jsonTemp["data"]["relationships"]["headquarters"]["item"]["properties"]


	# 	number_of_investments = link["number_of_investments"]
	# 	#skips if there is no investments
	# 	if number_of_investments == 0:
	# 		continue

	# 	# builds a dictionary (VC name : ([0]uuid,[1]permalink, [2]description, [3]image, [4]url, [5]address, [6]zip, [7]city, [8]state, [9]id))
	# 	organizations[link["name"]] = (str(jsonTemp["data"]["uuid"]), str(link["permalink"]), str(link["description"]), str(link["profile_image_url"]), 
	# 		str(link["homepage_url"]), str(link1["street_2"]), str(link1["postal_code"]),str(link1["city"]),str(link1["region_code2"]), investor_counter)
	# 	print(link[name])
	# 	investor_counter += 1					
		

	# print("finished first page of organization creation") 
	

	#Just counting up to page 2 for now...
	for x in range (1, 3):
		print("there are more pages. Wer're on page: " + str(x)	) 
		print ("next page url is: " + jsonResponse["data"]["paging"]["next_page_url"])
		r = requests.get(jsonResponse["data"]["paging"]["next_page_url"] + "&user_key=4c3b3f5bc197608d9e93bfbda7be32e2")		
		jsonResponse = r.json()
		for item in jsonResponse["data"]["items"]:
			organizations_list.append(item)
	
	add_to_dictionary(organizations_list)
	print("finished all organization creation") 
	# Here we have all vcs added to our dictionary along with their values		
	#Investments of every VC
	number_of_vcs = len(organizations)
	print("There are " + str(number_of_vcs) + " VCs, in this set")		
	


	######## Writing to Database #########
	VC_ID = {}
	for vc in organizations:
		# print (len(organizations[vc]))
		data = organizations[vc]
		print (vc +": " + str(investor_counter))
		investor_counter += 1
		VC_ID[vc] = investor_counter
		# print (type(data[1]))
		# print (type(data[3]) )
		# print (type(data[2])) 
		# print (type(data[4]) )
		# print (type(data[0]) )
		# print (type(data[5]) )
		# print (type(data[7]) )
		# print (type(data[6]) )
		# print (type(data[8])) 
		# print (type(investor_counter))

		# if (data[5] == "None"):
		# 	# print (type(data[5]))
		# 	data[5] = ""

		# print (type(data[5]))
		# print (data[5])
		# print (str(vc),str(investor_counter))
		store_vc_data(str(vc), data[1],data[3],data[2],data[4],data[0],data[5],data[7],data[6],data[8], str(investor_counter))
	
	######################################

	print ("finished uploading all data into Database")



except requests.exceptions.RequestException as e: 
    print (e)
    sys.exit(1)

#closes DB Connection
cursor.close()
cnx.close()			



