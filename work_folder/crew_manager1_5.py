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

class MockResponseManager:
    def __init__(self):
        self.mock_responses = {
            'medical': "I understand your medical concern. Based on general medical knowledge, here are some recommendations...",
            'nutrition': "For nutrition guidance, I recommend focusing on balanced meals with proper macronutrients...",
            'exercise': "For exercise planning, start with proper warm-up and gradually increase intensity...",
            'performance': "Based on performance data patterns, focus on recovery and consistent training...",
            'customer_success': "I'm here to help resolve any concerns and ensure you get maximum value from our program..."
        }
    
    def get_mock_response(self, query_type, query):
        return {
            'content': self.mock_responses.get(query_type, "I'm processing your request with limited resources. Here's general guidance..."),
            'agent': 'Ruby',
            'timestamp': None
        }

class HealthCrewManager:
    def __init__(self):
        self.mock_manager = MockResponseManager()
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
        """Initialize the CrewAI crew with simplified configuration"""
        try:
            if not IMPORTS_SUCCESSFUL:
                self.crew = None
                return
            
            # Define worker agents (exclude manager agent Ruby from this list)
            self.worker_agents = [drwarren, advik, Carla, Rachel, Neel]
            
            # Use only essential tasks to avoid complexity
            self.primary_tasks = [
                client_query_orchestration_task,  # Ruby's main task
                medical_research,  # Warren's main task
                nutrition_consultation_task,  # Carla's main task
                physiotherapy_consultation_task,  # Rachel's main task
                customer_success_consultation_task,  # Neel's main task
            ]
            
            # Initialize the crew with SIMPLIFIED configuration
            self.crew = Crew(
                agents=self.worker_agents,  # Only worker agents
                tasks=self.primary_tasks,
                process=Process.hierarchical,
                manager_agent=Ruby,  # Manager agent specified separately
                verbose=False,  # Reduced verbosity
                memory=False,  # Disable memory to avoid issues
                max_iter=3,  # ADDED: Limit iterations to prevent infinite loops
                max_execution_time=60,  # ADDED: 60 second timeout per task
            )
            
            print("Health Crew initialized successfully!")
            
        except Exception as e:
            print(f"Error initializing crew: {e}")
            print("Falling back to simple response system")
            self.crew = None
    
    def _execute_with_timeout(self, func, timeout_seconds=20):  # REDUCED timeout from 30 to 20
        """Execute a function with timeout using ThreadPoolExecutor"""
        with ThreadPoolExecutor(max_workers=1) as executor:
            try:
                future = executor.submit(func)
                return future.result(timeout=timeout_seconds)
            except FuturesTimeoutError:
                print("Query execution timed out, using fallback response")
                return None
            except Exception as e:
                print(f"Error in execution: {e}")
                return None
    
    def prepare_inputs(self, query: str) -> dict:
        """Prepare simplified inputs to avoid complexity"""
        return {
            'query': query.strip(),  # Clean the query
            # Remove complex template variables that might cause issues
        }
    
    def process_query(self, query: str) -> dict:
        """Process user query with API optimization"""
        try:
            if self.crew is None:
                return self.fallback_response(query)
        
        # Check if we should use mock response (implement API usage counter)
        if self.should_use_mock_response():
            query_type = self.classify_query(query)
            return self.mock_manager.get_mock_response(query_type, query)
        
            
            # Input validation
            if not query or not query.strip():
                return {
                    'content': "I didn't receive a clear question. Could you please ask me something specific about your health?",
                    'agent': 'Ruby'
                }
            
            # Limit query length and clean it
            query = query.strip()
            if len(query) > 500:  # REDUCED from 1000 to 500
                query = query[:500] + "..."
            
            print(f"Processing query: {query[:50]}...")
            
            # Prepare simplified inputs
            inputs = self.prepare_inputs(query)
            
            # Define crew execution with better error handling
            def execute_crew():
                try:
                    return self.crew.kickoff(inputs=inputs)
                except Exception as e:
                    print(f"Crew execution error: {e}")
                    return None
            
            # Execute with reduced timeout
            result = self._execute_with_timeout(execute_crew, timeout_seconds=20)
            
            if result is None:
                return {
                    'content': "I'm having some technical difficulties processing your request. Let me provide you with a direct response instead.",
                    'agent': 'Ruby'
                }
            
            # Parse the result with better error handling
            try:
                if hasattr(result, 'raw'):
                    content = str(result.raw)
                elif hasattr(result, 'content'):
                    content = str(result.content)
                else:
                    content = str(result)
                
                # Clean and validate content
                content = content.strip()
                if not content or len(content) < 10:
                    return self.fallback_response(query)
                
                return {
                    'content': content,
                    'agent': 'Ruby',
                    'timestamp': None
                }
                
            except Exception as e:
                print(f"Result parsing error: {e}")
                return self.fallback_response(query)
            
        except Exception as e:
            print(f"Error processing query: {e}")
            return self.fallback_response(query)
    
    def fallback_response(self, query: str) -> dict:
        """Provide improved fallback response when crew fails"""
        query_lower = query.lower().strip()
        
        # More specific response patterns
        if any(word in query_lower for word in ['headache', 'head', 'pain', 'hurt']):
            content = """I understand you're experiencing a headache. Here's some immediate guidance:

**Immediate Steps:**
- Rest in a quiet, dark room
- Apply a cold compress to your forehead or warm compress to neck/shoulders
- Stay hydrated - drink water
- Avoid bright lights and loud sounds

**When to Seek Medical Help:**
- Severe, sudden onset headache
- Headache with fever, stiff neck, or vision changes  
- Headache after a head injury
- Persistent headache lasting more than 24 hours

**Common Causes:**
- Tension/stress
- Dehydration
- Eye strain
- Sleep issues
- Caffeine withdrawal

I'm connecting you with Dr. Warren, our medical strategist, who can provide more personalized guidance based on your health profile. For emergencies, please contact emergency services immediately."""

        elif any(word in query_lower for word in ['hello', 'hi', 'hey', 'start']):
            content = "Hello! I'm Ruby, your health management assistant. I coordinate your care with our expert medical team including Dr. Warren (medical), Dr. Advik (performance), Dr. Carla (nutrition), Rachel (physiotherapy), and Neel (customer success). How can I help you today?"
            
        elif any(word in query_lower for word in ['medical', 'doctor', 'health', 'symptom', 'sick']):
            content = "I'll connect you with Dr. Warren, our senior medical strategist, who can provide expert medical guidance. He has access to your health profile and can offer personalized recommendations. For immediate medical emergencies, please contact emergency services."
            
        elif any(word in query_lower for word in ['nutrition', 'diet', 'food', 'meal']):
            content = "I'll coordinate with Dr. Carla, our clinical nutritionist, for your nutrition questions. She can help with meal planning, dietary analysis, and nutritional guidance."
            
        elif any(word in query_lower for word in ['exercise', 'workout', 'training', 'movement']):
            content = "Rachel, our elite physiotherapist, will assist with exercise and movement questions. She can create programs and provide guidance on safe, effective training."
            
        else:
            content = f"I understand you're asking about: '{query}'. I'm coordinating with the appropriate specialist to provide you with expert guidance. Could you provide more specific details about what you'd like help with?"
        
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
            'Ms Ruby': 'General coordination, task delegation, and client management',
            'Dr Warren': 'Medical analysis, lab results, health strategy',
            'Dr Advik': 'Performance data, wearables analysis, recovery optimization',
            'Dr Carla': 'Nutrition planning, dietary analysis, supplement guidance',
            'Rachel': 'Exercise programming, physiotherapy, movement analysis',
            'Neel': 'Customer success, strategic reviews, relationship management'
        }
        return specializations.get(agent_name, 'General assistance')
    
    def trigger_automation_task(self, task_type: str, context: dict = None) -> dict:
        """Trigger automated tasks with improved error handling"""
        try:
            automation_queries = {
                'weekly_report': "Generate my weekly health progress report",
                'medication_reminder': "Check my medication schedule",
                'exercise_update': "Review my exercise plan", 
                'nutrition_review': "Review my nutrition plan",
                'health_checkup': "Schedule my health checkup"
            }
            
            query = automation_queries.get(task_type, f"Handle task: {task_type}")
            if context:
                query += f" Context: {context}"
            
            return self.process_query(query)
            
        except Exception as e:
            return {
                'content': f"I encountered an issue with the automation task '{task_type}'. Please try again or contact support if the issue persists.",
                'agent': 'Ruby',
                'timestamp': None
            }

# Use the improved manager
DefaultHealthCrewManager = HealthCrewManager