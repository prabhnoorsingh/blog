from django.core,mail import send_mail
from registration.signals import user_activated
import urllib2
import json

def fullContactCollect(email):
	api_key = '3558403aafc12f64'
	email = email
	fullURL = 'https://api.fullcontact.com/v2/person.json?apiKey='+api_key+
	loadUrl = urllib2.urlopen(fullURL)
	jsonData = json.load(loadUrl)

	return jsonData

def fullContactEmailSend(sender, user, request, **kwargs):
	email = user.email

	data = fullContactCollect(email)
	if data['status']==200:
		messgae= data
		send_mail("Full Contact Data",
					data,
					'prabhnoor925@gmail.com',
					'prabhnoor925@gmail.com',
					fail_silently=False)


user_activated.connect(fullContactEmailSend)