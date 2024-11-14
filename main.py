#!/usr/bin/env python3

import os
import time
import traceback
import json
from dotenv import load_dotenv
import datetime

from pushbullet import Pushbullet


def send_pushbullet(pb, text=None, url=None, failed=False):
    if not failed:
        if url:
            pb.push_link('New Hotel fits description', url, text, channel=pb.channels[0])
        else:
            pb.push_note('New Boligportal Email', text, channel=pb.channels[0])
    # else:
    #     pb.push_note('The Boligportal script failed', 'It failed ...', channel=pb.channels[0])


def script(QUERY, MAX_EMAILS, LOG_FILE, PB):
    # here will log the info of the messages, to not continuosly ping the same ones
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            log_messages = json.load(f)
    else:
        log_messages = {}

    # READ EMAILS
    emails = email_reader.get_emails(QUERY, MAX_EMAILS)
    print(f'At {datetime.datetime.now()}: {len(emails)} boligportal messages without reading.')

    if len(emails) > 0:
        for ind, email in enumerate(emails):

            # Prepare the text to send
            text = f"New email ({email['id']}) !!:\n  Subject: {email['subject']}.\n"

            if email['id'] not in log_messages.keys():
                # if its a new message

                # SEND NOTIFICATION
                send_pushbullet(PB, text=text, url=email['url'])

                # log it
                log_messages[email['id']] = email

                with open(LOG_FILE, 'w') as f:
                    json.dump(log_messages, f, indent=4)


def main():
    """Main function."""

    # where will save the logs
    LOG_FILE = './logs_messages.json'

    # Define if we will want to run it only once for cron jobs, or continuously
    CRON_JOB = False
    SLEEP_TIME = 10 # only needed if its not a cron job

    try:
        # Load parameters from the .env file
        load_dotenv()
        # phone_number = os.getenv('WHATS')
        pushbullet_token = os.getenv('PB_API')

        pb = Pushbullet(pushbullet_token)

        if CRON_JOB:
            pass
            # script(QUERY, MAX_EMAILS, LOG_FILE, pb)
        else:
            print('Starting script')
            while True:
                # script(QUERY, MAX_EMAILS, LOG_FILE, pb)
                print(f'Sleep for {SLEEP_TIME}s')
                time.sleep(SLEEP_TIME)

    except Exception as e:
        print('Failed')
        traceback.print_exc()
        # Will try to send a notification that the script is down
        send_pushbullet(pb, failed=True)

if __name__ == '__main__':
    main()
