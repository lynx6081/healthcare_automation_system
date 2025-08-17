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
        self.crew_manager = HealthCrewManager()
        self.automation_manager = AutomationManager()
        
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
            st.header("📅 Reminders & Events")
            
            # Get current reminders
            current_reminders = self.automation_manager.get_current_reminders()
            
            if current_reminders:
                for reminder in current_reminders:
                    urgency_class = "urgent-reminder" if reminder['urgent'] else "reminder-item"
                    if reminder['completed']:
                        urgency_class = "completed-reminder"
                    
                    st.markdown(f"""
                    <div class="{urgency_class}">
                        <strong>{reminder['type']}</strong><br>
                        {reminder['message']}<br>
                        <small>⏰ {reminder['due_date'].strftime('%Y-%m-%d %H:%M')}</small>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No pending reminders")
            
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
            
            if st.button("🍎 Nutrition Plan", key="nutrition", use_container_width=True):
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
        """Display chat messages"""
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
        """Process the latest user message"""
        if st.session_state.messages and st.session_state.messages[-1]['role'] == 'user':
            user_message = st.session_state.messages[-1]['content']
            
            # Show typing indicator
            with st.spinner('Ruby is thinking...'):
                try:
                    # Get response from crew manager
                    response = self.crew_manager.process_query(user_message)
                    
                    # Add response to chat
                    self.add_assistant_message(response['content'], response.get('agent', 'Ruby'))
                    
                    # Check if automation events should be triggered
                    if 'report' in user_message.lower():
                        self.automation_manager.schedule_follow_up('report_generated')
                    elif 'medication' in user_message.lower():
                        self.automation_manager.schedule_follow_up('medication_check')
                    
                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {str(e)}"
                    self.add_assistant_message(error_msg, 'System')

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
                        self.add_user_message(user_input)
                        self.process_message()
                        st.rerun()
            
            with col_clear:
                if st.button("Clear Chat 🗑️", key="clear_btn", use_container_width=True):
                    st.session_state.messages = []
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
            
            team_members = [
                ("Ruby", "Manager", "🟢 Online"),
                ("Dr. Warren", "Medical", "🟢 Available"),
                ("Dr. Advik", "Performance", "🟢 Available"),
                ("Dr. Carla", "Nutrition", "🟢 Available"),
                ("Rachel", "Physiotherapy", "🟢 Available"),
                ("Neel", "Relations", "🟢 Available")
            ]
            
            for name, role, status in team_members:
                st.markdown(f"""
                <div style="background-color: white; padding: 8px; margin: 4px 0; border-radius: 6px; border-left: 3px solid #007bff;">
                    <strong>{name}</strong><br>
                    <small>{role}</small><br>
                    <small>{status}</small>
                </div>
                """, unsafe_allow_html=True)

if __name__ == "__main__":
    app = ChatApp()
    app.run()