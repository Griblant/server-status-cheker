import os
import logging
import time
import requests
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(filename="servlogs.txt", 
format='%(levelname)s %(asctime)s %(message)s', level=logging.INFO) 


URL = 'https://python101.online/'
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TO_PHONE = os.getenv('TO_PHONE')
FROM_PHONE = os.getenv('FROM_PHONE')
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def response_cheker(url):
    response = requests.get(url)

    return response.status_code

def sms_send(server_status):
    try:
        message = client.messages.create(
            body='Server {URL} is unavailiable, status is' + server_status,
            from_=FROM_PHONE,
            to=TO_PHONE,
            ) 
        logging.info(f'SMS succsesfully sended. SID: {message.sid}')
    except Exception:
        logging.error('SMS wasnt sended')


while True:
    logging.info('Cheking server response')
    server_status = response_cheker(URL)

    if server_status == 200:
        logging.info('Server is available')
    else:
        sms_send(server_status)
        logging.info(f'Server status is {server_status}')

    time.sleep(60)
    