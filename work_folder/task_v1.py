# medical_research_task = Task(
#     description=(
#         "When the user asks about research papers, use the `research_paper_reader_tool` tool"
#         "search in this  url = f\"https://export.arxiv.org/api/query?search_query={query}\". "

#         """if the query is about *the user's own medical condition, past treatments, prescriptions, diagnoses, personal symptoms, or their individual health history*. 
#         (Example: 
#          -"I had surgery last year, can I take this new medication?"
#           "I was diagnosed with diabetes two years ago, should I adjust my diet now?"
#          - "My doctor prescribed me metformin in the past, is it safe to continue?"
#          - "I often get headaches after taking this pill — is that normal?"
#          - "I had an allergic reaction to penicillin once, what alternatives can I use?")
#           then use the `user_histroy_search_tool` "

#         "If the query doesn’t match any tool, politely explain that you cannot help."""

#         "user query = {query}"
#     ),
#     expected_output="A clear, concise research answer with sources.",
#     agent=drwarren
# )


# medical_brave_search_task = Task(
#     description={
#         "Search for the {query} using Brave Search."
#         "Get detailed information about the {query} from the search results."
#     },
#     expected_output = "A detailed summary about the {query} from the Brave Search results extracted.",
#     tools = [general_brave_search_tool],
#     agent = drwarren
# )

# medical_update_research_task = Task(
#     description={
#         "Search for the {query} on medical websites."
#         "Get detailed information about the {query} from the medical sources."
#     },
#     expected_output = "A detailed summary about the {query} from the medical websites extracted.",
#     tools = [medical_web_data_extractor_tool],
#     agent = drwarren
# )

# medical_answer_user_history_query =  Task(
#     description="Search for the {query} in the PDF and get the relevant information.",
#     expected_output = "A detailed answer to the user {query} with reference to the PDF data.",
#     tools = [medical_get_past_process_data_tool],
#     agent = drwarren
# )

# medical_query_identification = Task(
#     description = 
#         """
#         You are a task selector.  
#         Tasks available:  
#         1. medical_research_task: Select this if the query is about *studies, experiments, scientific findings, clinical trials, statistics, new treatments, medical literature, or general medical knowledge discovery, research*. 
#         (Example: 
#          -"What are the latest clinical trial results for cancer immunotherapy?",
#          -"Summarize research on how intermittent fasting affects blood sugar."
#          - "What does medical literature say about long-term effects of antidepressants?"
#          - "Is there evidence linking air pollution to asthma risk?"
#          - "What are the recent FDA-approved treatments for Alzheimer’s disease?",
#          -"Query contains the words research, findings, etc", 
#         )
#         2. medical_answer_user_history_query: Select this if the query is about *the user's own medical condition, past treatments, prescriptions, diagnoses, personal symptoms, or their individual health history*. 
#        (Example: 
#          -"I had surgery last year, can I take this new medication?"
#           "I was diagnosed with diabetes two years ago, should I adjust my diet now?"
#          - "My doctor prescribed me metformin in the past, is it safe to continue?"
#          - "I often get headaches after taking this pill — is that normal?"
#          - "I had an allergic reaction to penicillin once, what alternatives can I use?")

#         User query: "{query}"
#         Which task is most appropriate? Reply with the task name only.
#         """
#     ,
#     expected_output = """
#         Only one from :
#         medical_research_task 
#         medical_answer_user_history_query
#         """,
#     agent = drwarren
# )
