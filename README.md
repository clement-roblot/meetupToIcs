What why
========
This script is used to build a ics calendar containing the upcoming meetups you may want to go to. That way you can see those as potential future events in your regular calendar app.

Pre-install
===========
To run this script you need to put your API KEY in the file "apikey", you can get it on this page : https://secure.meetup.com/meetup_api/key/

Your key must be the only thing in this file (no quotes, no spaces, no new lines).

Run
===
To run the script you will need to install html2text with the command :

```
sudo pip install html2text requests
```

Then simply run the script :

```
./buildCalendar.py
```

