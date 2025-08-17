from crewai import Crew, Process
import sys
import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError

# Add the directory containing your original files to the path
sys.path.append('.')

# Import your existing agents and tasks
try:
    from agents import Ruby, drwarren, advik, Carla, Rachel, Neel
    from tasks2 import (
        project_task, medical_research, medical_report_automation,
        collaboration_by_warren, wearable_data_analysis_task,
        experiment_hypothesis_task, advik_performance_collaboration_task,
        continuous_monitoring_task, data_quality_management_task,
        diet_plan_generation_task, nutrition_consultation_task,
        carla_collaboration_integration_task, physiotherapy_consultation_task,
        exercise_program_generation_task, rachel_collaboration_integration_task,
        customer_success_consultation_task, strategic_review_management_task,
        neel_collaboration_integration_task, client_query_orchestration_task,
        progress_tracking_management_task, team_coordination_workflow_task,
        client_onboarding_coordination_task, crisis_management_coordination_task,
        quality_assurance_standardization_task, weekly_progress_report_generation_task
    )
    IMPORTS_SUCCESSFUL = True
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure your agents.py, tasks2.py, and tool2.py files are in the same directory")
    IMPORTS_SUCCESSFUL = False

class HealthCrewManager:
    def __init__(self):
        self.setup_crew()
        self.check_environment()
    
    def check_environment(self):
        """Check for required environment variables and setup"""
        required_env_vars = [
            'OPENAI_API_KEY',
            'SERPER_API_KEY',
            'TAVILY_API_KEY'
        ]
        
        missing_vars = []
        for var in required_env_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            print(f"Warning: Missing environment variables: {', '.join(missing_vars)}")
            print("The crew will use fallback mode for queries requiring these APIs")
        
        # Create docs directory if it doesn't exist
        docs_dir = '../docs'
        if not os.path.exists(docs_dir):
            os.makedirs(docs_dir)
            print(f"Created docs directory: {docs_dir}")
        
        # Create empty files if they don't exist
        required_files = [
            'profile.txt', 'reportformat.txt', 'dr_records.txt',
            'advic_records.txt', 'carla_records.txt', 'rachel_records.txt', 'ruby_records.txt'
        ]
        
        for file_name in required_files:
            file_path = os.path.join(docs_dir, file_name)
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    f.write(f"# {file_name} - Health Management System Data\n")
                    f.write("# This file stores data for the health management system\n\n")
                print(f"Created empty file: {file_path}")
    
    def setup_crew(self):
        """Initialize the CrewAI crew with all agents and tasks"""
        try:
            if not IMPORTS_SUCCESSFUL:
                self.crew = None
                return
            
            # Define worker agents (exclude manager agent Ruby from this list)
            self.worker_agents = [drwarren, advik, Carla, Rachel, Neel]
            
            # Start with basic tasks to avoid complexity issues
            self.primary_tasks = [
                client_query_orchestration_task,  # Ruby's main task
                medical_research,  # Warren's main task
                wearable_data_analysis_task,  # Advik's main task
                nutrition_consultation_task,  # Carla's main task
                physiotherapy_consultation_task,  # Rachel's main task
                customer_success_consultation_task,  # Neel's main task
            ]
            
            # Initialize the crew with basic configuration
            self.crew = Crew(
                agents=self.worker_agents,  # Only worker agents, not the manager
                tasks=self.primary_tasks,
                process=Process.hierarchical,
                manager_agent=Ruby,  # Manager agent specified separately
                verbose=False,  # Reduced verbosity to avoid clutter
                memory=False,  # Disable memory initially to avoid issues
            )
            
            print("Health Crew initialized successfully!")
            
        except Exception as e:
            print(f"Error initializing crew: {e}")
            print("Falling back to simple response system")
            self.crew = None
    
    def _execute_with_timeout(self, func, timeout_seconds=30):
        """Execute a function with timeout using ThreadPoolExecutor (Windows compatible)"""
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(func)
            try:
                return future.result(timeout=timeout_seconds)
            except FuturesTimeoutError:
                return None
    
    def process_query(self, query: str) -> dict:
        """Process user query through the crew"""
        try:
            if self.crew is None:
                return self.fallback_response(query)
            
            # Add input validation
            if not query or not query.strip():
                return {
                    'content': "I didn't receive a clear question. Could you please ask me something specific about your health?",
                    'agent': 'Ruby'
                }
            
            # Limit query length to prevent issues
            if len(query) > 1000:
                query = query[:1000] + "..."
            
            # Execute the crew with the user query
            print(f"Processing query: {query[:50]}...")
            
            # Define the crew execution function
            def execute_crew():
                return self.crew.kickoff(inputs={'query': query})
            
            # Execute with timeout (Windows compatible)
            result = self._execute_with_timeout(execute_crew, timeout_seconds=30)
            
            if result is None:
                return {
                    'content': "Your query is taking longer than expected. Let me provide a quick response instead.",
                    'agent': 'Ruby'
                }
            
            # Parse the result
            if hasattr(result, 'raw'):
                content = result.raw
            elif hasattr(result, 'content'):
                content = result.content
            else:
                content = str(result)
            
            # Ensure content is not empty
            if not content or content.strip() == "":
                content = "I've processed your query but didn't generate a clear response. Could you please rephrase your question?"
            
            return {
                'content': content,
                'agent': 'Ruby',
                'timestamp': None
            }
            
        except Exception as e:
            print(f"Error processing query: {e}")
            return self.fallback_response(query)
    
    def fallback_response(self, query: str) -> dict:
        """Provide fallback response when crew fails"""
        query_lower = query.lower()
        
        # Determine appropriate response based on query content
        if any(word in query_lower for word in ['hello', 'hi', 'hey', 'start']):
            content = "Hello! I'm Ruby, your health management assistant. I'm here to coordinate your care with our expert team. How can I help you today?"
        elif any(word in query_lower for word in ['medical', 'doctor', 'health', 'lab', 'test', 'symptom', 'headache', 'pain', 'sick']):
            content = "I understand you have a medical concern. I'll connect you with Dr. Warren, our medical strategist, who can provide expert medical guidance. For immediate medical emergencies, please contact emergency services. For your headache concern, Dr. Warren can help assess potential causes and recommend appropriate treatment options based on your health profile."
        elif any(word in query_lower for word in ['nutrition', 'diet', 'food', 'meal', 'eating']):
            content = "For your nutrition question, I'll coordinate with Dr. Carla, our clinical nutritionist. She can help with personalized meal plans, dietary analysis, and supplement guidance."
        elif any(word in query_lower for word in ['exercise', 'workout', 'training', 'fitness', 'movement']):
            content = "I'll have Rachel, our elite physiotherapist, assist you with exercise planning and movement guidance. She can create personalized exercise programs and help with injury prevention."
        elif any(word in query_lower for word in ['data', 'wearable', 'sleep', 'recovery', 'hrv']):
            content = "Dr. Advik, our performance scientist, will analyze your wearable data and provide insights on sleep, recovery, and performance optimization."
        elif any(word in query_lower for word in ['problem', 'issue', 'complaint', 'dissatisfied', 'concern']):
            content = "I'll coordinate with Neel, our customer success manager, to address your concerns and ensure you receive the best possible service."
        else:
            content = f"I understand you're asking about: '{query}'. Let me coordinate with the appropriate team member to provide you with expert guidance. Could you provide a bit more detail about what specific aspect you'd like help with?"
        
        return {
            'content': content,
            'agent': 'Ruby',
            'timestamp': None
        }
    
    def get_agent_status(self) -> dict:
        """Get status of all agents"""
        all_agents = [Ruby] + self.worker_agents if IMPORTS_SUCCESSFUL else []
        status = {}
        
        if not all_agents:
            return {"System": {"role": "Fallback", "available": True, "specialization": "Basic responses"}}
        
        for agent in all_agents:
            status[agent.name] = {
                'role': agent.role,
                'available': True,
                'specialization': self.get_agent_specialization(agent.name)
            }
        return status
    
    def get_agent_specialization(self, agent_name: str) -> str:
        """Get agent specialization description"""
        specializations = {
            'Ruby': 'General coordination, task delegation, and client management',
            'drwarren': 'Medical analysis, lab results, health strategy',
            'advik': 'Performance data, wearables analysis, recovery optimization',
            'Carla': 'Nutrition planning, dietary analysis, supplement guidance',
            'Rachel': 'Exercise programming, physiotherapy, movement analysis',
            'Neel': 'Customer success, strategic reviews, relationship management'
        }
        return specializations.get(agent_name, 'General assistance')
    
    def trigger_automation_task(self, task_type: str, context: dict = None) -> dict:
        """Trigger automated tasks like reports, reminders, etc."""
        try:
            automation_queries = {
                'weekly_report': "Generate my weekly health progress report with current status across all health domains",
                'medication_reminder': "Check my medication schedule and provide reminders for any due medications",
                'exercise_update': "Review and update my exercise plan based on recent progress and performance data",
                'nutrition_review': "Review my current nutrition plan and suggest any needed adjustments",
                'health_checkup': "Schedule my next health checkup and provide a current health status overview"
            }
            
            query = automation_queries.get(task_type, f"Handle automation task: {task_type}")
            if context:
                query += f" Additional context: {context}"
            
            return self.process_query(query)
            
        except Exception as e:
            return {
                'content': f"I encountered an issue with the automation task '{task_type}'. Let me provide what information I can. Please try again or contact support if the issue persists.",
                'agent': 'Ruby',
                'timestamp': None
            }

# Use the improved manager
DefaultHealthCrewManager = HealthCrewManager