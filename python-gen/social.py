import random
import datetime 

import core as c
import helpers as h

columnData = [
'social_customer_id',
'social_email',
'social_last_uri',
'social_timestamp',
'social_ip',
'social_sha256',
'social_uuid4'
]


def generateSocialInteractions(customerid: str, maxinteractions: int, email: str):

	rowcount = 0
	social = ""

	for newrow in range(random.randint(1,maxinteractions)):   # for each customer we gen 1-N social interactions, change as desired
		newrow = ""
		newrow += c.quote + customerid + c.quotecomma
		newrow += c.quote + email + c.quotecomma

		for idx, item in enumerate(columnData):	
			if item != "social_customer_id" and item != "social_email":
				newrow += c.quote + h.extraHandlerMap(item) + c.quote
				newrow += c.comma if idx+1 != len(columnData) else ""
		#6 newline if not last line
		if rowcount != maxinteractions:														
			newrow+= c.newline
		
		social += newrow

		rowcount+=1

	return(social)