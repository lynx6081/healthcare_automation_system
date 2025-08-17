import streamlit as st
import json
from datetime import datetime
from typing import Dict, Any, List
import pandas as pd

# Import your existing agents (assuming they're in agents.py)
try:
    from agents import Ruby, drwarren, advik, Carla, Rachel, Neel
    AGENTS_LOADED = True
    IMPORT_ERROR = None
except ImportError as e:
    st.error(f"Could not import agents. Error: {str(e)}")
    AGENTS_LOADED = False
    IMPORT_ERROR = str(e)
except Exception as e:
    st.error(f"Error loading agents: {str(e)}")
    AGENTS_LOADED = False
    IMPORT_ERROR = str(e)

# Configure Streamlit page
st.set_page_config(
    page_title="CrewAI Healthcare Team",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'selected_agent' not in st.session_state:
    st.session_state.selected_agent = "Ruby"
if 'task_results' not in st.session_state:
    st.session_state.task_results = {}

# Agent information mapping
AGENT_INFO = {
    "Ruby": {
        "emoji": "💼",
        "title": "Ms Ruby - Manager & Concierge",
        "description": "Logistics coordination, scheduling, and client experience management",
        "agent_obj": Ruby if AGENTS_LOADED else None
    },
    "Dr Warren": {
        "emoji": "👨‍⚕️",
        "title": "Dr Warren - Senior Medical Specialist",
        "description": "Medical analysis, lab results, and health strategy",
        "agent_obj": drwarren if AGENTS_LOADED else None
    },
    "Dr Advik": {
        "emoji": "📊",
        "title": "Dr Advik - Performance Scientist",
        "description": "Wearable data analysis, sleep, recovery, and performance insights",
        "agent_obj": advik if AGENTS_LOADED else None
    },
    "Dr Carla": {
        "emoji": "🥗",
        "title": "Dr Carla - Nutritionist",
        "description": "Biomarker-driven meal plans and nutrition optimization",
        "agent_obj": Carla if AGENTS_LOADED else None
    },
    "Rachel": {
        "emoji": "💪",
        "title": "Rachel - Elite Physiotherapist",
        "description": "Training programs, mobility, and movement optimization",
        "agent_obj": Rachel if AGENTS_LOADED else None
    },
    "Neel": {
        "emoji": "🎯",
        "title": "Neel - Relationship Strategist",
        "description": "Strategic reviews, client relations, and value alignment",
        "agent_obj": Neel if AGENTS_LOADED else None
    }
}

def execute_agent_task(agent_name: str, query: str) -> Dict[str, Any]:
    """Execute a task with the selected agent"""
    if not AGENTS_LOADED:
        return {
            "success": False,
            "result": "Agents not loaded. Please check your agents.py file.",
            "timestamp": datetime.now().isoformat()
        }
    
    try:
        agent = AGENT_INFO[agent_name]["agent_obj"]
        
        # For demonstration purposes, we'll simulate agent execution
        # In your actual implementation, you would call the agent's execute method
        # result = agent.execute(query)
        
        # Simulated response (replace with actual agent execution)
        simulated_result = f"[{agent_name}] Processing query: '{query}'\n\nThis is a simulated response. In the actual implementation, this would be the agent's response to your query."
        
        return {
            "success": True,
            "result": simulated_result,
            "agent": agent_name,
            "timestamp": datetime.now().isoformat(),
            "query": query
        }
    except Exception as e:
        return {
            "success": False,
            "result": f"Error executing agent task: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

def add_to_conversation_history(agent_name: str, query: str, result: str):
    """Add interaction to conversation history"""
    st.session_state.conversation_history.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "agent": agent_name,
        "query": query,
        "result": result
    })

# Main app layout
st.title("🏥 CrewAI Healthcare Team Dashboard")
st.markdown("---")

# Sidebar for agent selection and controls
with st.sidebar:
    st.header("🎛️ Control Panel")
    
    # Agent selection
    st.subheader("Select Agent")
    agent_options = list(AGENT_INFO.keys())
    selected_agent = st.selectbox(
        "Choose an agent to interact with:",
        agent_options,
        index=agent_options.index(st.session_state.selected_agent)
    )
    st.session_state.selected_agent = selected_agent
    
    # Display selected agent info
    agent_info = AGENT_INFO[selected_agent]
    st.info(f"**{agent_info['emoji']} {agent_info['title']}**\n\n{agent_info['description']}")
    
    st.markdown("---")
    
    # Conversation controls
    st.subheader("💬 Conversation")
    if st.button("Clear History", type="secondary"):
        st.session_state.conversation_history = []
        st.rerun()
    
    # Export conversation
    if st.session_state.conversation_history:
        conversation_json = json.dumps(st.session_state.conversation_history, indent=2)
        st.download_button(
            label="📥 Export Conversation",
            data=conversation_json,
            file_name=f"conversation_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header(f"{AGENT_INFO[selected_agent]['emoji']} Chat with {selected_agent}")
    
    # Query input
    with st.form("agent_query_form"):
        query = st.text_area(
            "Enter your query:",
            placeholder=f"Ask {selected_agent} anything related to their expertise...",
            height=100
        )
        
        col_submit, col_clear = st.columns([1, 1])
        with col_submit:
            submit_button = st.form_submit_button("🚀 Send Query", type="primary")
        with col_clear:
            clear_button = st.form_submit_button("🗑️ Clear Input")
    
    # Process query
    if submit_button and query.strip():
        with st.spinner(f"🤔 {selected_agent} is thinking..."):
            result = execute_agent_task(selected_agent, query)
            
            if result["success"]:
                st.success(f"✅ Response from {selected_agent}")
                st.markdown("### 📝 Response:")
                st.markdown(result["result"])
                
                # Add to conversation history
                add_to_conversation_history(selected_agent, query, result["result"])
                
            else:
                st.error(f"❌ Error: {result['result']}")
    
    elif submit_button:
        st.warning("⚠️ Please enter a query before submitting.")

with col2:
    st.header("👥 Team Overview")
    
    # Display all agents as cards
    for agent_name, info in AGENT_INFO.items():
        with st.container():
            if agent_name == selected_agent:
                st.markdown(f"**🎯 {info['emoji']} {agent_name}** (Active)")
            else:
                if st.button(f"{info['emoji']} {agent_name}", key=f"select_{agent_name}"):
                    st.session_state.selected_agent = agent_name
                    st.rerun()
            
            st.caption(info["description"])
            st.markdown("---")

# Conversation history
if st.session_state.conversation_history:
    st.header("📜 Conversation History")
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["💬 Chat View", "📊 Table View"])
    
    with tab1:
        # Display conversation in chat format
        for i, interaction in enumerate(reversed(st.session_state.conversation_history)):
            with st.expander(f"{interaction['agent']} - {interaction['timestamp']}", expanded=(i == 0)):
                st.markdown(f"**Query:** {interaction['query']}")
                st.markdown("**Response:**")
                st.markdown(interaction['result'])
    
    with tab2:
        # Display as table
        df = pd.DataFrame(st.session_state.conversation_history)
        st.dataframe(
            df[['timestamp', 'agent', 'query']],
            use_container_width=True,
            hide_index=True
        )
        
        # Show detailed view for selected row
        if not df.empty:
            selected_idx = st.selectbox("Select conversation to view details:", 
                                      range(len(df)), 
                                      format_func=lambda x: f"{df.iloc[x]['timestamp']} - {df.iloc[x]['agent']}")
            
            selected_interaction = df.iloc[selected_idx]
            st.markdown("### 📝 Detailed Response:")
            st.markdown(selected_interaction['result'])

# Footer
st.markdown("---")
st.markdown(
    "**Healthcare AI Team** | Built with Streamlit and CrewAI | "
    f"Agents Status: {'✅ Loaded' if AGENTS_LOADED else '❌ Not Loaded'}"
)

# Instructions for integration
if not AGENTS_LOADED:
    with st.expander("🔧 Integration Instructions & Error Details"):
        if IMPORT_ERROR:
            st.error(f"**Import Error Details:**\n```\n{IMPORT_ERROR}\n```")
            
            if "FileWriterTool" in IMPORT_ERROR:
                st.warning("**FileWriterTool Issue Detected**")
                st.markdown("""
                The error is in your `tools.py` file with `FileWriterTool`. Try fixing it with:
                
                **Option 1: Fix the FileWriterTool initialization**
                ```python
                # Instead of:
                update_record_tool = FileWriterTool('../docs/records.txt', '{summary}')
                
                # Try:
                update_record_tool = FileWriterTool(
                    file_path='../docs/records.txt',
                    content='{summary}'
                )
                
                # Or:
                update_record_tool = FileWriterTool(
                    filename='../docs/records.txt'
                )
                ```
                
                **Option 2: Comment out the problematic tool temporarily**
                ```python
                # update_record_tool = FileWriterTool('../docs/records.txt', '{summary}')
                ```
                """)
        
        st.markdown("""
        ### To integrate with your existing code:
        
        1. **Fix the FileWriterTool error** in your `tools.py` file (see above)
        
        2. **Save your agent definitions** in a file called `agents.py` in the same directory as this Streamlit app
        
        3. **Modify the execute_agent_task function** to actually call your agents:
        ```python
        def execute_agent_task(agent_name: str, query: str) -> Dict[str, Any]:
            agent = AGENT_INFO[agent_name]["agent_obj"]
            # Replace this with your actual agent execution
            result = agent.execute(query)  # or however you call your agents
            return {
                "success": True,
                "result": result,
                "agent": agent_name,
                "timestamp": datetime.now().isoformat(),
                "query": query
            }
        ```
        
        4. **Install dependencies**:
        ```bash
        pip install streamlit pandas crewai
        ```
        
        5. **Run the app**:
        ```bash
        streamlit run app.py
        ```
        
        ### Current Features:
        - Interactive agent selection
        - Query input and processing
        - Conversation history
        - Export functionality
        - Responsive design
        - Error handling
        """)