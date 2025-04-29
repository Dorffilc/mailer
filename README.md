# 📧 AI-Powered Automated Email Sender
This project automates drafting, validating, and sending professional emails at random intervals between 08:00 and 17:00.
Each email is drafted using OpenAI's ChatGPT, validated by a second AI, and includes attachments from a local folder.
The system tracks daily email limits with a progressive scaling plan and persists between restarts.

## 🚀 Features
✅ Drafts emails using dynamic AI instructions (instruction.txt).

✅ Takes into account the last sent email to vary wording naturally.

✅ Validates the quality of the drafted email before sending.

✅ Sends emails only during business hours (08:00 to 17:00).

✅ Randomized sending interval (20–30 minutes by default).

✅ Automatically attaches all files in the /attachments/ folder.

✅ Tracks emails sent per day using email_counter.json.

✅ Progressively increases daily sending limits (1, 2, 3, 5, 8, 10, 15, 20).

✅ Self-healing: creates necessary folders if missing.

## 📂 Project Structure
```
email_automation/
│
├── attachments/            # Files to be attached to each email
├── main.py                  # Main orchestrator
├── mailer.py                # Handles email sending
├── ai_interaction.py        # AI email drafting and validation
├── email_counter.py         # Tracks daily email counts and progression
├── vector_store.py          # (Optional) stores past emails if needed
├── instruction.txt          # AI prompt for drafting emails
├── email_counter.json       # Tracks sent emails (auto-created)
├── .env                     # Environment variables
├── requirements.txt         # Required Python packages
└── README.md                # This file
```
### 🛠 Setup Instructions
```
Clone the Repository
git clone https://your-repo-url/email_automation.git
cd email_automation
Create a Python Virtual Environment (Recommended)

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
Install Required Packages

pip install -r requirements.txt
Create your .env File
```

Example .env:
```
# Gmail Settings
GMAIL_ADDRESS=your-email@gmail.com
APP_PASSWORD=your-app-password

# OpenAI API
OPENAI_API_KEY=your-openai-api-key

# Email Settings
RECEIVER_EMAIL=recipient@example.com

# Timer Settings
MIN_WAIT_MINUTES=20
MAX_WAIT_MINUTES=30
```

### Edit instruction.txt
Provide the base instruction for drafting emails.
Example:
```
Write a professional update to a client regarding project status, maintaining a positive and proactive tone.
Prepare attachments/ Folder

Add any files you want attached to each email into the attachments/ folder.
(If missing, the folder will be auto-created.)
```

### Run the App
```
python main.py
```

## 📊 How the App Works
Every 20–30 minutes (randomized), the app checks:

Is it business hours?

Have we reached today's email limit?

If yes:

Draft a new email using ChatGPT.

Validate the draft using a second AI pass.

Attach all files inside /attachments/.

Send the email via Gmail.

Log the email into email_counter.json.

Daily email sending limits progressively increase:

1, 2, 3, 5, 8, 10, 15, 20 emails/day.

## 📈 Email Progression Tracking
email_counter.json keeps track of:

How many emails were sent today.

What progression step the project is at.

Even after restarting the app, the progression continues without resetting.

### Example email_counter.json:
```
{
  "progression_index": 2,
  "history": {
    "2025-04-28": { "emails_sent": 1 },
    "2025-04-29": { "emails_sent": 2 }
  }
}
```

## ⚙️ Environment Variables (.env)

Variable	Description
GMAIL_ADDRESS	Your Gmail address
APP_PASSWORD	Your Gmail App Password
OPENAI_API_KEY	Your OpenAI API Key
RECEIVER_EMAIL	Recipient's email address
MIN_WAIT_MINUTES	Minimum minutes between emails
MAX_WAIT_MINUTES	Maximum minutes between emails

## 📢 Important Notes
Ensure 2-Step Verification is enabled on your Gmail and use an App Password, not your normal password.

Be mindful of OpenAI API usage costs if sending frequent emails.

Gmail accounts have daily sending limits (~500 for regular accounts).

Make sure your attachments are not too large (stay under 20MB total is a good practice).

## ✨ Credits
Built with ❤️ using OpenAI, Python, and smart email automation practices.

## 📄 License
This project is for internal or personal use.
If you intend to distribute commercially, please review applicable licensing regarding Gmail API usage and OpenAI's API.
