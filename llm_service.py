import os
import json
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    """
    Service to handle LLM interactions for email processing.
    Supports OpenAI, Google Gemini, and Hugging Face.
    """
    
    def __init__(self, provider: str = "openai"):
        self.provider = provider.lower()
        
        if self.provider == "openai":
            import openai
            self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            self.model = os.getenv("OPENAI_MODEL", "gpt-4")
        elif self.provider == "gemini":
            import google.generativeai as genai
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            self.model = genai.GenerativeModel(os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite"))
        elif self.provider == "huggingface":
            from huggingface_hub import InferenceClient
            self.client = InferenceClient(token=os.getenv("HUGGINGFACE_API_KEY"))
            # Use a good instruction-tuned model that is free/available on Inference API
            self.model = os.getenv("HUGGINGFACE_MODEL", "mistralai/Mistral-7B-Instruct-v0.2")
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    def _call_llm(self, prompt: str) -> str:
        """Call the configured LLM with the given prompt."""
        try:
            if self.provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a helpful email assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )
                return response.choices[0].message.content.strip()
            
            elif self.provider == "gemini":
                response = self.model.generate_content(prompt)
                return response.text.strip()
            
            elif self.provider == "huggingface":
                # Using text-generation for HF
                response = self.client.text_generation(
                    prompt,
                    model=self.model,
                    max_new_tokens=500,
                    temperature=0.7,
                    return_full_text=False
                )
                return response.strip()
                
        except Exception as e:
            print(f"LLM Error ({self.provider}): {str(e)}")
            return f"Error calling LLM: {str(e)}"
    
    def categorize_email(self, email_subject: str, email_body: str, prompt_template: str) -> str:
        """
        Categorize an email using the provided prompt template.
        Returns: Category name as determined by the LLM based on the prompt
        """
        full_prompt = f"{prompt_template}\n\nEmail Subject: {email_subject}\nEmail Body: {email_body}\n\nCategory:"
        response = self._call_llm(full_prompt)
        
        # Clean up response to get just the category name
        # Remove quotes, extra whitespace, and take only the first line
        category = response.strip().strip('"').strip("'").split('\n')[0].strip()
        
        # Remove any common prefixes like "Category: " or "Answer: "
        for prefix in ["Category:", "Answer:", "Response:"]:
            if category.startswith(prefix):
                category = category[len(prefix):].strip()
        
        # Return the category name, or "Uncategorized" if empty
        return category if category else "Uncategorized"
    
    def extract_action_items(self, email_subject: str, email_body: str, prompt_template: str) -> list:
        """
        Extract action items from an email.
        Returns: List of action items
        """
        full_prompt = f"{prompt_template}\n\nEmail Subject: {email_subject}\nEmail Body: {email_body}\n\nAction Items (JSON):"
        response = self._call_llm(full_prompt)
        
        try:
            # Clean response to find JSON content
            response = response.strip()
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                response = response.split("```")[1].split("```")[0].strip()
                
            # Try to parse as JSON
            if response.startswith('['):
                return json.loads(response)
            else:
                # Extract JSON from response if it's embedded in text
                start_idx = response.find('[')
                end_idx = response.rfind(']') + 1
                if start_idx != -1 and end_idx != 0:
                    return json.loads(response[start_idx:end_idx])
                else:
                    # Return as single item list if not JSON but has content
                    return [line.strip("- *") for line in response.split('\n') if line.strip()] if response else []
        except json.JSONDecodeError:
            # If parsing fails, return as list of lines
            return [line.strip("- *") for line in response.split('\n') if line.strip()]
    
    def generate_draft(self, email_subject: str, email_body: str, email_sender: str, 
                      prompt_template: str, user_instruction: Optional[str] = None) -> Dict[str, str]:
        """
        Generate a draft reply to an email.
        Returns: Dict with 'subject' and 'body'
        """
        context = f"Original Email:\nFrom: {email_sender}\nSubject: {email_subject}\nBody: {email_body}"
        
        if user_instruction:
            full_prompt = f"{prompt_template}\n\n{context}\n\nUser Instructions: {user_instruction}\n\nPlease provide a subject line and body for the reply."
        else:
            full_prompt = f"{prompt_template}\n\n{context}\n\nPlease provide a subject line and body for the reply."
        
        response = self._call_llm(full_prompt)
        
        # Parse the response to extract subject and body
        subject = f"Re: {email_subject}"
        body = response
        
        # Try to extract subject if mentioned
        lines = response.split('\n')
        for i, line in enumerate(lines):
            if 'subject:' in line.lower():
                subject = line.split(':', 1)[1].strip()
                body = '\n'.join(lines[i+1:]).strip()
                break
        
        return {
            "subject": subject,
            "body": body
        }
    
    def chat_with_agent(self, query: str, email_context: Dict[str, Any], 
                       prompts: Dict[str, str]) -> Dict[str, Any]:
        """
        Handle conversational queries about an email.
        Returns: Dict with 'response', 'action', and optional 'data'
        """
        email_info = f"""
Email Context:
From: {email_context.get('sender', 'Unknown')}
Subject: {email_context.get('subject', 'No Subject')}
Body: {email_context.get('body', 'No content')}
Category: {email_context.get('category', 'Uncategorized')}
Action Items: {email_context.get('action_items', '[]')}
"""
        
        query_lower = query.lower()
        
        # Handle summarization
        if "summarize" in query_lower or "summary" in query_lower:
            prompt = f"Please provide a concise summary of the following email:\n{email_info}"
            response = self._call_llm(prompt)
            return {
                "response": response,
                "action": "none"
            }
        
        # Handle draft generation
        if "draft" in query_lower or "reply" in query_lower:
            draft_data = self.generate_draft(
                email_context.get('subject', ''),
                email_context.get('body', ''),
                email_context.get('sender', ''),
                prompts.get('Auto-Reply', 'Draft a professional reply.'),
                user_instruction=query
            )
            return {
                "response": "I've generated a draft reply for you.",
                "action": "draft_generated",
                "data": draft_data
            }
        
        # Handle task/action queries
        if "task" in query_lower or "action" in query_lower or "do" in query_lower:
            action_items = email_context.get('action_items', '[]')
            if isinstance(action_items, str):
                try:
                    action_items = json.loads(action_items)
                except:
                    action_items = []
            
            if action_items:
                response = f"Here are the action items extracted from this email:\n" + \
                          "\n".join([f"• {item}" for item in action_items])
            else:
                response = "No specific action items were found in this email."
            
            return {
                "response": response,
                "action": "none"
            }
        
        # General query
        prompt = f"{email_info}\n\nUser Question: {query}\n\nPlease answer based on the email context."
        response = self._call_llm(prompt)
        
        return {
            "response": response,
            "action": "none"
        }


# Mock LLM Service for testing without API keys
class MockLLMService:
    """Mock service for development/testing without actual API calls."""
    
    def categorize_email(self, email_subject: str, email_body: str, prompt_template: str) -> str:
        """Mock categorization logic that tries to respect the prompt template."""
        email_lower = (email_subject + " " + email_body).lower()
        
        # Try to extract categories from the prompt template
        categories_in_prompt = []
        if "categories:" in prompt_template.lower():
            # Extract text after "categories:"
            parts = prompt_template.lower().split("categories:")
            if len(parts) > 1:
                category_text = parts[1].split(".")[0]  # Get text until first period
                # Extract words that look like categories (capitalized words or comma-separated)
                import re
                categories_in_prompt = re.findall(r'\b[A-Z][a-z]+(?:\s+and\s+[A-Z][a-z]+)*', prompt_template)
        
        # Simple keyword-based categorization as fallback
        if "urgent" in email_lower or "important" in email_lower or "deadline" in email_lower or "critical" in email_lower:
            return categories_in_prompt[0] if categories_in_prompt and len(categories_in_prompt) > 0 else "Important"
        elif "newsletter" in email_lower or "weekly" in email_lower or "subscribe" in email_lower or "unsubscribe" in email_lower:
            return categories_in_prompt[1] if categories_in_prompt and len(categories_in_prompt) > 1 else "Newsletter"
        elif "spam" in email_lower or "winner" in email_lower or "claim" in email_lower or "congratulations" in email_lower or "lottery" in email_lower:
            return categories_in_prompt[2] if categories_in_prompt and len(categories_in_prompt) > 2 else "Spam"
        elif "meeting" in email_lower or "task" in email_lower or "please" in email_lower or "review" in email_lower or "approve" in email_lower:
            return categories_in_prompt[3] if categories_in_prompt and len(categories_in_prompt) > 3 else "To-Do"
        elif "birthday" in email_lower or "friend" in email_lower or "family" in email_lower or "lunch" in email_lower:
            return "Friends and Family" if "friends and family" in prompt_template.lower() else "Uncategorized"
        else:
            return "Uncategorized"
    
    def extract_action_items(self, email_subject: str, email_body: str, prompt_template: str) -> list:
        """Mock action item extraction."""
        actions = []
        email_text = email_body.lower()
        
        if "deadline" in email_text or "by friday" in email_text:
            actions.append("Complete task by deadline")
        if "send" in email_text or "submit" in email_text:
            actions.append("Send/submit requested items")
        if "meeting" in email_text:
            actions.append("Schedule or attend meeting")
        if "review" in email_text:
            actions.append("Review document/material")
        
        return actions if actions else []
    
    def generate_draft(self, email_subject: str, email_body: str, email_sender: str, 
                      prompt_template: str, user_instruction: Optional[str] = None) -> Dict[str, str]:
        """Mock draft generation."""
        return {
            "subject": f"Re: {email_subject}",
            "body": f"Dear {email_sender},\n\nThank you for your email regarding '{email_subject}'.\n\n"
                   f"I have received your message and will address it accordingly.\n\n"
                   f"{'User note: ' + user_instruction if user_instruction else ''}\n\n"
                   f"Best regards,\n[Your Name]"
        }
    
    def chat_with_agent(self, query: str, email_context: Dict[str, Any], 
                       prompts: Dict[str, str]) -> Dict[str, Any]:
        """Mock chat agent."""
        query_lower = query.lower()
        
        if "summarize" in query_lower or "summary" in query_lower:
            return {
                "response": f"Summary: This email from {email_context.get('sender', 'Unknown')} "
                           f"discusses '{email_context.get('subject', 'No Subject')}'. "
                           f"The main points include the content shared in the email body.",
                "action": "none"
            }
        
        if "draft" in query_lower or "reply" in query_lower:
            draft_data = self.generate_draft(
                email_context.get('subject', ''),
                email_context.get('body', ''),
                email_context.get('sender', ''),
                prompts.get('Auto-Reply', ''),
                user_instruction=query
            )
            return {
                "response": "I've generated a draft reply for you.",
                "action": "draft_generated",
                "data": draft_data
            }
        
        if "task" in query_lower or "action" in query_lower:
            action_items = email_context.get('action_items', '[]')
            if isinstance(action_items, str):
                try:
                    action_items = json.loads(action_items)
                except:
                    action_items = []
            
            if action_items:
                response = "Action items:\n" + "\n".join([f"• {item}" for item in action_items])
            else:
                response = "No specific action items found."
            
            return {"response": response, "action": "none"}
        
        return {
            "response": "I can help you summarize this email, draft a reply, or extract tasks. What would you like?",
            "action": "none"
        }


def get_llm_service(use_mock: bool = False) -> Any:
    """Factory function to get appropriate LLM service."""
    if use_mock:
        return MockLLMService()
    
    # Check if API keys are available
    openai_key = os.getenv("OPENAI_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")
    hf_key = os.getenv("HUGGINGFACE_API_KEY")
    
    if openai_key:
        return LLMService(provider="openai")
    elif gemini_key:
        return LLMService(provider="gemini")
    elif hf_key:
        return LLMService(provider="huggingface")
    else:
        # Fallback to mock if no keys available
        print("No API keys found. Using mock LLM service.")
        return MockLLMService()
