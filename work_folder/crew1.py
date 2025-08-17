import os
from crewai import Crew, Process, LLM
from crewai.memory import LongTermMemory
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage
from agents import Ruby,drwarren, Neel,advik,Carla, Rachel
from tools import user_history_search_tool,research_paper_reader_tool, medical_get_past_process_data_tool
from tasks import medical_research_task,  medical_query_identification, project_task
# Configure custom storage location
# custom_storage_path = "../ltsm"
# os.makedirs(custom_storage_path, exist_ok=True)
from dotenv import load_dotenv 

import streamlit as st

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# from langchain_community.llms import Ollama
# local_llama2 = LLM(
#     model="ollama/gemma3:12b",   # tell litellm it's an ollama model
#     base_url="http://localhost:11434",  # Ollama default
#     temperature=0.7
# )

# llm = LLM(
#      model="groq/llama3-70b-8192"
# )
st.title("Text Input Display App")

# Input text
user_input = st.text_input("Enter some text:")
input_dict = {
    'query': user_input
}

# medical_classification_crew = Crew(
#     verbose=False,
#     agents=[drwarren],
#     tasks=[medical_query_identification],
#     Process=Process.sequential,  # just one task here
#     manager_llm=LLM(
#         model="groq/llama-3.3-70b-versatile",
#         temperature=0
#     )
# )
# medical_classification_result = medical_classification_crew.kickoff(inputs =  input_dict)

# if "medical_research_task" in medical_classification_result:
#     selected_task = medical_research_task
# else:
#     selected_task = medical_answer_user_history_query

# def safe_execute(agent, query):
#     result = agent.run(query)
#     if "Action 'None'" in str(result):
#         return "I couldn’t find a suitable tool for that query."
#     return result

execution_crew = Crew(
    agents = [Ruby,drwarren, Neel,advik,Carla, Rachel],
    tasks = [project_task],
    Process = Process.hierarchical,
    # manager_llm = llm,
    memory=True,
    long_term_memory=LongTermMemory(
        storage=LTMSQLiteStorage(
            db_path=f"../ltsm/memory.db"
        )
    ),
    max_rpm = 100,
    share_crew = True
)

result = execution_crew.kickoff(inputs = input_dict)


# print(result)


# Display below
if user_input:
    st.write("You entered:")
    st.write(result)

# medical_research = Crew(
#     agents = [drwarren]
#     tasks = []
# )

#medical_answer_user_history_query,