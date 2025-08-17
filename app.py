import streamlit as st
import uuid
from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq
from vector_db import add_or_update_profile, retrieve_profile

# ---------------------------
# Initialize Groq LLM
# ---------------------------
llm = ChatGroq(
    model_name="your-groq-model",  # replace with your Groq model
    temperature=0.7
)

# ---------------------------
# Define Tasks
# ---------------------------
gather_health_task = Task(
    description="Gather health information from the user for a new profile",
    expected_output="A dictionary containing all required user health data, e.g., age, weight, height, medical history",
    verbose=True
)

make_report_task = Task(
    description="Generate a medical report for the user using existing and new health data",
    expected_output="A structured medical report as a string",
    verbose=True
)

# ---------------------------
# Define Agents
# ---------------------------
manager_agent = Agent(
    role="Manager",
    goal="Route queries and collect initial health info for new users",
    tasks=[gather_health_task],
    llm=llm,
    backstory="You are the manager agent. Your job is to collect user information and route queries to specialists efficiently.",
    verbose=True
)

medical_agent = Agent(
    role="Medical Strategist",
    goal="Create health reports using user data",
    tasks=[gather_health_task, make_report_task],
    llm=llm,
    backstory="You are a medical expert specialized in creating detailed health reports from user data.",
    verbose=True
)

crew = Crew(
  agents=[medical_agent,manager_agent ],
  tasks=[],
  process=Process.sequential,  # Optional: Sequential task execution is default
  memory=True,
  cache=True,
  max_rpm=100,
  share_crew=True
)

# ---------------------------
# Streamlit Interface
# ---------------------------
st.title("Health Report Assistant")
st.sidebar.header("User Profile")

# Unique user ID (for demo, can integrate login)
USER_ID = st.sidebar.text_input("Enter your User ID", str(uuid.uuid4()))

# Retrieve profile if exists
profile_data = retrieve_profile(USER_ID)
st.sidebar.json(profile_data if profile_data else {"info": "No profile data yet"})

# User query input
user_query = st.text_input("What would you like to do?", "Generate medical report")

if st.button("Submit Query"):
    with st.spinner("Processing..."):
        # First-time user: gather health info
        if not profile_data:
            messages = [{
                "role": "user",
                "content": f"Task: Gather health information from the user. User ID: {USER_ID}. Prompt: Please provide my health info"
            }]
            result = crew.kickoff(inputs=user_query)

            # Store profile in FAISS
            add_or_update_profile(USER_ID, result)
            st.success("Profile created successfully!")
            profile_data = result
        else:
            # Existing user: delegate to Medical Strategist
            messages = [{
                "role": "user",
                "content": f"Task: Create a medical report using the following user data: {profile_data}"
            }]
            result = crew.kickoff(inputs=user_query)
            st.success("Medical report generated!")

        # Show the result
        st.markdown(result if result else "No output generated")
