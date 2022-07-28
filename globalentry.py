import os
import requests
import time
import sys
import json

import telegram

from dotenv import load_dotenv 
from datetime import datetime, timedelta

# API URL
APPOINTMENTS_URL = "https://ttp.cbp.dhs.gov/schedulerapi/slots?orderBy=soonest&limit=1&locationId={location}&minimum=1"

TTP_TIME_FORMAT = '%Y-%m-%dT%H:%M'



load_dotenv()

token = os.getenv("BOT_TOKEN")
chat_id = os.getenv("CHAT_ID")
end_date = os.getenv("END_DATE")
# How often to run this check in seconds
TIME_WAIT = int(os.getenv("TIME_WAIT"))

# List of Global Entry locations
LOCATION_IDS = json.loads(os.getenv("LOCATIONS"))
# Dates
# now = datetime.now()
# future_date = now + timedelta(days=DELTA)


def send_chat(token, chat_id, message):
    """
    Telegram bot to send a message with an existing bot
    to a designated chat id.
    """
    bot = telegram.Bot(token)
    bot.send_message(text = message, chat_id=chat_id)

def check_schedule(location_code):
    """
    Formats appointment URL with location id
    and returns appointments if available.
    """
    url = APPOINTMENTS_URL.format(location=location_code)
    appointments = requests.get(url).json()
    return appointments

def main():
    try:
        while True:
            for city, id in LOCATION_IDS.items():
                try:
                    appointments = check_schedule(id)
                except Exception as e:
                    print("Could not retrieve appointments from API.")
                    appointments=[]
                if appointments:
                    appt_datetime = datetime.strptime(appointments[0]["startTimestamp"], '%Y-%m-%dT%H:%M')
                    message = f'An appointment was found at {appt_datetime} login to book it\n https://ttp.cbp.dhs.gov/schedulerui/'
                    send_chat(token,chat_id,message)
                    print("Message Sent")
                else:
                    print("No Appointments Found")
            time.sleep(TIME_WAIT)
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == "__main__":
    main()