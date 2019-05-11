import requests
import json
from dateutil.parser import parse
import datetime

# Get json object and save it to my custom JSON object
def getPartners():
	r = requests.get('http://www.url.com')
	return r.json

def datesAreConsecutive(date1, date2):
	d1 = parse(date1)
	d2 = parse(date2)
	return d2 - d1 == datetime.timedelta(1)

# Main method
if __name__ == '__main__':
	countries = dict()
	output = {'countries' : []}

	# get a list of all the partners
	r = requests.get('http://www.url.com')
	partners = r.json()['partners'] 

	# Iterate through the partners to get a list of countries,
	# and each country's possible dates where partners are
	# availible
	for	partner in partners:
		temp_country = partner['country']
		if temp_country not in countries:
			countries[temp_country] = dict()

		# Save the name of all partners who are availible for each date
		for avail in partner['availableDates']:
			if avail not in countries[temp_country]:
				countries[temp_country][avail] = set()
			countries[temp_country][avail].add(partner['email'])

	# Now Iterate thorough the countries and create an event for each
	# country
	for country, list_of_dates in countries.items():
		max_attendees = -1
		max_attendees_emails = []
		start_date = None


		# in order to find the 2 days with most attendees
		# we need to iterate through the sorted dates and  
		# keep count of the date that will yield the maximum
		# number of attendees
		sortedDates = sorted(list_of_dates.keys())
		for i in range(len(sortedDates)-1):
			if not datesAreConsecutive(sortedDates[i], sortedDates[i+1]):
				continue

			# Count atendees that can go to both days
			day1_atendees = countries[country][sortedDates[i]]
			day2_atendees = countries[country][sortedDates[i+1]]
			both_atendees = day1_atendees & day2_atendees

			if len(both_atendees) > max_attendees:
				max_attendees = len(both_atendees) 
				max_attendees_emails = list(both_atendees)
				start_date = sortedDates[i]

		event = dict()
		# if no suitible date was found
		if (max_attendees == -1):
			event['attendeeCount'] = 0
			event['attendees'] = []
			event['name'] = country
			event['startDate'] = None
		else:
			event['attendeeCount'] = max_attendees
			event['attendees'] = max_attendees_emails
			event['name'] = country
			event['startDate'] = start_date

		output['countries'].append(event)

	res = requests.post("http://www.url.com", data=json.dumps(output))
	print(res.text)