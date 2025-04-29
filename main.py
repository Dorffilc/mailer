import time
import random
from datetime import datetime
from mailer import send_email
from ai_interaction import draft_email, validate_email, generate_subject
from email_counter import increment_today_count, get_today_count, get_daily_max_limit
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def is_within_business_hours(start_hour=8, end_hour=17):
    current_hour = datetime.now().hour
    return start_hour <= current_hour < end_hour

def main():
    print("[START] Email Automation Program Started.")
    while True:
        # Random wait
        min_wait = int(os.getenv('MIN_WAIT_MINUTES', 20))
        max_wait = int(os.getenv('MAX_WAIT_MINUTES', 30))
        wait_minutes = random.randint(min_wait, max_wait)
        print(f"[INFO] Waiting {wait_minutes} minutes before next email attempt...")
        time.sleep(wait_minutes * 60)

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[INFO] Current time: {now}")

        if not is_within_business_hours():
            print("[INFO] Outside business hours (08:00-17:00). Skipping this cycle.")
            time.sleep(60*60)  # Sleep for 1 hour before checking again
            continue

        # Check if daily limit is reached
        current_count = get_today_count()
        daily_limit = get_daily_max_limit()
        print(f"[INFO] Today's email count: {current_count}/{daily_limit}")

        if current_count >= daily_limit:
            print(f"[WARNING] Reached today's max email limit ({daily_limit}). Skipping sending.")
            time.sleep(60*60)  # Sleep for 1 hour before checking again
            continue

        # Draft new email
        print("[ACTION] Drafting new email...")
        new_email = draft_email()

        # Validate drafted email
        print("[ACTION] Validating drafted email...")
        validated_email = validate_email(new_email)

        if validated_email:
            subject = generate_subject(validated_email)
            print(f"[ACTION] Sending email with subject: '{subject}'")
            print(f"[ACTION] Email body:\n{validated_email}")
            send_email(validated_email, subject)

            increment_today_count()
            updated_count = get_today_count()
            print(f"[SUCCESS] Email sent. Updated email count: {updated_count}/{daily_limit}")
        else:
            print("[ERROR] Email validation failed. Skipping sending this draft.")

if __name__ == "__main__":
    main()
