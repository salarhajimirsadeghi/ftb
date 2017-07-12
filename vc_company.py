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

HOST = "localhost"
USER = "root"
PASSWD = "012394"
DATABASE = "VCs"


def grab_info():

	cnx = mysql.connector.connect(host=HOST, user=USER, passwd=PASSWD, database=DATABASE)
	vc_cursor = cnx.cursor(buffered=True)
	cnx2 = mysql.connector.connect(host=HOST, user=USER, passwd=PASSWD, database=DATABASE)
	company_cursor = cnx.cursor(buffered=True)
# <<<<<<< Updated upstream
# =======
	cnx3 = mysql.connector.connect(host=HOST, user=USER, passwd=PASSWD, database=DATABASE)
	insert_cursor = cnx3.cursor(buffered=True)
	cnx4 = mysql.connector.connect(host=HOST, user=USER, passwd=PASSWD, database=DATABASE)
	checkD_cursor = cnx4.cursor(buffered = True)
# >>>>>>> Stashed changes
	

	query2 = ("SELECT COMPANY_NAME, PERMA_LINK, CID FROM COMPANIES")	
	company_cursor.execute(query2)
	cnx2.commit()

	counter = 1
	for (COMPANY_NAME, PERMA_LINK, CID) in company_cursor:
		try:
			company_url = 'https://api.crunchbase.com/v/3/organizations/'+ PERMA_LINK +'?user_key=4c3b3f5bc197608d9e93bfbda7be32e2'
			req = requests.get(company_url)
			jsonT = req.json()

			try:

				#company_investors is a list at this point (from the API)
				company_investors = jsonT["data"]["relationships"]["investors"]["items"]

				for investor in company_investors:
					try: 				
						investor_name = investor["properties"]["name"]						
						query = ("SELECT VC_NAME, PERMA_LINK, VID FROM VCs WHERE VC_NAME = '%s'" %investor_name)
			
						vc_cursor.execute(query)
						cnx.commit()

						row = vc_cursor.fetchone()
						if row is not None:	  					
		  					VID = row[2].strip()
		  					VC_NAME = row[0].strip()

		  					checkD_query = ("SELECT VID, CID FROM VC_COMPANY WHERE VID ='%s' AND CID ='%s' " %(VID, CID))
		  					
		  					checkD_cursor.execute(checkD_query)
		  					
		  					hasRow = checkD_cursor.fetchone()
		  					if(hasRow is None):
		  	         
			  					# insert into 3rd table
			  					# print(type(VID))
			  					# print("before insert query") 
			  					# print("before inserting")
			  					insert_query = ("INSERT INTO VC_COMPANY(VID, VC_NAME, CID, COMPANY_NAME) VALUES \
			  						(%s, %s, %s, %s)")
			  					# print(VID, VC_NAME, CID, COMPANY_NAME) 
			  					insert_cursor.execute(insert_query, (VID, VC_NAME, CID, COMPANY_NAME))
			  					cnx3.commit()
			  					# print("after cursor.execute")
			  					# row = vc_cursor.fetchone()
		  					else: 
		  						print ("hasRow: ", hasRow)

					except:					
						continue
			except:
				continue
			print (COMPANY_NAME, PERMA_LINK, CID)
		
		except:
			continue
	# >>>>>>> Stashed changes



				





		# for (VC_NAME, PERMA_LINK, VID) in vc_cursor:
		# 	print(VC_NAME, VID)
		# 	url = 'https://api.crunchbase.com/v/3/organizations/'+ PERMA_LINK +'/investments?user_key=4c3b3f5bc197608d9e93bfbda7be32e2'
		# 	requ = requests.get(url)
		# 	jsonTemp = requ.json()


	cnx.close()
	cnx2.close()
# <<<<<<< Updated upstream
	company_cursor.close()	
	vc_cursor.close()			
# =======
	cnx3.close()
	company_cursor.close()	
	vc_cursor.close()		
	insert_cursor.close()
# >>>>>>> Stashed changes
	


grab_info()


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
