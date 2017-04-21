#!/usr/bin/env python

# sudo pip install --upgrade google-api-python-client
# sudo pip install html2text

import requests
import json
import codecs
import time
import html2text
import os


#signId = "YOURID"
apiKey = open(os.path.expanduser('./apikey')).read().strip()
dstFileName = "meetupCalendar.ics"


#requestUrl = "https://api.meetup.com/self/groups?&photo-host=public&sig_id=" + signId + "&sign=true&key=" + apiKey
requestUrl = "https://api.meetup.com/self/groups?&photo-host=public&sign=true&key=" + apiKey
r = requests.get(requestUrl)



targetFile = codecs.open(dstFileName, "w", "utf-8")
targetFile.write("BEGIN:VCALENDAR\n")
targetFile.write("PRODID:-//Mozilla.org/NONSGML Mozilla Calendar V1.1//EN\n")
targetFile.write("VERSION:2.0\n")


for group in r.json():

	print group['urlname']

	requestUrl = "https://api.meetup.com/"
	requestUrl += group['urlname']
	requestUrl += "/events?photo-host=public"
	#requestUrl += "&sig_id=" + signId
	requestUrl += "&status=proposed%2Csuggested%2Cupcoming"
	requestUrl += "&sign=true&key=" + apiKey

	events = requests.get(requestUrl)


	for event in events.json():

		if 'time' in event:
			targetFile.write("BEGIN:VEVENT" + "\n")
			targetFile.write("CREATED:" + "20150128T203538Z" + "\n")
			targetFile.write("LAST-MODIFIED:" + "20161101T095442Z" + "\n")
			targetFile.write("DTSTAMP:" + "20161101T095442Z" + "\n")
			#targetFile.write("UID:1m7j60as0psklein1gm88c87do@google.com")
			targetFile.write("SUMMARY:" + event["name"] + "\n")
			targetFile.write("STATUS:TENTATIVE" + "\n")
			#targetFile.write("LOCATION:" + event["venue"] + "\n")

			if 'venue' in event:
				targetFile.write("LOCATION:" + event["venue"]["address_1"] +", " + event["venue"]["city"] + "\n")

			#targetFile.write("ORGANIZER;CN=Boulo:mailto:380uvj0ph71nb0k3tol66uh2sg@group.calendar.google.com")

			startTime = time.strftime( '%Y%m%dT%H%M%S', time.localtime( int(event["time"])/1000 ) )

			if 'duration' in event:
				endTime = time.strftime( '%Y%m%dT%H%M%S', time.localtime( (int(event["time"]) + int(event["duration"]))/1000 ) )
			else:
				endTime = time.strftime( '%Y%m%dT%H%M%S', time.localtime( (int(event["time"]) + 7200000)/1000 ) )

			targetFile.write("DTSTART;TZID=Europe/Paris:" + startTime + "\n")
			targetFile.write("DTEND;TZID=Europe/Paris:" + endTime + "\n")

			targetFile.write("URL:" + event["link"] + "\n")
			
			if 'description' in event:
				targetFile.write("DESCRIPTION:" + html2text.html2text(event["description"]).replace('\n', '\\n') + "\n")
			else:
				targetFile.write("DESCRIPTION:")
  			
			targetFile.write("SEQUENCE:0" + "\n")
			targetFile.write("X-DEFAULT-ALARM:TRUE" + "\n")
			targetFile.write("END:VEVENT" + "\n")

			#print " - " + event["name"]


targetFile.write("END:VCALENDAR")
