import json
import os
from datetime import datetime


DATA_FILE = "emails.json"
PROMPTS_FILE = "prompts.json"
DRAFTS_FILE = "drafts.json"

DEFAULT_PROMPTS = {
    "Categorization": {
        "description": "Determines the category of incoming emails",
        "template": "Analyze the following email and categorize it into one of these categories: Important, Newsletter, Spam, To-Do. Return only the category name."
    },
    "Action Extraction": {
        "description": "Extracts tasks from emails",
        "template": "Extract any action items or tasks from the following email. Return them as a JSON list of strings. If none, return []."
    },
    "Auto-Reply": {
        "description": "Generates draft replies",
        "template": "Draft a professional and polite reply to the following email. Use the context if provided. Keep it concise and professional."
    }
}

def load_emails():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            # Convert timestamp strings back to datetime objects
            for email in data:
                if 'timestamp' in email and isinstance(email['timestamp'], str):
                    try:
                        email['timestamp'] = datetime.fromisoformat(email['timestamp'])
                    except ValueError:
                        pass
            return data
    except Exception as e:
        print(f"Error loading emails: {e}")
        return []

def save_emails(emails):
    # Convert datetime objects to strings for JSON serialization
    serializable_emails = []
    for email in emails:
        email_copy = email.copy()
        if 'timestamp' in email_copy and isinstance(email_copy['timestamp'], datetime):
            email_copy['timestamp'] = email_copy['timestamp'].isoformat()
        serializable_emails.append(email_copy)
        
    with open(DATA_FILE, 'w') as f:
        json.dump(serializable_emails, f, indent=2)

def load_prompts():
    if not os.path.exists(PROMPTS_FILE):
        save_prompts(DEFAULT_PROMPTS)
        return DEFAULT_PROMPTS
    try:
        with open(PROMPTS_FILE, 'r') as f:
            return json.load(f)
    except:
        return DEFAULT_PROMPTS

def save_prompts(prompts):
    with open(PROMPTS_FILE, 'w') as f:
        json.dump(prompts, f, indent=2)

def load_drafts():
    if not os.path.exists(DRAFTS_FILE):
        return []
    try:
        with open(DRAFTS_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_drafts(drafts):
    with open(DRAFTS_FILE, 'w') as f:
        json.dump(drafts, f, indent=2)

def add_draft(email_id, subject, body):
    drafts = load_drafts()
    draft = {
        "id": len(drafts) + 1,
        "email_id": email_id,
        "subject": subject,
        "body": body,
        "status": "draft",
        "created_at": datetime.now().isoformat()
    }
    drafts.append(draft)
    save_drafts(drafts)
    return draft

