import streamlit as st
import json
from datetime import datetime
from llm_service import LLMService, MockLLMService
from ingestion import generate_mock_emails
import storage

# Page configuration
st.set_page_config(
    page_title="Email Productivity Agent",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .email-card {
        padding: 1.5rem;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    .email-card:hover {
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(102, 126, 234, 0.5);
        transform: translateY(-2px);
    }
    .category-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 0.5rem;
    }
    .important { background-color: #ef4444; color: white; }
    .newsletter { background-color: #3b82f6; color: white; }
    .spam { background-color: #6b7280; color: white; }
    .to-do { background-color: #10b981; color: white; }
    .uncategorized { background-color: #f59e0b; color: white; }
    
    .chat-message { padding: 1rem; border-radius: 10px; margin-bottom: 0.5rem; }
    .user-message { background-color: rgba(102, 126, 234, 0.2); margin-left: 2rem; }
    .agent-message { background-color: rgba(118, 75, 162, 0.2); margin-right: 2rem; }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'selected_email_id' not in st.session_state:
    st.session_state.selected_email_id = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'llm_provider' not in st.session_state:
    st.session_state.llm_provider = "mock"
if 'llm_service' not in st.session_state:
    if st.session_state.llm_provider == "mock":
        st.session_state.llm_service = MockLLMService()
    else:
        st.session_state.llm_service = LLMService(provider=st.session_state.llm_provider)

# Load Data on Startup
if 'emails' not in st.session_state:
    emails = storage.load_emails()
    if not emails:
        emails = generate_mock_emails(20)
        storage.save_emails(emails)
    st.session_state.emails = emails

if 'prompts' not in st.session_state:
    st.session_state.prompts = storage.load_prompts()

if 'drafts' not in st.session_state:
    st.session_state.drafts = storage.load_drafts()

def get_category_class(category: str) -> str:
    return category.lower().replace("-", "_")

def render_email_card(email, is_selected=False):
    category_class = get_category_class(email['category'])
    card_style = "border: 2px solid #667eea;" if is_selected else ""
    
    action_count = len(email.get('action_items', []))
    
    st.markdown(f"""
    <div class="email-card" style="{card_style}">
        <div>
            <span class="category-badge {category_class}">{email['category']}</span>
            <strong style="font-size: 1.1rem;">{email['subject']}</strong>
        </div>
        <div style="margin-top: 0.5rem; color: #9ca3af;">
            From: {email['sender']} | {email['timestamp'].strftime('%Y-%m-%d %H:%M')}
        </div>
        {f'<div style="margin-top: 0.5rem;">📋 {action_count} action item(s)</div>' if action_count > 0 else ''}
    </div>
    """, unsafe_allow_html=True)

def main():
    st.sidebar.markdown("## 📧 Email Productivity Agent")
    
    # LLM Provider Selection
    st.sidebar.markdown("### 🤖 LLM Provider")
    llm_options = ["mock", "openai", "gemini", "huggingface"]
    llm_labels = {
        "mock": "Mock (Testing)",
        "openai": "OpenAI GPT",
        "gemini": "Google Gemini",
        "huggingface": "Hugging Face"
    }
    
    selected_provider = st.sidebar.selectbox(
        "Select LLM",
        llm_options,
        format_func=lambda x: llm_labels[x],
        index=llm_options.index(st.session_state.llm_provider)
    )
    
    if selected_provider != st.session_state.llm_provider:
        st.session_state.llm_provider = selected_provider
        if selected_provider == "mock":
            st.session_state.llm_service = MockLLMService()
        else:
            try:
                st.session_state.llm_service = LLMService(provider=selected_provider)
                st.sidebar.success(f"✅ Switched to {llm_labels[selected_provider]}")
            except Exception as e:
                st.sidebar.error(f"❌ Error: {str(e)}")
                st.session_state.llm_provider = "mock"
                st.session_state.llm_service = MockLLMService()
        st.rerun()
    
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio(
        "Navigation",
        ["📥 Inbox", "🔧 Prompt Brain", "📝 Review Drafts", "⚙️ Settings"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.metric("Total Emails", len(st.session_state.emails))
    st.sidebar.metric("Drafts", len(st.session_state.drafts))
    
    if page == "📥 Inbox":
        render_inbox_page()
    elif page == "🔧 Prompt Brain":
        render_prompt_brain_page()
    elif page == "📝 Review Drafts":
        render_drafts_page()
    elif page == "⚙️ Settings":
        render_settings_page()

def render_inbox_page():
    st.markdown('<h1 class="main-header">📥 Email Inbox</h1>', unsafe_allow_html=True)
    
    # Categorize Button
    if st.button("✨ Categorize All Emails"):
        with st.spinner("Categorizing emails using AI..."):
            service = st.session_state.llm_service
            prompt_template = st.session_state.prompts["Categorization"]["template"]
            
            progress_bar = st.progress(0)
            for i, email in enumerate(st.session_state.emails):
                try:
                    category = service.categorize_email(email['subject'], email['body'], prompt_template)
                    email['category'] = category
                except Exception as e:
                    st.error(f"Error categorizing email {email['id']}: {str(e)}")
                    email['category'] = "Uncategorized"
                progress_bar.progress((i + 1) / len(st.session_state.emails))
            
            storage.save_emails(st.session_state.emails)
            st.success("✅ Categorization Complete!")
            st.rerun()

    # Filters
    col1, col2 = st.columns([2, 1])
    with col1:
        search = st.text_input("🔍 Search emails", placeholder="Search...")
    with col2:
        # Extract unique categories from emails dynamically
        unique_categories = sorted(set(email['category'] for email in st.session_state.emails))
        categories = ["All"] + unique_categories
        selected_category = st.selectbox("Filter by Category", categories)

    # Filter Logic
    filtered_emails = st.session_state.emails
    if selected_category != "All":
        filtered_emails = [e for e in filtered_emails if e['category'] == selected_category]
    if search:
        term = search.lower()
        filtered_emails = [e for e in filtered_emails if term in e['subject'].lower() or term in e['sender'].lower() or term in e['body'].lower()]
    
    # Sort by time desc
    filtered_emails.sort(key=lambda x: x['timestamp'], reverse=True)

    # Layout
    col_list, col_detail = st.columns([1, 2])
    
    with col_list:
        st.markdown(f"### Emails ({len(filtered_emails)})")
        for email in filtered_emails:
            with st.container():
                if st.button(f"📧 {email['id']}", key=f"btn_{email['id']}", use_container_width=True):
                    st.session_state.selected_email_id = email['id']
                    st.session_state.chat_history = []
                    st.rerun()
                render_email_card(email, is_selected=(st.session_state.selected_email_id == email['id']))
    
    with col_detail:
        if st.session_state.selected_email_id:
            selected_email = next((e for e in st.session_state.emails if e['id'] == st.session_state.selected_email_id), None)
            if selected_email:
                render_email_detail(selected_email)
            else:
                st.warning("Email not found. It may have been filtered out.")
        else:
            st.info("Select an email to view details.")

def render_email_detail(email):
    st.markdown("### 📧 Email Details")
    
    category_class = get_category_class(email['category'])
    st.markdown(f"""
    <div style="background: rgba(255,255,255,0.05); padding: 1.5rem; border-radius: 10px;">
        <div><span class="category-badge {category_class}">{email['category']}</span></div>
        <h3>{email['subject']}</h3>
        <p style="color: #9ca3af;">From: {email['sender']}</p>
        <p style="color: #9ca3af;">Date: {email['timestamp'].strftime('%Y-%m-%d %H:%M')}</p>
        <hr style="border-color: rgba(255,255,255,0.1);">
        <p style="white-space: pre-wrap;">{email['body']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if email.get('action_items'):
        st.markdown("### 📋 Action Items")
        for item in email['action_items']:
            st.markdown(f"- {item}")

    st.markdown("---")
    st.markdown("### 🤖 Agent Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📝 Summarize"):
            process_agent_query(email, "Summarize this email")
            
    with col2:
        if st.button("✍️ Draft Reply"):
            process_agent_query(email, "Draft a professional reply to this email", save_draft=True)
            
    with col3:
        if st.button("📋 Extract Tasks"):
            with st.spinner("Extracting tasks..."):
                service = st.session_state.llm_service
                prompt = st.session_state.prompts["Action Extraction"]["template"]
                try:
                    actions = service.extract_action_items(email['subject'], email['body'], prompt)
                    
                    # Update email
                    email['action_items'] = actions
                    storage.save_emails(st.session_state.emails)
                    
                    # Show in chat
                    st.session_state.chat_history.append({
                        'role': 'agent',
                        'content': f"I've extracted the following tasks:\n" + "\n".join([f"- {t}" for t in actions]) if actions else "No specific action items found."
                    })
                except Exception as e:
                    st.session_state.chat_history.append({
                        'role': 'agent',
                        'content': f"Error extracting tasks: {str(e)}"
                    })
                st.rerun()

    # Chat Interface
    st.markdown("### 💬 Chat with Agent")
    
    for msg in st.session_state.chat_history:
        role_class = "user-message" if msg['role'] == 'user' else "agent-message"
        icon = "👤" if msg['role'] == 'user' else "🤖"
        st.markdown(f'<div class="chat-message {role_class}">{icon} {msg["content"]}</div>', unsafe_allow_html=True)
        
        if 'draft_data' in msg:
             with st.expander("📝 View Generated Draft"):
                 st.text(f"Subject: {msg['draft_data']['subject']}")
                 st.text_area("Body", msg['draft_data']['body'], height=150, key=f"draft_view_{id(msg)}")
                 if st.button("💾 Save to Drafts", key=f"save_{id(msg)}"):
                     storage.add_draft(email['id'], msg['draft_data']['subject'], msg['draft_data']['body'])
                     st.session_state.drafts = storage.load_drafts()
                     st.success("✅ Draft saved!")
                     st.rerun()

    user_query = st.text_input("Ask a question about this email:", key="chat_input")
    if st.button("Send") and user_query:
        process_agent_query(email, user_query)
        st.rerun()

def process_agent_query(email, query, save_draft=False):
    st.session_state.chat_history.append({'role': 'user', 'content': query})
    
    service = st.session_state.llm_service
    
    # Prepare context
    context = {
        'sender': email['sender'],
        'subject': email['subject'],
        'body': email['body'],
        'category': email['category'],
        'action_items': json.dumps(email.get('action_items', []))
    }
    
    # Simple prompts dict for the service
    prompts_dict = {k: v['template'] for k, v in st.session_state.prompts.items()}
    
    with st.spinner("Thinking..."):
        try:
            result = service.chat_with_agent(query, context, prompts_dict)
            agent_msg = {'role': 'agent', 'content': result['response']}
            
            if result.get('action') == 'draft_generated' and result.get('data'):
                agent_msg['draft_data'] = result['data']
                
                # Auto-save draft if requested
                if save_draft:
                    storage.add_draft(email['id'], result['data']['subject'], result['data']['body'])
                    st.session_state.drafts = storage.load_drafts()
                    agent_msg['content'] += "\n\n✅ Draft has been saved to Review Drafts."
                
            st.session_state.chat_history.append(agent_msg)
        except Exception as e:
            st.session_state.chat_history.append({
                'role': 'agent',
                'content': f"Error: {str(e)}"
            })

def render_prompt_brain_page():
    st.markdown('<h1 class="main-header">🔧 Prompt Brain</h1>', unsafe_allow_html=True)
    
    prompts = st.session_state.prompts
    tabs = st.tabs(list(prompts.keys()))
    
    for i, (name, data) in enumerate(prompts.items()):
        with tabs[i]:
            st.markdown(f"*{data['description']}*")
            new_template = st.text_area("Template", value=data['template'], height=200, key=f"prompt_{name}")
            
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button(f"💾 Save {name} Prompt"):
                    prompts[name]['template'] = new_template
                    storage.save_prompts(prompts)
                    st.session_state.prompts = storage.load_prompts()  # Reload from storage to ensure sync
                    st.success(f"✅ {name} prompt saved and will be used immediately!")
                    st.info("💡 Click 'Categorize All Emails' to apply changes to existing emails.")
            
            with col2:
                if st.button(f"🔄 Reset {name} Default"):
                    default_template = storage.DEFAULT_PROMPTS[name]['template']
                    prompts[name]['template'] = default_template
                    storage.save_prompts(prompts)
                    st.session_state.prompts = storage.load_prompts()
                    # Force update the widget state to reflect the change
                    st.session_state[f"prompt_{name}"] = default_template
                    st.rerun()

def render_drafts_page():
    st.markdown('<h1 class="main-header">📝 Review Drafts</h1>', unsafe_allow_html=True)
    
    drafts = st.session_state.drafts
    
    if not drafts:
        st.info("No drafts yet. Generate drafts using the 'Draft Reply' button in the Inbox.")
        return
    
    st.markdown(f"### You have {len(drafts)} draft(s)")
    
    for draft in reversed(drafts):  # Show newest first
        email = next((e for e in st.session_state.emails if e['id'] == draft['email_id']), None)
        
        with st.expander(f"📧 Draft #{draft['id']}: {draft['subject']}"):
            if email:
                st.markdown(f"**In reply to:** {email['subject']}")
                st.markdown(f"**Original sender:** {email['sender']}")
                st.markdown("---")
            
            with st.form(key=f"draft_form_{draft['id']}"):
                subject = st.text_input("Subject", value=draft['subject'])
                body = st.text_area("Body", value=draft['body'], height=200)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.form_submit_button("💾 Save Changes"):
                        # Update draft
                        for d in st.session_state.drafts:
                            if d['id'] == draft['id']:
                                d['subject'] = subject
                                d['body'] = body
                        storage.save_drafts(st.session_state.drafts)
                        st.success("✅ Draft updated!")
                        st.rerun()
                
                with col2:
                    if st.form_submit_button("🗑️ Delete"):
                        st.session_state.drafts = [d for d in st.session_state.drafts if d['id'] != draft['id']]
                        storage.save_drafts(st.session_state.drafts)
                        st.success("🗑️ Draft deleted!")
                        st.rerun()

def render_settings_page():
    st.markdown('<h1 class="main-header">⚙️ Settings</h1>', unsafe_allow_html=True)
    
    st.markdown("### 🔄 Data Management")
        
    if st.button("🗑️ Reset All Data (Clear Emails & Drafts)"):
        st.session_state.emails = []
        st.session_state.drafts = []
        storage.save_emails([])
        storage.save_drafts([])
        st.success("✅ Cleared!")
        st.rerun()

    st.markdown("---")
    st.markdown("### About")
    st.markdown("**Email Productivity Agent v1.0** (JSON Edition)")
    st.markdown(f"**Current LLM:** {st.session_state.llm_provider.upper()}")

if __name__ == "__main__":
    main()
