from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Create a thread for persistent conversation
thread = client.beta.threads.create()

def load_instruction():
    """Load instructions from 'instruction.txt'."""
    try:
        with open('instruction.txt', 'r') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError("Instruction file not found. Please create 'instruction.txt'.")
    except Exception as e:
        raise Exception(f"Error loading instruction file: {e}")

def draft_email(previous_email=None):
    """Draft an email using OpenAI's thread API."""
    instruction = load_instruction()

    context = f"Previous email wording:\n{previous_email}\n\n" if previous_email else ""
    prompt = f"{instruction}\n\n{context}Draft a uniquely worded new email accordingly."

    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=os.getenv("OPENAI_ASSISTANT_ID")
    )

    # Polling until the run completes
    while True:
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        if run_status.status == "completed":
            break

    messages = client.beta.threads.messages.list(thread_id=thread.id)
    email_text = messages.data[0].content[0].text.value.strip()

    return email_text

def validate_email(email_text):
    """Validate an email's tone, clarity, and professionalism."""
    validation_prompt = (
        f"Review the following email for tone, clarity, and professionalism. "
        f"If acceptable, reply with 'APPROVED' followed by the refined email."
         f"make sure there are no fillable fields in the email such as [Your Email Address] [Your Contact Number] [Your Contact Information] remove any information between square brackets. "
        f"Otherwise, make improvements:\n\n{email_text}"
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a professional editor and quality checker."},
            {"role": "user", "content": validation_prompt}
        ],
        temperature=1,
    )

    result = response.choices[0].message.content

    if "APPROVED" in result:
        approved_text = result.split('APPROVED', 1)[1].strip()
        return approved_text
    else:
        print("Validation failed. AI feedback:\n", result)
        return None
    
def generate_subject(content=None):
    """Generate a subject line for the email."""
    subject_prompt = (
        "Generate a subject line for the following email content:\n\n"
        f"{content}"
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional email subject line generator."},
            {"role": "user", "content": subject_prompt}
        ],
        temperature=1,
    )

    return response.choices[0].message.content.strip()

def reset_thread():
    """Reset the conversation history by creating a new thread."""
    global thread
    thread = client.beta.threads.create()
