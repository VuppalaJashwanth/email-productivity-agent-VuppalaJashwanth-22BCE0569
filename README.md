# Email Productivity Agent 📧

A prompt-driven AI-powered email management system built with Streamlit that helps you categorize emails, extract action items, and generate professional replies using LLM technology.

## 🎯 Features

### Phase 1: Email Ingestion & Knowledge Base
- **Load Mock Emails**: Generate 20 realistic test emails with varied categories (Spam, Important, Newsletter, To-Do, Uncategorized)
- **Prompt Brain**: Create, edit, and save custom AI prompts for:
  - Email categorization (Dynamic categories supported!)
  - Action item extraction
  - Auto-reply draft generation
- **JSON Storage**: Simple, flat-file storage for emails, prompts, and drafts (No database required)

### Phase 2: Email Processing Agent
- **Intelligent Inbox**: View and filter emails by category, sender, or content
- **AI Agent Chat**: Interact with emails using natural language:
  - "Summarize this email"
  - "What tasks do I need to do?"
  - "Draft a reply based on professional tone"
  - Ask any custom questions about the email
- **Action Item Extraction**: Automatically identifies tasks and deadlines

### Phase 3: Draft Generation Agent
- **Smart Draft Creation**: AI generates context-aware email replies
- **Draft Management**: Review, edit, and save generated drafts in the "Review Drafts" page
- **Never Auto-Send**: All drafts are saved for review (safety first!)
- **Thread Context**: Drafts use original email context for relevance

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Virtual environment (recommended)

### Installation

1. **Activate Virtual Environment** (if not already activated):
```bash
.\venv\Scripts\activate
```

2. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure API Keys**:
```bash
# Copy the example file
copy .env.example .env

# Edit .env and add your API keys
# OPENAI_API_KEY=...
# GEMINI_API_KEY=...
# HUGGINGFACE_API_KEY=...
```

4. **Run the Application**:
```bash
streamlit run app.py
```

The application will open automatically in your browser at `http://localhost:8501` (or similar port).

## 📖 User Guide

### 1. Loading Emails
- On first run, 20 mock emails are automatically generated.
- Click **"✨ Categorize All Emails"** in the Inbox to apply AI categorization.

### 2. Viewing Inbox
- Navigate to **"📥 Inbox"** page
- Use filters to find specific emails by category or search terms
- Click on any email to view details

### 3. Interacting with Email Agent
- Select an email from the inbox
- Use quick action buttons:
  - **Summarize**: Get a concise summary
  - **Draft Reply**: Generate a professional response (saved to Drafts)
  - **Extract Tasks**: List all action items
- Or ask custom questions in the chat input

### 4. Managing Prompts ("Prompt Brain")
- Go to **"🔧 Prompt Brain"** page
- Edit the three main prompts:
  - **Categorization**: Add new categories (e.g., "Friends and Family")
  - **Action Extraction**: Customize how tasks are found
  - **Auto-Reply**: Change the default reply tone
- **Save**: Updates take effect immediately.
- **Reset**: Revert to default prompts if needed.

### 5. Working with Drafts
- Navigate to **"📝 Review Drafts"** page
- Review all generated drafts
- Edit draft content as needed
- Delete drafts you don't need

### 6. Settings & Configuration
- Go to **"⚙️ Settings"** page
- **Reset All Data**: Clear all emails and drafts to start fresh.

## 🧠 LLM Integration

The application supports dynamic switching between providers via the sidebar dropdown:

1. **Mock (Testing)**: No API key needed. Uses keyword matching.
2. **OpenAI (GPT)**: Requires `OPENAI_API_KEY`.
3. **Google Gemini**: Requires `GEMINI_API_KEY`.
4. **Hugging Face**: Requires `HUGGINGFACE_API_KEY`.

## 🏗️ Architecture

```
.
├── app.py              # Main Streamlit application
├── llm_service.py      # LLM integration (OpenAI/Gemini/HF/Mock)
├── ingestion.py        # Mock email generation
├── storage.py          # JSON file handling (emails.json, prompts.json, drafts.json)
├── requirements.txt    # Python dependencies
└── .env                # API configuration
```

### Data Storage (JSON)

- **emails.json**: Stores email content, metadata, and categories.
- **prompts.json**: Stores custom prompt templates.
- **drafts.json**: Stores generated drafts.

## 🎨 Key Design Decisions

1. **Streamlit for UI**: Single framework for both frontend and backend
2. **JSON Storage**: Lightweight, portable, no database setup required.
3. **Modular LLM Service**: Easy to switch between providers via UI.
4. **Prompt-Driven**: All AI behavior is customizable via prompts.
5. **Safety First**: Drafts are never auto-sent.

## 🔒 Safety Features

- **No Auto-Send**: Drafts are never sent automatically
- **All Drafts Saved**: Review and edit before sending
- **Mock Mode**: Test without making actual API calls
- **Local Storage**: All data stays on your machine

## 📝 Assignment Requirements Met

✅ **Phase 1**: Email ingestion with prompt storage (JSON)
✅ **Phase 2**: Email processing agent with RAG-style queries
✅ **Phase 3**: Draft generation with safety constraints

### UI Requirements
- ✅ Load and view emails
- ✅ Create and edit prompts
- ✅ Email agent chat interface
- ✅ Draft generation and review

### Backend Requirements
- ✅ Prompt storage (JSON)
- ✅ Processing pipeline (categorization + actions)
- ✅ LLM integration with error handling

### Agent Logic
- ✅ Summarization
- ✅ Reply drafting
- ✅ Task extraction
- ✅ General inbox queries
- ✅ Never auto-sends emails

## 📄 License

MIT License - feel free to use for educational purposes

## 👨‍💻 Development

Built with:
- Python 3.x
- Streamlit
- OpenAI / Google Gemini / Hugging Face APIs
"# email-productivity-agent-VuppalaJashwanth-22BCE0569" 
