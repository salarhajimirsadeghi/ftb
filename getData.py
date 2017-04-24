from urllib.request import urlopen
from urllib.error import HTTPError
import requests
import json
import sys
import math
from operator import add
from os.path import join, isfile, dirname



# Can be seen by entire program
organizations = {}
VC_Investments = {}
global investor_counter
all_investments = set()


#Function that just adds to our organization dictionary
def add_to_dictionary(organizations_list):
	print("got to add_to_dictionary function") 
	for org in organizations_list:
		global investor_counter
		# print() org["properties"]["permalink"]
		url = 'https://api.crunchbase.com/v/3/organizations/'+ org["properties"]["permalink"] +'/investments?user_key=4c3b3f5bc197608d9e93bfbda7be32e2'
		r = requests.get(url)
		jsonTemp = r.json()

		number_of_investments = jsonTemp["data"]["paging"]["total_items"]		
		
		#skips if there is no investments
		if number_of_investments == 0:
			continue
		
		organizations[org['properties']['name']] = (org["uuid"], org["properties"]["permalink"], org["properties"]["region_name"], investor_counter)				
		investor_counter += 1
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

	# number_of_pages = jsonResponse["data"]["paging"]["number_of_pages"]	
	organizations_list = jsonResponse["data"]["items"]
	investor_counter = 0


	
	for org in organizations_list:

		url = 'https://api.crunchbase.com/v/3/organizations/'+ org["properties"]["permalink"] +'/investments?user_key=4c3b3f5bc197608d9e93bfbda7be32e2'
		r = requests.get(url)
		jsonTemp = r.json()

		number_of_investments = jsonTemp["data"]["paging"]["total_items"]		
		#skips if there is no investments
		if number_of_investments == 0:
			continue

		# builds a dictionary (name : (uuid, permalink, region_name, id))		
		organizations[org['properties']['name']] = (org["uuid"], org["properties"]["permalink"], org["properties"]["region_name"], investor_counter)
		investor_counter += 1					
		

	print("finished organization creation") 
	

	#Just counting up to page 3 for now...
	for x in range (1, 3):	
		print("there are more pages. Wer're on page: " + str(x)	) 
		r = requests.get(jsonResponse["data"]["paging"]["next_page_url"] + "&user_key=4c3b3f5bc197608d9e93bfbda7be32e2")		
		jsonResponse = r.json()
		organizations_list = jsonResponse["data"]["items"]
		add_to_dictionary(organizations_list)
	print("finished all organization creation") 
	# Here we have all vcs added to our dictionary along with their values		
	#Investments of every VC
	number_of_vcs = len(organizations)
	print("There are " + str(number_of_vcs) + " VCs, in this set")		
	


	#############################################################################################
	# Figuring out all the VCs Investments
	# key is the name of the VCs
	for key in organizations:
	
		permalink = organizations[key][1]
		url = 'https://api.crunchbase.com/v/3/organizations/'+ permalink +'/investments?user_key=4c3b3f5bc197608d9e93bfbda7be32e2'
		r = requests.get(url)
		jsonForm = r.json()

		#temporary variable to hold a list of all investments	
		companies = []
		invest_page = jsonForm["data"]["paging"]["number_of_pages"]
		#if there are more than 1 page of investments
		if ( invest_page > 1):
			for i in range (1, invest_page):
				
				r = requests.get(jsonResponse["data"]["paging"]["next_page_url"] + "&user_key=4c3b3f5bc197608d9e93bfbda7be32e2")
				jsonResponse = r.json()
				
				try:	
					add_investments(key, jsonForm["data"]["items"])
				except:
					add_investments(key, jsonForm["data"]["item"])
				
					
		
		#makes a dictionary with (name: [investments uuid format])
		else:						
			try:  			
				for company in jsonForm["data"]["items"]:
					companies.append(company["relationships"]["funding_round"]["relationships"]["funded_organization"]["properties"]["name"])
			except:
				try:
					company  = jsonForm["data"]["item"]			
					companies.append(company["relationships"]["funding_round"]["relationships"]["funded_organization"]["properties"]["name"])
				except: 
					continue								
	
		all_investments.update(companies)
		VC_id = organizations[key][3]
		VC_Investments[VC_id] = companies

	
	# Creates a dictionary with company_name(key) and id(value)
	# (company_name, id)	
	investments_dict = {}
	company_counter = 0
	for company in all_investments:
		investments_dict[company] = company_counter
		company_counter += 1

 

	fileHandle = open('VC_Investments.txt', 'w')	
	
	#a list of all the VCs (id) and investments (company id) in a tuple
	# (53, 123), (53, 765), ...
	Main_Data = []

	#adds the ids of companies that a specific VC invested 
	#in into a temporary list 
	for vc_id in VC_Investments:
		invest_comp_id = []
		for comp in VC_Investments[vc_id]:
			invest_comp_id.append(investments_dict[comp])

		#makes sure no duplicates
		inv_comp_id_set = set(invest_comp_id)
		invest_comp_id = list(inv_comp_id_set)
		invest_comp_id.sort()	
		
		for x in invest_comp_id:
			Main_Data.append((vc_id, x))
			fileHandle.write(str(vc_id) + ";" + str(x) + "\n")
	
	
	fileHandle.close()

	fileHandle = open("VC_Stats.txt", 'w')
	fileHandle.write("number of total investments:" + str(company_counter))
	fileHandle.close()
		
	print(Main_Data)


	# if 1-100 training, 101 - 200 validation, else testing

except requests.exceptions.RequestException as e: 
    print (e)
    sys.exit(1)





