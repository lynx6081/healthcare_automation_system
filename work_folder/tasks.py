from crewai import Task
from tools import research_paper_reader_tool,past_search_data_tool, general_search_tool,research_paper_reader_tool,report_format_reader_tool,warren_update_record_tool
from agents import drwarren, Ruby, advik
import ssl
import certifi
import urllib.request

ssl_context = ssl.create_default_context(cafile=certifi.where())
with urllib.request.urlopen("https://arxiv.org", context=ssl_context) as r:
    print(r.read())
                        

project_task = Task(
    description = """
Your task is to understand and analyze each client query, determine what is required, and then decide who should handle it within the team. If the query falls within your scope, you will complete it yourself. If it requires expertise from other teammates, you will assign the task to one or more of them, provide them with the necessary context, and coordinate their efforts.

Workflow of a Query

Receive & Analyze – You read and interpret the client’s query, clarifying intent and requirements.

Decide Ownership – You determine if you can answer directly or if it should be routed to a teammate.

If within your scope → complete it yourself.

If external expertise is needed → delegate to the right teammate(s).

Coordinate & Track – Share the query and context with teammates, follow up on their progress, and ensure they deliver on time.

Integrate & Confirm – Collect the responses, check for completeness and accuracy, and resolve any gaps.

Deliver to Client – Provide the final answer in a clear, accurate, and seamless manner, ensuring the client sees only one smooth response and never the complexity of the coordination behind it

Also, before delegating work to the next teammate, convey the name of the person to whom you are delegating, to the user.

if the query is related to any medical knowledge then delegate it on to  senior medical strategist
if query is about the digital data then pass it to data analysis expert and  , the data could be the data gathered from wearables like sleeptime, pulserate etc.
if query is related to nutrition then delegate it to the renowned nutritionist carla.
if the query is related to physiology like any physical movement, body movements then pass it to the physiotherapist rachel.
if query is related with customer dissatisfaction or any problems the user is facing then pass it on to relationship manager neel, he will handle it

Decide whom to pass the query and then pass it to only required co workers and not all based on the context you understand.
client query: {query}
""",
expected_output= """
deliver the final answer, it should be:

Clear: Easy to understand, neatly structured, and free of unnecessary jargon.

Accurate: Fact-checked, consistent, and addressing all client questions, with next steps clearly stated if pending.

Seamless: One unified response with a consistent tone — hiding all behind-the-scenes coordination.

Reassuring: Closes the loop with confirmation, showing everything is handled proactively and thoroughly.

Professional: Timestamped if needed, with working links, attachments, and clear action points
""",
agent=Ruby
)

## MEDICAL RESEARCH BY WARREN:
medical_research = Task(
description = """
Medical Research Task Prompt for Dr. Warren:
When handling user queries, you must identify the type of query and use the correct tool to provide accurate, clear, and useful information.
The query can any one of the following types:
- Patient history Queries
-Latest Medical News Queries
-Research-Based Queries

For query identification and execution of task, details are provided below along with the tools each query will require.

Patient History Queries – If the user asks about a past illness or event (e.g., “I had pneumonia a year ago, what were my test results then?”), use the `past_search_data_tool` tool to access their medical records. Provide details of the illness, lab results, treatments, and recovery notes from their history.

Latest Medical News Queries – If the user asks about recent developments (e.g., “Is there a new treatment for diabetes released this year?”), use the `general_search_tool` tool to gather up-to-date news or medical reports. Summarize the findings in clear, reliable terms.

Research-Based Queries – If the user asks about studies or ongoing research (e.g., “What are the key findings of the latest cancer immunotherapy research?” or “Is there research happening on long-COVID?”), use the `research_paper_reader_tool` tool to fetch information. Provide key findings, active research areas, and relevant data from published studies

Identify the query, work on it with the tools provided and  Deliver the results in plain, understandable language, highlight what the information means for the patient, and ensure clarity, accuracy, and clinical precision in your response.

forwarding – Once complete, forward the final report to the `Ruby` (manager), who will ensure it is shared with the user.

query = {query}
""",
expected_output="""
Deliver the results to `Ruby` in plain, understandable language, highlight what the information means for the patient, and ensure clarity, accuracy, and clinical precision in your response.
""",
tools=[past_search_data_tool, general_search_tool,research_paper_reader_tool],
agents= drwarren
)

# Automated Report Generation:
medical_report_automation = Task(
    description="""
You must keep track of the user’s medical health on a continuous basis by intercating with the user, and every 3 months from the date the user joins generate a clear and concise health report for the user in the form of a text message.

Report Creation – Use the `report_format_reader_tool` tool to access the standard reporting format.Read and understand the report format. Present the report as structured text highlighting key health areas, progress, and any problems or risks. Focus on what the member or team cares about, such as tracking specific conditions, biomarkers, or goals.

Data Requirements – If additional medical records or missing data are needed, directly request the Manager to ask the user for the required information. Make sure all necessary details are gathered before finalizing the report. You may also collaborate with other specialized agents in their respective fields if specific expertise or data is required for the report.

Final Output – Deliver the report as a text message that is simple, accurate, and actionable. Clearly point out areas of concern, improvements, and personalized recommendations for the next steps in the user’s health strategy.

Forwarding – Once complete, forward the final report to `Ruby` (Manager), who will ensure it is shared with the user.

Health Record Update – After generating the report, summarise the report and use the `update_record_tool` tool to store it as {summary} and update the user’s health record with {summary} accordingly. Add any new findings, progress notes, and recommendations into the already stored medical history so that the user’s record always stays current and accurate.

Always ensure the communication is professional, easy to understand, and directly valuable to the user.
""",
expected_output="Deliver the automate 3 month interval, report to `Ruby` as a text message that is simple, accurate, and actionable. Clearly point out areas of concern, improvements, and personalized recommendations for the next steps in the user’s health strategy. Save the report summary to the you local file using the provided tools for later reference ",
tools=[report_format_reader_tool,update_record_tool],
agent = drwarren
)

# COLLABORATION BY WARREN: 
collaboration_by_warren = Task(
description="""
You must collaborate with other specialized agents whenever their expertise is needed to solve a user query or strengthen your medical strategy.

With `advik` (Performance Scientist): Share lab results and medical goals; ask him to track daily wearable data for progress. Use his insights on sleep, recovery, HRV, and trends to detect issues and refine your clinical direction.

With `Carla` (Nutritionist): Share diagnostic findings, risks, and medical priorities. Ensure her nutrition and supplement plans align with medical safety. Use her feedback from food logs and nutrition patterns to support your treatment strategies.

With `Rachel` (Physiotherapist): Share lab results, imaging, medical history, and restrictions. Use her movement assessments, injury feedback, and performance data to adjust health plans and prevent risks.

Collaborate whenever another agent’s data, expertise, or feedback is required to turn your medical guidance into safe, effective, real-world action.

Example: If you are updating the reports and you require data about user's eating habits then you will ask `Carla` (nutritionist) for help.

query = {query}
""",
expected_output="Expected and well defined answer to the query with the help of other co-workers whenever needed. ",
agent=drwarren
)


