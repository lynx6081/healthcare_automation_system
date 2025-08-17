import streamlit as st
import json 
import datetime as dt
from datetime import datetime, timedelta
import time
import threading
from typing import List, Dict
import os

from crew_manager import HealthCrewManager
from automation import AutomationManager

# Configure page
st.set_page_config(
    page_title="Health AI Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for WhatsApp-style interface
st.markdown("""
<style>
    .chat-container {
        height: 60vh;
        overflow-y: auto;
        padding: 10px;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        background-color: #f5f5f5;
    }
    
    .user-message {
        background-color: #007bff;
        color: white;
        padding: 10px 15px;
        border-radius: 18px;
        margin: 5px 0;
        margin-left: 20%;
        text-align: right;
        word-wrap: break-word;
    }
    
    .ai-message {
        background-color: white;
        color: black;
        padding: 10px 15px;
        border-radius: 18px;
        margin: 5px 0;
        margin-right: 20%;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        word-wrap: break-word;
    }
    
    .timestamp {
        font-size: 0.8em;
        color: #666;
        margin: 2px 0;
    }
    
    .reminder-item {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 8px;
        padding: 10px;
        margin: 5px 0;
    }
    
    .urgent-reminder {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
    }
    
    .completed-reminder {
        background-color: #d1edff;
        border: 1px solid #bee5eb;
        opacity: 0.7;
    }
</style>
""", unsafe_allow_html=True)

class ChatApp:
    def __init__(self):
        # Initialize managers only once using session state
        if 'crew_manager' not in st.session_state:
            st.session_state.crew_manager = HealthCrewManager()
            print("✅ Created new HealthCrewManager instance")
        
        if 'automation_manager' not in st.session_state:
            st.session_state.automation_manager = AutomationManager()
            print("✅ Created new AutomationManager instance")

        # Use the singleton instances
        self.crew_manager = st.session_state.crew_manager
        self.automation_manager = st.session_state.automation_manager

        if 'current_agent' not in st.session_state:
            st.session_state.current_agent = 'Ruby'

        if 'delegation_history' not in st.session_state:
            st.session_state.delegation_history = []
        
        # Initialize session state
        if 'messages' not in st.session_state:
            st.session_state.messages = []
            # Add welcome message
            welcome_msg = {
                'role': 'assistant',
                'content': 'Hello! I\'m Ruby, your health management assistant. I\'m here to help coordinate your care with our expert team. How can I assist you today?',
                'timestamp': datetime.now(),
                'agent': 'Ruby'
            }
            st.session_state.messages.append(welcome_msg)
        
        if 'reminders' not in st.session_state:
            st.session_state.reminders = []
        
        if 'automation_started' not in st.session_state:
            st.session_state.automation_started = False

    def start_automation(self):
        """Start background automation tasks"""
        if not st.session_state.automation_started:
            threading.Thread(target=self.automation_manager.start_automation, daemon=True).start()
            st.session_state.automation_started = True

    def display_sidebar(self):
        """Display reminders and upcoming events in sidebar"""
        with st.sidebar:
            st.header("📅 Automated Reminders")
            
            # Get current reminders
            try:
                current_reminders = self.automation_manager.get_current_reminders()
                
                # Separate automated vs manual reminders
                automated_reminders = [r for r in current_reminders if 'automated' in r.get('tags', [])]
                manual_reminders = [r for r in current_reminders if 'automated' not in r.get('tags', [])]
                
                # Display automated reminders first
                if automated_reminders:
                    st.subheader("🤖 Automated Tasks")
                    for reminder in automated_reminders:
                        st.markdown(f"""
                        <div class="reminder-item" style="border-left: 3px solid #ff9800;">
                            <strong>🤖 {reminder['type']}</strong><br>
                            {reminder['message']}<br>
                            <small>⏰ {reminder['due_date'].strftime('%Y-%m-%d %H:%M')}</small>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No pending reminders")
            except Exception as e:
                st.error(f"Error loading reminders: {e}")
            
            # Quick actions
            st.subheader("⚡ Quick Actions")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📊 Health Report", key="health_report"):
                    self.add_user_message("Generate my current health report")
                    self.process_message()
            
            with col2:
                if st.button("💊 Medication", key="medication"):
                    self.add_user_message("Show my medication schedule")
                    self.process_message()
            
            if st.button("🎯 Nutrition Plan", key="nutrition", use_container_width=True):
                self.add_user_message("Show my current nutrition plan")
                self.process_message()
            
            if st.button("🏃‍♂️ Exercise Plan", key="exercise", use_container_width=True):
                self.add_user_message("Show my current exercise plan")
                self.process_message()

    def add_user_message(self, message: str):
        """Add user message to chat"""
        user_msg = {
            'role': 'user',
            'content': message,
            'timestamp': datetime.now(),
            'agent': 'User'
        }
        st.session_state.messages.append(user_msg)

    def add_assistant_message(self, message: str, agent: str = 'Ruby'):
        """Add assistant message to chat"""
        assistant_msg = {
            'role': 'assistant',
            'content': message,
            'timestamp': datetime.now(),
            'agent': agent
        }
        st.session_state.messages.append(assistant_msg)

    def display_chat(self):
        """Display chat messages with current agent indicator"""
        # Add current agent indicator
        st.markdown(f"""
        <div style="background-color: #e3f2fd; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
            <strong>Currently Active Agent: {st.session_state.current_agent}</strong>
        </div>
        """, unsafe_allow_html=True)
        
        # Display chat messages
        chat_container = st.container()
        
        with chat_container:
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            
            for message in st.session_state.messages:
                timestamp = message['timestamp'].strftime('%H:%M')
                agent = message.get('agent', 'Assistant')
                
                if message['role'] == 'user':
                    st.markdown(f"""
                    <div class="user-message">
                        {message['content']}
                        <div class="timestamp">{timestamp}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="ai-message">
                        <strong>{agent}:</strong> {message['content']}
                        <div class="timestamp">{timestamp}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

    def process_message(self):
        """Process the latest user message with improved error handling"""
        if st.session_state.messages and st.session_state.messages[-1]['role'] == 'user':
            user_message = st.session_state.messages[-1]['content']
        else:
            return
        
        # Show typing indicator with current agent
        with st.spinner(f'{st.session_state.current_agent} is processing your request...'):
            try:
                print(f"🔄 Processing message: {user_message[:50]}...")
                
                # Get response from crew manager
                response = self.crew_manager.process_query(user_message)
                
                print(f"✅ Received response from {response.get('agent', 'Unknown')}")
                
                # Check for delegation info
                if 'delegation_info' in response and response['delegation_info']:
                    delegation_info = response['delegation_info']
                    delegated_agent = delegation_info['agent']
                    reason = delegation_info['reason']
                    
                    if delegated_agent != st.session_state.current_agent:
                        # Show delegation message
                        delegation_msg = f"Ruby is delegating this query to {delegated_agent} for {reason}."
                        self.add_assistant_message(delegation_msg, 'Ruby')
                        
                        # Update current agent
                        st.session_state.current_agent = delegated_agent
                        st.session_state.delegation_history.append({
                            'from': 'Ruby',
                            'to': delegated_agent,
                            'query': user_message,
                            'timestamp': datetime.now()
                        })
                        print(f"🔄 Delegated to {delegated_agent}")
                
                # Add response to chat
                agent_name = response.get('agent', st.session_state.current_agent)
                self.add_assistant_message(response['content'], agent_name)
                
                # Handle automation triggers if needed
                if response.get('automated', False):
                    print(f"🤖 Automated task triggered: {response.get('task_type', 'unknown')}")
                
            except Exception as e:
                print(f"❌ Error processing message: {str(e)}")
                error_msg = f"I apologize, but I encountered an issue processing your request. Let me provide you with a direct response instead."
                
                # Provide a better fallback response
                fallback_response = self.crew_manager.fallback_response(user_message)
                self.add_assistant_message(fallback_response['content'], fallback_response['agent'])

    def detect_delegation(self, response_content):
        """Detect agent delegation from response content"""
        content_lower = response_content.lower()
        
        if any(phrase in content_lower for phrase in ['dr warren', 'medical strategist', 'medical expert']):
            return 'Dr Warren'
        elif any(phrase in content_lower for phrase in ['advik', 'performance scientist', 'data analysis']):
            return 'Advik'  
        elif any(phrase in content_lower for phrase in ['carla', 'nutritionist', 'nutrition expert']):
            return 'Carla'
        elif any(phrase in content_lower for phrase in ['rachel', 'physiotherapist', 'exercise expert']):
            return 'Rachel'
        elif any(phrase in content_lower for phrase in ['neel', 'customer success', 'relationship manager']):
            return 'Neel'
        
        return None
    
    def run(self):
        """Main application runner"""
        st.title("🏥 Health AI Assistant")
        st.subheader("Your Personal Health Management Team")
        
        # Start automation
        self.start_automation()
        
        # Display sidebar
        self.display_sidebar()
        
        # Main chat area
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Display chat
            self.display_chat()
            
            # Input area
            st.markdown("---")
            
            # Text input
            user_input = st.text_input(
                "Type your message...", 
                key="user_input",
                placeholder="Ask me anything about your health..."
            )
            
            # Send button
            col_send, col_clear = st.columns([1, 1])
            
            with col_send:
                if st.button("Send 📤", key="send_btn", use_container_width=True):
                    if user_input:
                        print(f"📨 User input: {user_input}")
                        self.add_user_message(user_input)
                        self.process_message()
                        st.rerun()
            
            with col_clear:
                if st.button("Clear Chat 🗑️", key="clear_btn", use_container_width=True):
                    st.session_state.messages = []
                    st.session_state.current_agent = 'Ruby'
                    st.session_state.delegation_history = []
                    # Add welcome message back
                    welcome_msg = {
                        'role': 'assistant',
                        'content': 'Hello! I\'m Ruby, your health management assistant. How can I assist you today?',
                        'timestamp': datetime.now(),
                        'agent': 'Ruby'
                    }
                    st.session_state.messages.append(welcome_msg)
                    st.rerun()

        with col2:
            # Team status
            st.subheader("👥 Team Status")
            
            try:
                team_status = self.crew_manager.get_agent_status()
                if team_status:
                    for agent_name, status in team_status.items():
                        status_color = "🟢" if status.get('available', True) else "🔴"
                        st.markdown(f"""
                        <div style="background-color: white; padding: 8px; margin: 4px 0; border-radius: 6px; border-left: 3px solid #007bff;">
                            <strong>{agent_name}</strong><br>
                            <small>{status.get('role', 'Unknown')}</small><br>
                            <small>{status_color} Available</small>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("Team status unavailable")
            except Exception as e:
                st.error(f"Error loading team status: {str(e)}")

if __name__ == "__main__":
    app = ChatApp()
    app.run()