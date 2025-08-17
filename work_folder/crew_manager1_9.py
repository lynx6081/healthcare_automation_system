from crewai import Crew, Process
import sys
import os

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
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure your agents.py, tasks2.py, and tool2.py files are in the same directory")

class HealthCrewManager:
    def __init__(self):
        self.setup_crew()
    
    def setup_crew(self):
        """Initialize the CrewAI crew with all agents and tasks"""
        try:
            # Define worker agents (exclude manager agent Ruby from this list)
            self.worker_agents = [drwarren, advik, Carla, Rachel, Neel]
            
            # Define primary tasks (the most commonly used ones)
            self.primary_tasks = [
                project_task,  # Main orchestration task
                client_query_orchestration_task,  # Ruby's main task
                medical_research,  # Warren's main task
                wearable_data_analysis_task,  # Advik's main task
                nutrition_consultation_task,  # Carla's main task
                physiotherapy_consultation_task,  # Rachel's main task
                customer_success_consultation_task,  # Neel's main task
            ]
            
            # Initialize the crew - FIXED: Only worker agents in the agents list
            self.crew = Crew(
                agents=self.worker_agents,  # Only worker agents, not the manager
                tasks=self.primary_tasks,
                process=Process.hierarchical,
                manager_agent=Ruby,  # Manager agent specified separately
                verbose=True,
                memory=True
            )
            
            print("Health Crew initialized successfully!")
            
        except Exception as e:
            print(f"Error initializing crew: {e}")
            # Fallback to a simple setup
            self.crew = None
    
    def process_query(self, query: str) -> dict:
        """Process user query through the crew"""
        try:
            if self.crew is None:
                return {
                    'content': "I'm sorry, the system is currently initializing. Please try again in a moment.",
                    'agent': 'System'
                }
            
            # Execute the crew with the user query
            result = self.crew.kickoff(inputs={'query': query})
            
            # Parse the result
            if hasattr(result, 'raw'):
                content = result.raw
            else:
                content = str(result)
            
            return {
                'content': content,
                'agent': 'Ruby',
                'timestamp': None
            }
            
        except Exception as e:
            print(f"Error processing query: {e}")
            return {
                'content': f"I encountered an error while processing your request. Let me help you with what I can. Your query was: '{query}'. Could you please rephrase or provide more specific details?",
                'agent': 'Ruby',
                'timestamp': None
            }
    
    def get_agent_status(self) -> dict:
        """Get status of all agents"""
        all_agents = [Ruby] + self.worker_agents  # Include Ruby for status display
        status = {}
        for agent in all_agents:
            status[agent.name] = {
                'role': agent.role,
                'available': True,  # In a real implementation, this would check actual availability
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
                'weekly_report': "Generate my weekly health progress report",
                'medication_reminder': "Check my medication schedule and remind me of any due medications",
                'exercise_update': "Update my exercise plan based on recent progress",
                'nutrition_review': "Review my nutrition plan and suggest any needed adjustments",
                'health_checkup': "Schedule my next health checkup and review current status"
            }
            
            query = automation_queries.get(task_type, f"Handle automation task: {task_type}")
            if context:
                query += f" Context: {context}"
            
            return self.process_query(query)
            
        except Exception as e:
            return {
                'content': f"Error in automation task {task_type}: {str(e)}",
                'agent': 'System',
                'timestamp': None
            }

# Fallback responses for when CrewAI isn't available
class FallbackManager:
    def __init__(self):
        self.responses = {
            'greeting': "Hello! I'm Ruby, your health management assistant. I'm here to coordinate your care. How can I help you today?",
            'medical': "I'll connect you with Dr. Warren for medical guidance. He'll review your query and provide expert medical advice.",
            'nutrition': "Let me get Dr. Carla, our nutritionist, to help you with your dietary questions and meal planning.",
            'exercise': "I'll have Rachel, our physiotherapist, assist you with exercise planning and movement guidance.",
            'data': "Dr. Advik, our performance scientist, will analyze your wearable data and provide insights.",
            'support': "I'll coordinate with Neel for any service-related concerns or strategic support you need.",
            'default': "I understand you need assistance. Let me coordinate with the right team member to give you the best help possible."
        }
    
    def process_query(self, query: str) -> dict:
        """Process query with fallback responses"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['hello', 'hi', 'hey', 'start']):
            response = self.responses['greeting']
        elif any(word in query_lower for word in ['medical', 'doctor', 'health', 'lab', 'test']):
            response = self.responses['medical']
        elif any(word in query_lower for word in ['nutrition', 'diet', 'food', 'meal']):
            response = self.responses['nutrition']
        elif any(word in query_lower for word in ['exercise', 'workout', 'training', 'fitness']):
            response = self.responses['exercise']
        elif any(word in query_lower for word in ['data', 'wearable', 'sleep', 'recovery']):
            response = self.responses['data']
        elif any(word in query_lower for word in ['problem', 'issue', 'complaint', 'dissatisfied']):
            response = self.responses['support']
        else:
            response = self.responses['default']
        
        return {
            'content': response,
            'agent': 'Ruby (Fallback)',
            'timestamp': None
        }

# Try to use the full CrewAI implementation, fallback if needed
try:
    DefaultHealthCrewManager = HealthCrewManager
except:
    DefaultHealthCrewManager = FallbackManager
    print("Using fallback manager due to CrewAI import issues")