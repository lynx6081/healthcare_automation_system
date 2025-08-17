from crewai import Task
from tool2 import (research_paper_reader_tool,report_format_reader_tool,warren_update_record_tool,warren_past_search_data_tool,medical_web_data_extractor_tool,advic_data_update_tool,advic_search_data_tool,carla_past_search_data_tool,carla_update_record_tool,nutrition_web_data_extractor_tool, rachel_past_search_data_tool, movement_web_data_extractor_tool, rachel_update_record_tool, ruby_progress_data_tool, user_medical_search_tool, ruby_update_record_tool)
from agents import drwarren, Ruby, advik, Carla, Rachel, Neel

project_task = Task(
    description = """
    

Your task is to understand and analyze each client query, determine what is required, and then decide who should handle it within the team. If the query falls within your scope, you will complete it yourself. If it requires expertise from other teammates, you will assign the task to one or more of them, provide them with the necessary context, and coordinate their efforts.

-The query from the user must be delivered to the specific specialist agents by you. The answers/ solutions to the query that you delegated to the specific specialist agents must be answered by them directly.
- The respective reports, exercise plans, nutrition plans that you recieve from the specialist agents must be sent to the user by you .

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

- the query is transferred to you by 'Ruby' 
Medical Research Task Prompt for Dr. Warren:
When handling user queries, you must identify the type of query and use the correct tool to provide accurate, clear, and useful information.
The query can any one of the following types:
- Patient history Queries
-Latest Medical News Queries
-Research-Based Queries

- the query is transferred to you by 'Ruby' 
For query identification and execution of task, details are provided below along with the tools each query will require.

Patient History Queries – If the user asks about a past illness or event (e.g., “I had pneumonia a year ago, what were my test results then?”), use the `warren_past_search_data_tool` tool to access their medical records. Provide details of the illness, lab results, treatments, and recovery notes from their history.

Latest Medical News Queries – If the user asks about recent developments (e.g., “Is there a new treatment for diabetes released this year?”), use the `medical_web_data_extractor_tool` tool to gather up-to-date news or medical reports. Summarize the findings in clear, reliable terms.

Research-Based Queries – If the user asks about studies or ongoing research (e.g., “What are the key findings of the latest cancer immunotherapy research?” or “Is there research happening on long-COVID?”), use the `research_paper_reader_tool` tool to fetch information. Provide key findings, active research areas, and relevant data from published studies

Identify the query, work on it with the tools provided and  Deliver the results in plain, understandable language, highlight what the information means for the patient, and ensure clarity, accuracy, and clinical precision in your response.

once you get the answer to the query, then communicate it directly with the user by sending him message.

query = {query}

You must use tools wisely and only when absolutely necessary. Carefully analyze the query and determine if a tool is truly essential to accomplish the task. If it is, select only the most suitable tool and use it with precision. If it is not required, do NOT use any tools. Avoid unnecessary or excessive tool use—apply them only when they are critical to achieving accurate, efficient, and relevant results.
""",
expected_output="""
Deliver the results to `Ruby` in plain, understandable language, highlight what the information means for the patient, and ensure clarity, accuracy, and clinical precision in your response.
""",
tools=[warren_past_search_data_tool,research_paper_reader_tool,medical_web_data_extractor_tool],
agent = drwarren
)

# Automated Report Generation:
medical_report_automation = Task(
    description="""
You must keep track of the user’s medical health on a continuous basis by intercating with the user, and every 3 months from the date the user joins generate a clear and concise health report for the user in the form of a text message.

Report Creation – Use the `report_format_reader_tool` tool to access the standard reporting format.Read and understand the report format. Present the report as structured text highlighting key health areas, progress, and any problems or risks. Focus on what the member or team cares about, such as tracking specific conditions, biomarkers, or goals.

Data Requirements – If additional medical records or missing data are needed, directly request the Manager to ask the user for the required information. Make sure all necessary details are gathered before finalizing the report. You may also collaborate with other specialized agents in their respective fields if specific expertise or data is required for the report.

Final Output – Deliver the report as a text message that is simple, accurate, and actionable. Clearly point out areas of concern, improvements, and personalized recommendations for the next steps in the user’s health strategy.

Forwarding – Once complete, forward the final report to report

Health Record Update – After generating the report, summarise the report and use the `update_record_tool` tool to store it as {summary} and update the user’s health record with {summary} accordingly. Add any new findings, progress notes, and recommendations into the already stored medical history so that the user’s record always stays current and accurate.

Always ensure the communication is professional, easy to understand, and directly valuable to the user.


- the query is transferred to you by 'Ruby' 

You must use tools wisely and only when absolutely necessary. Carefully analyze the query and determine if a tool is truly essential to accomplish the task. If it is, select only the most suitable tool and use it with precision. If it is not required, do NOT use any tools. Avoid unnecessary or excessive tool use—apply them only when they are critical to achieving accurate, efficient, and relevant results.
""",
expected_output="Deliver the automate 3 month interval, report to `Ruby` as a text message that is simple, accurate, and actionable. Clearly point out areas of concern, improvements, and personalized recommendations for the next steps in the user’s health strategy. Save the report summary to the you local file using the provided tools for later reference ",
tools=[report_format_reader_tool,warren_update_record_tool],
agent = drwarren
)

# COLLABORATION BY WARREN: 
collaboration_by_warren = Task(
description="""
You must collaborate with other specialized agents whenever their expertise is needed to solve a user query or strengthen your medical strategy.

With `advik` (Performance Scientist): Share lab results and medical goals by accessing the `warren_past_search_data_tool`tool ; ask him to track daily wearable data for progress. Use his insights on sleep, recovery, HRV, and trends to detect issues and refine your clinical direction.

With `Carla` (Nutritionist): Share diagnostic findings, risks, and medical priorities  by accessing the `warren_past_search_data_tool` tool . Ensure her nutrition and supplement plans align with medical safety. Use her feedback from food logs and nutrition patterns to support your treatment strategies.

With `Rachel` (Physiotherapist): Share lab results, imaging, medical history, and restrictions,  by accessing the `warren_past_search_data_tool`. Use her movement assessments, injury feedback, and performance data to adjust health plans and prevent risks.

Collaborate whenever another agent’s data, expertise, or feedback is required to turn your medical guidance into safe, effective, real-world action.

Example: If you are updating the reports and you require data about user's eating habits then you will ask `Carla` (nutritionist) for help.


- the query is transferred to you by 'Ruby' 
query = {query}

You must use tools wisely and only when absolutely necessary. Carefully analyze the query and determine if a tool is truly essential to accomplish the task. If it is, select only the most suitable tool and use it with precision. If it is not required, do NOT use any tools. Avoid unnecessary or excessive tool use—apply them only when they are critical to achieving accurate, efficient, and relevant results.
""",
expected_output="Expected and well defined answer to the query with the help of other co-workers whenever needed. ",
tools=[warren_past_search_data_tool],
agent=drwarren
)

#ADVIK_USER_QUERY:
wearable_data_analysis_task = Task(
    description="""

    
- the query is transferred to you by 'Ruby' 
Handle user queries related to wearable data and performance analytics using manually collected data:

DATA COLLECTION AND MAINTENANCE:
1. REGULAR DATA REQUESTS FROM USER:
   - Ask user for daily/weekly wearable data updates
   - Request specific metrics: sleep duration, sleep stages, HRV, resting HR, training load, stress scores
   - Maintain consistent data collection schedule (daily check-ins recommended)
   - Store all data as {data} in local text file using the `advic_data_update_tool ` with timestamps and organized format

2. LOCAL DATA FILE MANAGEMENT:
   - Update local file with new user-provided data regularly
   - Organize data by date, metric type, and measurement categories
   - Maintain historical data for trend analysis
   - Ensure data consistency and proper formatting

QUERY PROCESSING WORKFLOW:
1. IDENTIFY QUERY TYPE:
   - Sleep patterns: "Why is my deep sleep decreasing?" 
   - Recovery metrics: "What's affecting my HRV recovery?"
   - Training impact: "How does my workout intensity affect next-day readiness?"
   - Stress indicators: "Why is my resting heart rate elevated?"
   - Performance trends: "Am I overtraining based on my data?"

2. DATA RETRIEVAL AND ANALYSIS:
   - Check local text file for relevant historical data using the `advic_search_data_tool`
   - Identify available data points related to the query
   - Assess data completeness for the analysis period needed
   - Request additional specific data from user if gaps exist

3. PATTERN ANALYSIS:
   - Analyze sleep patterns: bedtime consistency, sleep stages, efficiency, wake episodes
   - Examine recovery trends: HRV patterns, resting HR trends, body temperature variations
   - Assess training load impact: strain scores, readiness correlation with workouts
   - Evaluate stress indicators: elevated HR, fragmented sleep, low HRV recovery

4. DATA GAP HANDLING:
   - If insufficient data exists, ask user for specific additional information
   - Request recent data points relevant to the query timeframe
   - Ask for context around concerning patterns (lifestyle changes, stress events, etc.)
   - Gather device-specific data if needed for accurate analysis

5. INSIGHT GENERATION:
   - Identify specific correlations from available data
   - Explain physiological mechanisms in simple terms
   - Compare against personal baselines when sufficient data exists
   - Highlight concerning trends requiring attention

6. ACTIONABLE RECOMMENDATIONS:
   - Provide specific, measurable actions to improve metrics
   - Suggest optimal timing for sleep, training, and recovery
   - Recommend lifestyle adjustments based on data patterns
   - Set realistic improvement targets with timelines

DATA COLLECTION REQUESTS:
- If analysis requires more data: "I need your HRV readings from the past week to answer this properly"
- For trend analysis: "Can you share your sleep data from the last 2 weeks?"
- For correlation analysis: "I need both your training log and recovery scores for comparison"

Query: {query}

You must use tools wisely and only when absolutely necessary. Carefully analyze the query and determine if a tool is truly essential to accomplish the task. If it is, select only the most suitable tool and use it with precision. If it is not required, do NOT use any tools. Avoid unnecessary or excessive tool use—apply them only when they are critical to achieving accurate, efficient, and relevant results.
""",
    expected_output="""
Comprehensive data analysis response including:
1. Direct answer to the user's specific query based on available data
2. Key metrics identified from local file and their current status vs baselines
3. Specific patterns or correlations discovered from stored data
4. Clear explanation of what the data means for performance/health
5. Actionable recommendations with expected timelines
6. Specific requests for additional data if needed for complete analysis
7. Monitoring suggestions for tracking improvement
8. Red flags or areas requiring immediate attention

Format: Data-driven insights in plain language with specific numbers and practical next steps.
Request any missing data points needed for thorough analysis.
Forward complete analysis to Ruby for user delivery.
""",
    tools=[advic_data_update_tool,advic_search_data_tool],  
    agent=advik
)

# TASK 2: HYPOTHESIS FORMATION AND EXPERIMENT DESIGN
experiment_hypothesis_task = Task(
    description="""

    
- the query is transferred to you by 'Ruby' 
Design and execute data-driven experiments to optimize user performance and recovery:

HYPOTHESIS DEVELOPMENT PROCESS:
1. DATA PATTERN IDENTIFICATION:
   - Analyze wearable data for meaningful correlations and if data is not present, search in the local file using `advic_search_data_tool` tool.
   - Identify recurring patterns affecting sleep, recovery, or performance
   - Look for lifestyle factors impacting key metrics
   - Generate testable hypotheses from observations

2. HYPOTHESIS FORMULATION:
   Examples of testable hypotheses:
   - "Bedtime after midnight reduces HRV by 10% next day"
   - "Back-to-back HIIT sessions decrease recovery scores by 20%"
   - "Caffeine after 2pm reduces deep sleep by 15 minutes"
   - "Zone-2 cardio improves HRV recovery compared to high-intensity training"

3. EXPERIMENT DESIGN:
   - Define clear, measurable outcomes (primary and secondary metrics)
   - Set experiment duration (1-2 weeks optimal for behavior change detection)
   - Establish baseline measurement period (minimum 1 week)
   - Control for confounding variables
   - Create simple, actionable intervention protocols

4. IMPLEMENTATION PROTOCOL:
   - Provide clear daily instructions for user
   - Set data collection requirements and frequency
   - Establish check-in points and progress monitoring
   - Create contingency plans for adherence issues

5. RESULTS ANALYSIS:
   - Compare pre/post intervention metrics
   - Calculate statistical significance of changes
   - Identify which metrics improved, stayed stable, or declined
   - Assess practical significance vs statistical significance

6. RECOMMENDATION FORMATION:
   - Determine if intervention should be permanently adopted
   - Suggest modifications for better results
   - Design follow-up experiments if needed
   - Integrate successful interventions into daily routine

EXPERIMENT EXAMPLES:
- Sleep Optimization: Test consistent 10:30pm bedtime vs variable bedtime
- Recovery Enhancement: Compare active recovery days vs complete rest days
- Training Timing: Test morning vs evening workout performance impact
- Nutrition Timing: Evaluate meal timing effects on sleep quality

You must use tools wisely and only when absolutely necessary. Carefully analyze the query and determine if a tool is truly essential to accomplish the task. If it is, select only the most suitable tool and use it with precision. If it is not required, do NOT use any tools. Avoid unnecessary or excessive tool use—apply them only when they are critical to achieving accurate, efficient, and relevant results.

Query/Goal: {query}
""",
    expected_output="""
Complete experiment plan including:
1. Clear hypothesis statement with expected outcomes
2. Detailed experiment protocol and timeline (baseline, intervention, analysis phases)
3. Specific metrics to track and measurement methods
4. Daily action items and behavior modifications for user
5. Success criteria and decision thresholds
6. Risk assessment and safety considerations
7. Expected results timeline and next steps

Submit experiment plan to Dr Warren for medical safety review.
Coordinate with Ruby for user communication and scheduling support.
Collaborate with relevant specialists based on experiment focus area.
""",
    tools=[advic_search_data_tool],  # Add: local_file_reader_tool, local_file_writer_tool, data_request_tool
    agent=advik
)

# TASK 3: INTER-AGENT COLLABORATION FOR PERFORMANCE OPTIMIZATION
advik_performance_collaboration_task= Task(
    description="""

    
- the query is transferred to you by 'Ruby' 
Collaborate with specialized team members to integrate wearable data insights with their expertise:

COLLABORATION PROTOCOLS:

WITH `drwarren` (Medical Specialist):
- SHARE: Concerning wearable trends that may indicate medical issues
  * Persistent HRV decline (>20% below baseline for >1 week)
  * Elevated resting HR without training explanation
  * Chronic sleep disruption patterns
  * Unusual stress response patterns
- REQUEST: Lab results, medical history, medication effects on metrics
- INTEGRATE: Align performance recommendations with medical safety
- ESCALATE: Urgent patterns requiring immediate medical attention
- To use `drwarren` data, use `warren_past_search_data_tool` tool and if no data is present, return that data is unavalable for now


WITH `Carla` (Nutritionist):
- SHARE: Sleep and recovery responses to nutrition timing and composition
  * Post-meal sleep quality impacts
  * Hydration effects on HRV and recovery
  * Supplement timing correlation with performance metrics
- REQUEST: Detailed food logs, meal timing, supplement protocols
- COLLABORATE: Design nutrition experiments based on wearable feedback
- OPTIMIZE: Meal and supplement timing for performance and recovery
- To use `carla` data, use `carla_past_search_data_tool` tool and if no data is present, return that data is unavalable for now

WITH `Rachel` (Physiotherapist):
- SHARE: Training load data, recovery patterns, and readiness scores
  * Impact of different exercise types on recovery metrics
  * Optimal training timing based on readiness scores
  * Recovery capacity trends and training load tolerance
- REQUEST: Movement assessments, injury history, training modifications
- COORDINATE: Adjust training intensity based on recovery data
- PREVENT: Overtraining and injury risk through data monitoring
- To use `rachel` data, use `rachel_past_search_data_tool` tool,and if no data is present, return that data is unavalable for now

COLLABORATION WORKFLOW:
1. IDENTIFY COLLABORATION NEED:
   - Multi-factorial performance issues requiring expert input
   - Medical safety concerns from wearable data patterns
   - Optimization opportunities requiring specialist knowledge

2. PREPARE COLLABORATION REQUEST:
   - Summarize relevant wearable data trends and patterns
   - Specify what expertise or information is needed
   - Provide clear context and timeline requirements

3. INTEGRATE SPECIALIST FEEDBACK:
   - Incorporate expert recommendations into performance strategy
   - Validate recommendations against wearable data patterns
   - Identify potential conflicts and resolve with medical oversight

4. MONITOR COLLABORATIVE OUTCOMES:
   - Track effectiveness of integrated recommendations
   - Adjust strategies based on multi-source feedback
   - Document successful collaboration patterns for future reference

   You must use tools wisely and only when absolutely necessary. Carefully analyze the query and determine if a tool is truly essential to accomplish the task. If it is, select only the most suitable tool and use it with precision. If it is not required, do NOT use any tools. Avoid unnecessary or excessive tool use—apply them only when they are critical to achieving accurate, efficient, and relevant results.
Query/Context: {query}
""",
    expected_output="""
Collaborative analysis including:
1. Identified need for specialist expertise and rationale
2. Specific data trends and patterns to share with specialists
3. Clear requests for information or recommendations from each specialist
4. Integration plan for combining wearable insights with specialist advice
5. Monitoring plan for collaborative intervention effectiveness
6. Timeline for follow-up and strategy adjustment

Coordinate with appropriate specialists based on identified needs.
Ensure all recommendations maintain medical safety oversight.
Forward integrated strategy to `Ruby` for user communication.
""",
    tools=[carla_past_search_data_tool,rachel_past_search_data_tool,warren_past_search_data_tool],  # Add: local_file_reader_tool, user_communication_tool, data_request_tool
    agent=advik
    #context=[Ruby, Rachel, drwarren, Carla]
)

continuous_monitoring_task = Task(
    description="""
Provide ongoing monitoring of wearable data for proactive performance optimization:

MONITORING FRAMEWORK:
1. DAILY READINESS ASSESSMENT:
   - Calculate daily readiness scores based on sleep, HRV, and recovery metrics
   - Provide training recommendations (full intensity, moderate, active recovery, rest)
   - Flag concerning patterns requiring immediate attention

2. WEEKLY TREND ANALYSIS:
   - Identify weekly patterns in sleep, recovery, and performance metrics
   - Compare current week to previous weeks and seasonal baselines
   - Generate weekly performance summary with key insights

3. MONTHLY COMPREHENSIVE REVIEW:
   - Analyze long-term trends and seasonal variations
   - Assess progress toward performance goals
   - Identify optimization opportunities for next month

4. ALERT SYSTEM:
   - Immediate alerts: Dangerous overreaching, severe sleep deprivation
   - Trend alerts: Declining performance patterns, concerning metric changes
   - Opportunity alerts: Optimal conditions for challenging workouts or experiments

PROACTIVE INTERVENTIONS:
- Suggest rest days before overreaching occurs
- Recommend sleep optimization when patterns decline
- Propose training adjustments based on recovery capacity
- Coordinate with team members for comprehensive interventions

You must use tools wisely and only when absolutely necessary. Carefully analyze the query and determine if a tool is truly essential to accomplish the task. If it is, select only the most suitable tool and use it with precision. If it is not required, do NOT use any tools. Avoid unnecessary or excessive tool use—apply them only when they are critical to achieving accurate, efficient, and relevant results.

Context: {monitoring_period}
""",
    expected_output="""
Monitoring report including:
1. Current performance status and readiness assessment
2. Trend analysis with comparison to baselines
3. Proactive recommendations for optimization
4. Alert notifications requiring attention
5. Collaboration needs with other team members
6. Performance trajectory and goal progress

Deliver daily summaries to Ruby for user communication.
Provide specialist alerts to relevant team members as needed.
""",
    #tools=[],  # Add: monitoring_dashboard_tool, alert_system_tool, trend_analysis_tool
    agent=advik
    #context=[Ruby]
)

# ADDITIONAL TASK: DATA QUALITY AND DEVICE MANAGEMENT
data_quality_management_task = Task(
    description="""

    
- the query is transferred to you by 'Ruby' 
Ensure optimal wearable data quality and device performance for accurate analysis:

DATA QUALITY ASSURANCE:
1. DAILY DATA VALIDATION:
   - Verify data sync from all connected devices if devices are present
   - Identify missing data points or anomalous readings
   - Cross-validate metrics across multiple devices when available
   - Flag potential device malfunctions or user error

2. DEVICE OPTIMIZATION:
   - Monitor battery levels and charging patterns
   - Ensure proper device fit and positioning
   - Validate sensor accuracy against known standards
   - Recommend device settings for optimal data collection

3. TROUBLESHOOTING PROTOCOL:
   - Diagnose common device issues and connectivity problems
   - Provide step-by-step resolution guidance
   - Escalate complex technical issues to device manufacturers
   - Suggest alternative data collection methods during device downtime

4. USER EDUCATION:
   - Guide proper device wearing techniques
   - Explain impact of device placement on data accuracy
   - Provide maintenance schedules and best practices
   - Educate on factors that can affect data quality

CONTINUOUS IMPROVEMENT:
- Evaluate new device features and capabilities
- Recommend device upgrades when beneficial
- Optimize data collection protocols based on user lifestyle
- Maintain historical data integrity during device transitions

You must use tools wisely and only when absolutely necessary. Carefully analyze the query and determine if a tool is truly essential to accomplish the task. If it is, select only the most suitable tool and use it with precision. If it is not required, do NOT use any tools. Avoid unnecessary or excessive tool use—apply them only when they are critical to achieving accurate, efficient, and relevant results.

Issue/Context: {data_quality_issue}
""",
    expected_output="""
Data quality assessment including:
1. Current data quality status and issues identified
2. Device performance evaluation and recommendations
3. Specific troubleshooting steps for identified problems
4. User education needs and guidance materials
5. Upgrade recommendations with cost-benefit analysis
6. Data integrity verification and validation results

Coordinate with `Ruby` for device procurement and user support.
Ensure continuous high-quality data for accurate analysis and recommendations.
""",
    agent=advik,
    #context=[Ruby]
)

diet_plan_generation_task = Task(
    description="""
    Design and continuously optimize personalized nutrition and diet plans for users based on comprehensive health data analysis. 
    
    Your responsibilities include:
    - Analyze user biomarkers (blood work, CGM trends, microbiome data) and if data is required, either collaborate with `drwarren` or access the data using the `warren_past_search_data_tool`
    - Incorporate lifestyle factors, training schedules, and specific health goals and ask user if any data is missing
    - Create initial personalized meal plans with macronutrient breakdowns, and other important nutrition data of the user
    - Monitor user adherence and satisfaction levels
    - Adjust plans based on user feedback (e.g., food preferences, difficulty following plan)
    - Track progress metrics and refine recommendations accordingly
    - Ensure plans remain practical, sustainable, and aligned with evolving user needs
    - Store the personlised meal plan as {mealplan} and update it whenever their are changes using the `carla_update_record_tool`tool to access and write in the file.
    - to access the original document, use the `carla_past_search_data_tool` tool.
    - All diet plans (new or revised) must be submitted to `Ruby`(manager) for approval before user delivery.
    - If you want to access any sort of nutritional data, you can either search on web using the `nutrition_web_data_extractor_tool` or find the relevant research papers using the `research_paper_reader_tool`

    You must use tools wisely and only when absolutely necessary. Carefully analyze the query and determine if a tool is truly essential to accomplish the task. If it is, select only the most suitable tool and use it with precision. If it is not required, do NOT use any tools. Avoid unnecessary or excessive tool use—apply them only when they are critical to achieving accurate, efficient, and relevant results.
    """,
    
    expected_output="""
    A comprehensive personalized diet plan document containing:
    - Complete meal plan with breakfast, lunch, dinner, and snack options
    - Detailed macronutrient breakdown (carbs, proteins, fats) per meal
    - Weekly meal schedule aligned with training days and rest days
    - Specific food recommendations based on biomarker analysis
    - Supplement protocol if applicable
    - Progress tracking metrics and adjustment triggers
    - Implementation timeline and adherence guidelines
    - Formatted for `Ruby` review and approval
    """,
    
    tools=[
        warren_past_search_data_tool, nutrition_web_data_extractor_tool,carla_past_search_data_tool, research_paper_reader_tool, carla_update_record_tool
    ],
    
    agent=Carla,
    #context=[Ruby]
)

nutrition_consultation_task = Task(
    description="""

    
- the query is transferred to you by 'Ruby' 
    Provide expert nutritional guidance and answer user queries within your specialization domain.
    
    Query categories you handle:
    - Nutrition and diet plan questions (e.g., "Best meal plan for fat loss?")
    - Eating habits and food-specific queries (e.g., "Should I eat tomatoes daily?", "Benefits of morning bananas?")
    - Food log interpretation and CGM data analysis (e.g., "Why glucose spikes after dinner?")
    - Supplement recommendations and guidance (e.g., "Magnesium for better sleep?")
    - Meal timing and frequency optimization
    - Hydration strategies and requirements
    
    Ensure all responses are:
    - Personalized based on user's health goals, lab markers, and lifestyle
    - Practical and actionable
    - Sustainable for long-term adherence
    - Evidence-based and aligned with current nutritional science

    INFORMATION ACCESS:
    - To access the current information about the user, use the `carla_past_search_data_tool` to access the nurtition data available
    - If the data is unavailable in the available data, then search about the query in research papers by using `research_paper_reader_tool` tool or search it on web urls by using `nutrition_web_data_extractor_tool` tool for appropriate answers.

You must use tools wisely and only when absolutely necessary. Carefully analyze the query and determine if a tool is truly essential to accomplish the task. If it is, select only the most suitable tool and use it with precision. If it is not required, do NOT use any tools. Avoid unnecessary or excessive tool use—apply them only when they are critical to achieving accurate, efficient, and relevant results.
    query = {query}
    """,
    
    expected_output="""
    Detailed nutritional consultation response including:
    - Direct answer to user's specific question
    - Personalized recommendations based on user's health profile
    - Scientific rationale behind the advice
    - Practical implementation steps
    - Potential considerations or precautions
    - Follow-up recommendations or monitoring suggestions
    - Clear, jargon-free language for user understanding
    -short and to the point, no extra unnecessary work
    """,
    
    tools=[
        carla_past_search_data_tool,research_paper_reader_tool,nutrition_web_data_extractor_tool
    ],
    
    agent=Carla
    
    #async_execution=True
)

carla_collaboration_integration_task = Task(
    description="""
    Collaborate seamlessly with specialized agents to optimize nutritional strategies within the broader health ecosystem.
    
    Collaboration protocols:
    
    **With `drwarren` (Medical Strategist):**
    - Share food log insights, CGM trends, and supplement recommendations
    - Adjust dietary strategies based on diagnostic findings and medical risks
    - Ensure nutrition interventions align with clinical priorities and safety protocols
    - Coordinate supplement protocols with medical treatments

    **With `Advik` (Performance Scientist):**
    - Integrate wearable data insights into meal timing and macronutrient strategies
    - Align nutrition with recovery trends and energy fluctuation patterns
    - Optimize hydration strategies based on performance metrics
    - Coordinate pre/post-workout nutrition with training schedules
    
    **With `Rachel` (Physiotherapist):**
    - Provide nutrition insights supporting injury recovery and muscle function
    - Align supplementation with rehabilitation goals and movement assessments
    - Coordinate anti-inflammatory nutrition strategies with physical therapy
    - Support performance demands through targeted nutritional interventions
    
    Initiate collaboration whenever another agent's expertise is required for comprehensive nutritional optimization.

    - If another agent requires any data, search the data in your local file using the `carla_past_search_data_tool`tool to get the required query data and then summarise it and share it with agent.

    You must use tools wisely and only when absolutely necessary. Carefully analyze the query and determine if a tool is truly essential to accomplish the task. If it is, select only the most suitable tool and use it with precision. If it is not required, do NOT use any tools. Avoid unnecessary or excessive tool use—apply them only when they are critical to achieving accurate, efficient, and relevant results.
    """,
    
    expected_output="""
    Collaborative integration report containing:
    - Specific data shared with each collaborating agent
    - Insights received from other agents and how they impact nutritional strategy
    - Integrated recommendations that consider medical, performance, and physical therapy inputs
    - Coordinated action plan with clear role delineations
    - Timeline for implementation and follow-up collaborations
    - Documentation of how multi-agent insights enhance nutritional outcomes
    - Updated user nutrition strategy reflecting all collaborative inputs
    """,
    
    tools=[
        carla_past_search_data_tool
    ],
    
    agent=Carla,
    
    #context=[drwarren, advik, Rachel, Ruby],
    
    #collaboration=True
)

physiotherapy_consultation_task = Task(
    description="""
    
- the query is transferred to you by 'Ruby' 
    Provide expert physiotherapy guidance and answer user queries within your specialization domain covering the body's muscular, skeletal, and functional systems.
    
    Query categories you handle:
    - Practical injury management questions (e.g., "How to treat ankle sprain?", "Should I use heat or ice?")
    - Exercise programming guidance (e.g., "Which exercises strengthen lower back?", "How to improve posture?")
    - Strength and rehabilitation support (e.g., "Safe recovery after knee surgery?", "How to prevent shoulder impingement?")
    - Physiology basics explanations (e.g., "Which muscle is responsible for hip flexion?", "How do ligaments support joint stability?")
    - Movement assessment and biomechanical analysis
    - Injury prevention strategies and protocols
    
    Ensure all responses are:
    - Personalized based on user's movement patterns, injury history, and physical goals
    - Practical and actionable with clear implementation steps
    - Evidence-based and aligned with current physiotherapy science
    - Safe and appropriate for user's current physical condition
    - Clear, jargon-free language reflecting expertise in physiotherapy, biomechanics, rehabilitation, and movement science

    INFORMATION ACCESS:
    - To access current user information, use the `rachel_past_search_data_tool` to access movement and physical therapy data available
    - If data is unavailable, search research papers using `research_paper_reader_tool` or web data using `movement_web_data_extractor_tool` for evidence-based answers
    - For medical clearances or restrictions, collaborate with `drwarren` or access data using `warren_past_search_data_tool`

    You must use tools wisely and only when absolutely necessary. Carefully analyze the query and determine if a tool is truly essential to accomplish the task. If it is, select only the most suitable tool and use it with precision. If it is not required, do NOT use any tools. Avoid unnecessary or excessive tool use—apply them only when they are critical to achieving accurate, efficient, and relevant results.

    query = {query}
    """,
    
    expected_output="""
    Detailed physiotherapy consultation response including:
    - Direct answer to user's specific question
    - Personalized recommendations based on user's physical profile and movement patterns
    - Scientific rationale behind the advice with biomechanical explanations
    - Practical implementation steps with exercise descriptions or treatment protocols
    - Safety considerations and precautions
    - Progressive modifications and progressions
    - Follow-up recommendations or monitoring suggestions
    - Clear, professional language for user understanding
    - Short and to the point, no extra unnecessary work
    """,
    
    tools=[
        rachel_past_search_data_tool,research_paper_reader_tool , movement_web_data_extractor_tool, warren_past_search_data_tool
    ],
    
    agent=Rachel,
    
    #async_execution=True
)

exercise_program_generation_task = Task(
    description="""
    Create and continuously optimize personalized exercise programs that are automatically updated every two weeks based on comprehensive movement analysis and progress tracking.
    
    Your responsibilities include:
    - Analyze user movement patterns, strength assessments, and injury history using `rachel_past_search_data_tool`
    - Collaborate with `advik` for wearable data insights or access using `advik_search_data_tool`
    - Create comprehensive exercise programs covering all key areas:
      * Strength Training - progressive overload protocols
      * Mobility & Flexibility - targeted range of motion improvements
      * Injury Prevention & Rehabilitation - identify weaknesses and implement targeted rehab/prehab routines
      * Form & Technique Mastery - ensure optimal biomechanics for every exercise
    - Implement progress tracking using measurable metrics (load lifted, ROM, movement quality)
    - Monitor user adherence and consistency with program following
    - Evaluate improvements in performance and movement patterns
    - Address any risks or setbacks promptly with program modifications
    - Update exercise programs every two weeks based on user progress, recovery, and evolving needs
    - Store personalized exercise plan as {exerciseplan} and update using `rachel_update_record_tool`
    - Access original documents using `rachel_past_search_data_tool`
    - All exercise programs (new or revised) must be submitted to `Ruby` (manager) for approval before user delivery
    - Research evidence-based exercise protocols using `research_paper_reader_tool` or `movement_web_data_extractor_tool`

    You must use tools wisely and only when absolutely necessary. Carefully analyze the query and determine if a tool is truly essential to accomplish the task. If it is, select only the most suitable tool and use it with precision. If it is not required, do NOT use any tools. Avoid unnecessary or excessive tool use—apply them only when they are critical to achieving accurate, efficient, and relevant results.
    """,
    
    expected_output="""
    A comprehensive personalized exercise program document containing:
    - Complete 2-week exercise program with daily workout schedules
    - Detailed strength training protocols with sets, reps, and progression schemes
    - Mobility and flexibility routines with specific stretches and ROM targets
    - Injury prevention exercises targeting identified movement dysfunctions
    - Form cues and technique instructions for safe exercise execution
    - Progress tracking metrics and measurement protocols
    - Weekly assessment checkpoints and adjustment triggers
    - Implementation timeline with gradual progression guidelines
    - Clear, structured format that is simple to follow and results-focused
    - Aligned with long-term physical resilience and performance goals
    - Formatted for `Ruby` review and approval
    """,
    
    tools=[
        rachel_past_search_data_tool, advic_search_data_tool, research_paper_reader_tool, 
        movement_web_data_extractor_tool, rachel_update_record_tool
    ],
    
    agent=Rachel,
    #context=[Ruby]
)

rachel_collaboration_integration_task = Task(
    description="""
    Collaborate seamlessly with specialized agents to optimize exercise programs and physiotherapy interventions within the broader health ecosystem.
    
    Collaboration protocols:
    
    **With `drwarren` (Medical Specialist):**
    - Receive lab results, imaging, medical history, and movement restrictions
    - Use medical insights to design safe training plans and adapt exercises for risk factors
    - Align rehabilitation routines with clinical priorities and medical protocols
    - Share movement assessments, performance data, and injury feedback to help refine clinical strategies
    - Coordinate exercise modifications with medical treatments and recovery protocols

    **With `advik` (Performance Scientist):**
    - Incorporate wearable data on sleep, recovery, HRV, and workload trends to optimize training intensity
    - Align exercise programming with recovery cycles and physiological readiness
    - Share exercise progress and physical performance markers for physiological data interpretation
    - Coordinate training loads with recovery metrics and performance optimization strategies
    
    **With `Carla` (Nutritionist):**
    - Coordinate nutrition and supplementation supporting muscle growth, recovery, and joint health
    - Share training demands and progress so dietary strategies can be adjusted accordingly
    - Use food log insights to adapt programs for energy, performance, and injury prevention
    - Align exercise timing with nutritional protocols for optimal recovery and adaptation
    
    Initiate collaboration whenever another agent's expertise is required for comprehensive physical optimization and ensure every plan is safe, medically sound, and fully integrated.

    - If another agent requires any data, search the data in your local file using the `rachel_past_search_data_tool` to get the required query data and then summarize it and share it with the agent.

    You must use tools wisely and only when absolutely necessary. Carefully analyze the query and determine if a tool is truly essential to accomplish the task. If it is, select only the most suitable tool and use it with precision. If it is not required, do NOT use any tools. Avoid unnecessary or excessive tool use—apply them only when they are critical to achieving accurate, efficient, and relevant results.
    """,
    
    expected_output="""
    Collaborative integration report containing:
    - Specific movement and performance data shared with each collaborating agent
    - Medical insights, performance metrics, and nutritional considerations received from other agents
    - Integrated exercise recommendations considering medical clearances, performance data, and nutritional support
    - Coordinated action plan with clear role delineations and safety protocols
    - Timeline for implementation with regular collaborative check-ins and updates
    - Documentation of how multi-agent insights enhance exercise program safety and effectiveness
    - Updated user exercise strategy reflecting all collaborative inputs and medical considerations
    - Risk mitigation strategies developed through collaborative expertise
    """,
    
    tools=[
        rachel_past_search_data_tool
    ],
    
    agent=Rachel,
    
    #context=[drwarren, advik, Carla, Ruby],
    
    #collaboration=True
)

customer_success_consultation_task = Task(
    description="""
    
- the query is transferred to you by 'Ruby' 
    Provide expert customer success guidance and answer user queries within your specialization domain focusing on strategic client relationship management and value optimization.
    
    Query categories you handle:
    - Customer dissatisfaction resolution (e.g., "Client unhappy with results?", "How to rebuild trust after service issues?")
    - Strategic review leadership (e.g., "Preparing for quarterly business review?", "How to present ROI metrics?")
    - Critical escalation management (e.g., "Client threatening to leave?", "Executive complaint handling?")
    - Value reframing and strategic alignment (e.g., "Connecting daily actions to long-term goals?", "Demonstrating program value?")
    - Client retention and expansion strategies
    - Stakeholder communication and relationship building
    - Success metrics definition and tracking
    
    Ensure all responses are:
    - Strategic and focused on long-term client value and relationship building
    - Practical with actionable frameworks for client success management
    - Aligned with big-picture goals and business objectives
    - Confidence-building for both internal team and client relationships
    - Professional and solution-oriented reflecting expertise in customer success, strategic account management, and value delivery

    INFORMATION ACCESS:
    - Access Ruby's progress tracking data using the `ruby_progress_data_tool` to understand current program execution status
    - Access user general data using the `user_medical_search_tool` to understand client background and context
    - Base all strategic responses on these two data sources: progress data and user general information
    - Collaborate with `Ruby` for operational updates when needed

    You must use tools wisely and only when absolutely necessary. Carefully analyze the query and determine if a tool is truly essential to accomplish the task. If it is, select only the most suitable tool and use it with precision. If it is not required, do NOT use any tools. Avoid unnecessary or excessive tool use—apply them only when they are critical to achieving accurate, efficient, and relevant results.
    query = {query}
    """,
    
    expected_output="""
    Detailed customer success consultation response including:
    - Direct answer to user's specific strategic question
    - Personalized recommendations based on progress data and user general information
    - Strategic rationale with frameworks for customer success and value delivery
    - Practical implementation steps with clear action items and timelines
    - Stakeholder communication strategies and key messaging points
    - Risk mitigation approaches and escalation protocols
    - Success metrics and tracking mechanisms
    - Follow-up recommendations and strategic monitoring suggestions
    - Professional, confident language focused on long-term value creation
    - Short and to the point, no extra unnecessary work
    """,
    
    tools=[
        ruby_progress_data_tool, user_medical_search_tool
    ],
    
    agent=Neel,
    
    #async_execution=True
)

strategic_review_management_task = Task(
    description="""
    Lead and execute comprehensive strategic reviews including Quarterly Business Reviews (QBRs) and major client assessment sessions based on progress analysis and user context.
    
    Your responsibilities include:
    - Access Ruby's progress tracking data using `ruby_progress_data_tool` to analyze client engagement patterns, satisfaction metrics, and value realization
    - Access user general data using `user_medical_search_tool` for comprehensive client background and context
    - Create strategic review presentations covering:
      * Client success metrics and ROI demonstration based on progress data
      * Health outcomes and program effectiveness analysis from Ruby's tracking
      * Strategic goal alignment and progress tracking using available data
      * Future opportunity identification and expansion planning
    - Develop action plans connecting daily operational activities to long-term strategic objectives
    - Prepare stakeholder communication materials and executive summaries
    - Conduct review meetings with key stakeholders and decision makers
    - Provide strategic insights and recommendations for ongoing client success optimization
    - All strategic reviews must be coordinated with `Ruby` for operational alignment and seamless execution

    You must use tools wisely and only when absolutely necessary. Carefully analyze the query and determine if a tool is truly essential to accomplish the task. If it is, select only the most suitable tool and use it with precision. If it is not required, do NOT use any tools. Avoid unnecessary or excessive tool use—apply them only when they are critical to achieving accurate, efficient, and relevant results.
    """,
    
    expected_output="""
    A comprehensive strategic review package containing:
    - Executive summary highlighting key client success metrics and strategic wins based on progress data
    - Detailed ROI analysis with quantified outcomes and program value from Ruby's tracking
    - Strategic goal alignment assessment showing progress against client objectives
    - Performance analysis with key success indicators and trend insights
    - Future opportunity roadmap with expansion and optimization recommendations
    - Risk assessment and mitigation strategies for client retention
    - Action plan with clear timelines and success metrics
    - Stakeholder presentation materials optimized for executive communication
    - Follow-up protocol and next review scheduling framework
    - Documentation aligned with long-term client value creation and strategic partnership development
    - Formatted for seamless execution coordination with `Ruby`
    """,
    
    tools=[
        ruby_progress_data_tool, user_medical_search_tool
    ],
    
    agent=Neel,
    #context=[Ruby]
)

neel_collaboration_integration_task = Task(
    description="""
    Collaborate seamlessly with operational management to optimize customer success strategies and ensure strategic alignment across all client touchpoints using available progress and user data.
    
    Collaboration protocols:
    
    **With `Ruby` (Operations Manager):**
    - Access progress tracking data using `ruby_progress_data_tool` to understand current execution status and client engagement
    - Access user general data using `user_medical_search_tool` for comprehensive client context and background
    - Share strategic priorities and client success requirements for operational planning
    - Coordinate seamless execution of strategic initiatives and client commitments
    - Align operational metrics with strategic success indicators and client value objectives
    - Ensure all follow-up actions are executed efficiently enabling strategic focus maintenance
    - Rely on Ruby's consolidated data from all specialist agents for comprehensive client insights
    
    **Strategic Integration Approach:**
    - Use Ruby's aggregated data from all specialist agents (drwarren, advik, Rachel, Carla) for holistic client success analysis
    - Connect specialist outcomes to strategic client value propositions without direct agent interaction
    - Leverage Ruby's operational oversight to ensure all specialist insights are reflected in strategic planning
    - Focus on strategic interpretation of progress data and user context for optimal client success outcomes
    
    Maintain strategic focus on client confidence, long-term value delivery, and relationship strengthening using available data sources.

    - All strategic insights and client success initiatives are based on Ruby's comprehensive progress tracking and user general data.

    You must use tools wisely and only when absolutely necessary. Carefully analyze the query and determine if a tool is truly essential to accomplish the task. If it is, select only the most suitable tool and use it with precision. If it is not required, do NOT use any tools. Avoid unnecessary or excessive tool use—apply them only when they are critical to achieving accurate, efficient, and relevant results.
    """,
    
    expected_output="""
    Collaborative strategic integration report containing:
    - Strategic analysis of client success metrics based on Ruby's progress tracking data
    - Comprehensive client success strategy incorporating insights from user general data and progress trends
    - Coordinated strategic action plan with clear value delivery timelines and success indicators
    - Timeline for strategic initiative implementation with regular progress reviews through Ruby's tracking
    - Documentation of how progress data and user context enhance overall client value proposition and satisfaction
    - Updated comprehensive client success strategy reflecting all available data insights and strategic priorities
    - Risk mitigation and opportunity identification strategies developed from progress analysis and user context
    - Executive communication framework connecting all progress outcomes to strategic client objectives
    - Strategic recommendations for Ruby to coordinate with specialist agents for optimal client outcomes
    """,
    
    tools=[
        ruby_progress_data_tool, user_medical_search_tool
    ],
    
    agent=Neel,
    
    #context=[Ruby],
    
    #collaboration=True
)

# RUBY'S CORE TASKS - OPERATIONS MANAGER

# TASK 1: CLIENT QUERY ORCHESTRATION AND DELEGATION
client_query_orchestration_task = Task(
    description="""
    
- the query is transferred to you by 'Ruby' 
    Serve as the primary client interface and intelligent query orchestration system for all client requests.
    
    Your primary responsibilities:
    - Receive and analyze all client queries to understand intent, scope, and urgency
    - Determine the appropriate team member(s) to handle each query based on expertise domains
    - Delegate queries with proper context and clear expectations
    - Track query progress and ensure timely completion
    - Consolidate responses from multiple specialists into coherent, unified client communications
    - Maintain consistent client experience regardless of backend complexity
    
    DELEGATION DECISION FRAMEWORK:
    - Medical queries → `drwarren` (Senior Medical Strategist) - use `user_medical_search_tool` to provide context
    - Wearable data/performance analytics → `advik` (Performance Scientist) - use `ruby_progress_data_tool` to share relevant progress data
    - Nutrition/diet planning → `Carla` (Nutritionist) - use `ruby_progress_data_tool` to provide nutrition tracking data
    - Exercise/physiotherapy → `Rachel` (Physiotherapist) - use `ruby_progress_data_tool` to share movement and exercise progress
    - Client satisfaction/strategic issues → `Neel` (Customer Success Manager) - use `ruby_progress_data_tool` to provide comprehensive progress overview
    - Multi-domain queries → Coordinate multiple specialists using appropriate data tools
    
    TOOL USAGE:
    - `ruby_progress_data_tool`: Access comprehensive client progress across all domains for delegation context
    - `user_medical_search_tool`: Retrieve client background information for medical-related queries
    
    QUALITY ASSURANCE:
    - Ensure all responses are complete, accurate, and client-appropriate
    - Verify technical accuracy without compromising accessibility
    - Maintain professional tone and consistent messaging
    - Follow up on any gaps or inconsistencies in specialist responses

    You must use tools wisely and only when absolutely necessary. Carefully analyze the query and determine if a tool is truly essential to accomplish the task. If it is, select only the most suitable tool and use it with precision. If it is not required, do NOT use any tools. Avoid unnecessary or excessive tool use—apply them only when they are critical to achieving accurate, efficient, and relevant results.
    
    Client Query: {query}
    """,
    
    expected_output="""
    Comprehensive client response including:
    - Direct answer to client's specific query
    - Coordinated insights from relevant specialists
    - Clear next steps and action items
    - Timeline for implementation or follow-up
    - Unified, professional communication hiding operational complexity
    - Seamless client experience with single point of contact
    - Documentation of delegation and coordination for progress tracking
    """,
    
    tools=[ruby_progress_data_tool, user_medical_search_tool],
    agent=Ruby
)

# TASK 2: PROGRESS TRACKING AND CLIENT SUCCESS MONITORING
progress_tracking_management_task = Task(
    description="""
    Maintain comprehensive tracking of client progress across all health domains and coordinate regular progress assessments.
    
    Your responsibilities include:
    - Track client engagement and satisfaction metrics across all specialist areas
    - Monitor adherence to plans created by specialists (diet, exercise, medical recommendations)
    - Consolidate progress data from all team members into unified client progress reports
    - Identify trends, improvements, and areas requiring attention
    - Coordinate regular check-ins with clients to gather feedback and assess satisfaction
    - Flag potential issues before they become major problems
    - Prepare progress summaries for `Neel` to use in strategic reviews
    - Update client records with progress information and save weekly progress reports
    
    TOOL USAGE:
    - `ruby_progress_data_tool`: Read existing progress data to analyze trends and patterns
    - `ruby_update_record_tool`: Save weekly progress reports and update client records with new progress information
    - `user_medical_search_tool`: Access client background information for context in progress analysis
    
    PROGRESS MONITORING AREAS:
    - Medical: Lab results, symptom tracking, medication adherence (coordinate with drwarren)
    - Performance: Wearable data trends, fitness improvements, recovery patterns (coordinate with advik)
    - Nutrition: Diet plan adherence, weight management, energy levels (coordinate with Carla)
    - Exercise: Workout completion, strength gains, injury prevention (coordinate with Rachel)
    - Overall: Client satisfaction, goal achievement, quality of life improvements
    
    WEEKLY PROGRESS REPORT GENERATION:
    - Compile comprehensive weekly progress data from all specialists
    - Save weekly progress summary as {weekly_progress_summary} using `ruby_update_record_tool`
    - Ensure Neel can access this data via `ruby_progress_data_tool` for strategic reviews
    
    ALERT SYSTEM:
    - Red flags: Non-adherence patterns, declining metrics, client dissatisfaction
    - Yellow flags: Plateaus, minor concerns, scheduling issues
    - Green flags: Excellent progress, high engagement, goal achievements

    You must use tools wisely and only when absolutely necessary. Carefully analyze the query and determine if a tool is truly essential to accomplish the task. If it is, select only the most suitable tool and use it with precision. If it is not required, do NOT use any tools. Avoid unnecessary or excessive tool use—apply them only when they are critical to achieving accurate, efficient, and relevant results.
    """,
    
    expected_output="""
    Comprehensive progress tracking report including:
    - Current status across all health domains with specific metrics
    - Trend analysis comparing recent performance to baselines
    - Adherence rates for all specialist-created plans and recommendations
    - Client satisfaction assessment with feedback summary
    - Alert notifications requiring immediate attention or celebration
    - Progress toward long-term health goals with milestone tracking
    - Recommendations for plan adjustments based on progress patterns
    - Weekly progress summary saved for Neel's strategic review access
    - Updated client records with all progress information documented
    """,
    
    tools=[ruby_progress_data_tool, ruby_update_record_tool, user_medical_search_tool],
    agent=Ruby
)

# TASK 3: TEAM COORDINATION AND WORKFLOW MANAGEMENT
team_coordination_workflow_task = Task(
    description="""
    Coordinate seamless collaboration between all specialists to ensure integrated, holistic client care.
    
    Your responsibilities include:
    - Facilitate communication between specialists when collaborative approaches are needed
    - Ensure all team members have access to relevant client information and context
    - Coordinate timing of interventions to avoid conflicts (e.g., training intensity during medical treatments)
    - Manage workflow priorities and resource allocation across the team
    - Resolve conflicts between specialist recommendations with medical oversight priority
    - Ensure consistent messaging and approach across all specialist communications
    - Coordinate regular team meetings for complex client cases
    - Track team performance and identify opportunities for process improvement
    
    TOOL USAGE:
    - `ruby_progress_data_tool`: Access comprehensive client data to share relevant context with specialists
    - `user_medical_search_tool`: Retrieve client background for team coordination decisions
    - `ruby_update_record_tool`: Document team coordination decisions and workflow improvements
    
    COLLABORATION SCENARIOS:
    - Medical concerns affecting training plans → Coordinate drwarren and Rachel using client medical data
    - Nutrition optimization for performance → Coordinate Carla and advik using progress metrics
    - Recovery issues impacting multiple domains → Coordinate all relevant specialists with comprehensive data
    - Client dissatisfaction requiring comprehensive response → Coordinate with Neel using progress data and client context
    
    WORKFLOW MANAGEMENT:
    - Prioritize urgent medical issues over optimization requests (use medical search tool for context)
    - Balance specialist workloads to ensure timely responses
    - Ensure proper handoffs between team members with complete data context
    - Maintain documentation of all collaborative decisions and outcomes using update tool

    You must use tools wisely and only when absolutely necessary. Carefully analyze the query and determine if a tool is truly essential to accomplish the task. If it is, select only the most suitable tool and use it with precision. If it is not required, do NOT use any tools. Avoid unnecessary or excessive tool use—apply them only when they are critical to achieving accurate, efficient, and relevant results.
    """,
    
    expected_output="""
    Team coordination summary including:
    - Current collaborative projects and their status
    - Workflow optimization recommendations and process improvements
    - Conflict resolution outcomes and decision documentation
    - Team performance metrics and individual specialist contributions
    - Resource allocation recommendations for optimal client service
    - Communication protocols ensuring seamless client experience
    - Process documentation for complex multi-specialist cases saved via update tool
    - Quality assurance measures for consistent service delivery
    """,
    
    tools=[ruby_progress_data_tool, ruby_update_record_tool, user_medical_search_tool],
    agent=Ruby,
    #context=[drwarren, advik, Carla, Rachel, Neel]
)

# TASK 4: CLIENT ONBOARDING AND INITIAL ASSESSMENT COORDINATION
client_onboarding_coordination_task = Task(
    description="""
    Lead comprehensive client onboarding process ensuring all specialists have necessary information to provide personalized care.
    
    Your responsibilities include:
    - Conduct initial client assessment to understand goals, preferences, and constraints
    - Coordinate data collection from all specialists (medical history, fitness assessment, nutrition preferences, etc.)
    - Ensure all specialists have comprehensive client profiles for personalized planning
    - Set realistic expectations and timelines for goal achievement
    - Create integrated onboarding timeline coordinating all specialist initial assessments
    - Establish communication preferences and check-in schedules
    - Document all initial data and create baseline metrics for future progress tracking
    
    TOOL USAGE:
    - `user_medical_search_tool`: Access and update initial client background information and medical history
    - `ruby_update_record_tool`: Document all initial assessment data, baseline metrics, and onboarding information as {onboarding_data}
    - `ruby_progress_data_tool`: Create initial progress tracking framework for ongoing monitoring
    
    ONBOARDING CHECKLIST:
    - Medical: Health history, current conditions, medications, lab work needs (document via update tool)
    - Performance: Fitness level, wearable device setup, activity preferences (save baseline data)
    - Nutrition: Dietary restrictions, preferences, current eating patterns, goals (document preferences)
    - Exercise: Movement assessment needs, injury history, activity preferences (save assessment data)
    - Success: Goal setting, communication preferences, success metrics definition (document via update tool)
    
    INTEGRATION REQUIREMENTS:
    - Ensure all specialist plans complement rather than conflict with each other
    - Establish clear priorities when goals or recommendations overlap (document decisions)
    - Create realistic timeline for achieving integrated health outcomes (save timeline via update tool)

    You must use tools wisely and only when absolutely necessary. Carefully analyze the query and determine if a tool is truly essential to accomplish the task. If it is, select only the most suitable tool and use it with precision. If it is not required, do NOT use any tools. Avoid unnecessary or excessive tool use—apply them only when they are critical to achieving accurate, efficient, and relevant results.
    """,
    
    expected_output="""
    Complete client onboarding package including:
    - Comprehensive client profile with goals, preferences, and constraints
    - Integrated assessment timeline coordinating all specialist evaluations
    - Baseline metrics established across all health domains and saved via update tool
    - Initial care plan with coordinated specialist interventions
    - Communication schedule and client engagement protocols
    - Realistic timeline and expectations for goal achievement
    - All initial data documented in progress tracking system for ongoing monitoring
    - Quality assurance checklist ensuring comprehensive onboarding
    - Handoff protocols to all relevant specialists with proper context from medical search tool
    """,
    
    tools=[ruby_progress_data_tool, ruby_update_record_tool, user_medical_search_tool],
    agent=Ruby,
    #context=[drwarren, advik, Carla, Rachel, Neel]
)

# TASK 5: CRISIS MANAGEMENT AND URGENT RESPONSE COORDINATION
crisis_management_coordination_task = Task(
    description="""
    Handle urgent situations and coordinate rapid response across all team members for critical client needs.
    
    Your responsibilities include:
    - Identify and classify urgent situations requiring immediate attention
    - Coordinate rapid response from appropriate specialists based on crisis type
    - Ensure proper medical oversight for any health-related emergencies
    - Manage client communication during crisis situations with appropriate urgency and calm professionalism
    - Coordinate follow-up care and monitoring after crisis resolution
    - Document crisis response for process improvement and future reference
    - Coordinate with `Neel` for relationship management during difficult situations
    
    TOOL USAGE:
    - `user_medical_search_tool`: Quickly access client medical history and context for health-related emergencies
    - `ruby_progress_data_tool`: Review recent progress patterns to understand crisis context
    - `ruby_update_record_tool`: Document crisis response, outcomes, and lessons learned as {crisis_response_log}
    
    CRISIS CATEGORIES:
    - Medical Emergency: Use medical search tool for context, coordinate with drwarren for immediate guidance
    - Injury/Safety: Access medical history, coordinate with Rachel and drwarren for proper assessment
    - Severe Client Dissatisfaction: Use progress data to understand context, coordinate with Neel
    - Data/Privacy Issues: Handle directly with appropriate specialist consultation, document response
    - Performance Concerns: Review progress data, coordinate rapid assessment and intervention planning
    
    RESPONSE PROTOCOLS:
    - Triage urgency level using available client data and activate appropriate response team
    - Ensure clear, frequent communication with client during crisis
    - Coordinate specialist response without overwhelming client with multiple contacts
    - Document all crisis responses and outcomes via update tool for continuous improvement

    You must use tools wisely and only when absolutely necessary. Carefully analyze the query and determine if a tool is truly essential to accomplish the task. If it is, select only the most suitable tool and use it with precision. If it is not required, do NOT use any tools. Avoid unnecessary or excessive tool use—apply them only when they are critical to achieving accurate, efficient, and relevant results.
    """,
    
    expected_output="""
    Crisis management response including:
    - Crisis assessment and classification with urgency level based on client data analysis
    - Coordinated specialist response plan with clear roles and timelines
    - Client communication strategy maintaining confidence and transparency
    - Immediate action steps with responsible team members assigned
    - Follow-up monitoring plan ensuring complete crisis resolution
    - Complete crisis documentation saved via update tool with lessons learned
    - Process improvement recommendations for future crisis management
    - Relationship management strategy coordinated with Neel using progress data context
    - Medical safety verification with drwarren oversight when applicable using medical search data
    """,
    
    tools=[ruby_progress_data_tool, ruby_update_record_tool, user_medical_search_tool],
    agent=Ruby,
    #context=[drwarren, advik, Carla, Rachel, Neel]
)

# TASK 6: QUALITY ASSURANCE AND SERVICE STANDARDIZATION
quality_assurance_standardization_task = Task(
    description="""
    Maintain consistent service quality and standardization across all specialist interactions while ensuring personalized care.
    
    Your responsibilities include:
    - Monitor quality and consistency of all specialist communications and recommendations
    - Ensure all client-facing materials meet professional standards and brand consistency
    - Coordinate regular team training and knowledge sharing sessions
    - Maintain service delivery standards and protocols across all team members
    - Collect and analyze client feedback for continuous service improvement
    - Implement quality improvement initiatives based on client feedback and performance metrics
    - Ensure all specialist recommendations are clearly explained and actionable for clients
    - Coordinate regular service delivery reviews and optimization sessions
    
    TOOL USAGE:
    - `ruby_progress_data_tool`: Access client satisfaction metrics and service delivery performance data
    - `user_medical_search_tool`: Review client profiles to ensure personalized quality standards
    - `ruby_update_record_tool`: Document quality improvement initiatives, team training records, and service standards as {quality_assurance_log}
    
    QUALITY STANDARDS:
    - Communication: Professional, clear, empathetic, and actionable (monitor via progress data)
    - Accuracy: Evidence-based, medically safe, and individually appropriate (verify against client profiles)
    - Timeliness: Responsive within established timeframes for each query type (track via progress data)
    - Consistency: Unified approach and messaging across all specialists (document standards via update tool)
    - Personalization: Tailored to individual client needs, goals, and preferences (verify against medical search data)
    
    CONTINUOUS IMPROVEMENT:
    - Regular client satisfaction surveys and feedback analysis using progress data tool
    - Team performance metrics tracking and optimization documented via update tool
    - Process refinement based on service delivery outcomes saved as improvement logs
    - Knowledge sharing and best practice documentation using update tool

    You must use tools wisely and only when absolutely necessary. Carefully analyze the query and determine if a tool is truly essential to accomplish the task. If it is, select only the most suitable tool and use it with precision. If it is not required, do NOT use any tools. Avoid unnecessary or excessive tool use—apply them only when they are critical to achieving accurate, efficient, and relevant results.
    """,
    
    expected_output="""
    Quality assurance report including:
    - Current service quality metrics accessed via progress data tool across all specialists and client interactions
    - Client feedback analysis from progress data with trends and improvement opportunities identified
    - Team performance assessment with individual and collective strengths and development areas
    - Process improvement recommendations with implementation timelines documented via update tool
    - Service standardization updates ensuring consistent, high-quality client experience
    - Training and development recommendations for team skill enhancement saved as training logs
    - Quality metrics dashboard for ongoing monitoring and optimization
    - Best practices documentation saved via update tool for consistent service delivery excellence
    """,
    
    tools=[ruby_progress_data_tool, ruby_update_record_tool, user_medical_search_tool],
    agent=Ruby,
    #context=[drwarren, advik, Carla, Rachel, Neel]
)

# TASK 7: WEEKLY PROGRESS REPORT GENERATION FOR STRATEGIC REVIEW
weekly_progress_report_generation_task = Task(
    description="""
    Generate comprehensive weekly progress reports that provide Neel with detailed client success data for strategic reviews and relationship management.
    
    Your responsibilities include:
    - Compile weekly progress data from all specialists across all health domains
    - Analyze trends, improvements, and areas of concern from the past week
    - Create executive summary highlighting key wins, challenges, and strategic opportunities
    - Document client engagement levels, satisfaction indicators, and adherence metrics
    - Prepare strategic insights for Neel's customer success initiatives
    - Maintain consistent weekly reporting schedule for predictable strategic planning
    - Archive weekly reports for quarterly and annual strategic reviews
    
    TOOL USAGE:
    - `ruby_progress_data_tool`: Access comprehensive client progress data from all specialists for analysis
    - `ruby_update_record_tool`: Save weekly progress report as {weekly_progress_report_YYYY_MM_DD} for Neel's access
    - `user_medical_search_tool`: Include relevant client context and background for strategic interpretation
    
    WEEKLY REPORT STRUCTURE:
    - Executive Summary: Key highlights, concerns, and strategic opportunities
    - Medical Progress: Health outcomes, lab results, medication adherence (from drwarren data)
    - Performance Analytics: Wearable data trends, recovery patterns, fitness improvements (from advik data)
    - Nutrition Compliance: Diet adherence, weight management, energy levels (from Carla data)
    - Exercise Progression: Workout completion, strength gains, movement quality (from Rachel data)
    - Client Satisfaction: Engagement levels, feedback, communication preferences
    - Strategic Recommendations: Action items for customer success and relationship management
    
    NEEL ACCESS INTEGRATION:
    - Ensure all weekly reports are formatted for easy strategic interpretation
    - Include quantified metrics that support ROI discussions and value demonstration
    - Highlight client success stories and areas requiring strategic attention
    - Provide trend analysis that supports quarterly business reviews and strategic planning

    You must use tools wisely and only when absolutely necessary. Carefully analyze the query and determine if a tool is truly essential to accomplish the task. If it is, select only the most suitable tool and use it with precision. If it is not required, do NOT use any tools. Avoid unnecessary or excessive tool use—apply them only when they are critical to achieving accurate, efficient, and relevant results.
    """,
    
    expected_output="""
    Comprehensive weekly progress report including:
    - Executive summary with key performance indicators and strategic insights
    - Domain-specific progress analysis (medical, performance, nutrition, exercise) with quantified outcomes
    - Client satisfaction assessment with engagement metrics and feedback summary
    - Trend analysis comparing current week to previous periods and established baselines
    - Strategic opportunities and recommendations for customer success initiatives
    - Alert notifications for areas requiring immediate strategic attention or celebration
    - Adherence metrics across all specialist-created plans and interventions
    - Weekly progress report saved via update tool with timestamp for Neel's strategic review access
    - Action items and follow-up recommendations for continued client success optimization
    """,
    
    tools=[ruby_progress_data_tool, ruby_update_record_tool, user_medical_search_tool],
    agent=Ruby,
    #context=[Neel]
)