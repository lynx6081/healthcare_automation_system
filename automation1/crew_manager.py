from crewai import Crew, Process
import sys
import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from datetime import datetime
import signal

# Add the directory containing your original files to the path
sys.path.append('.')

# Mock Response System for API optimization
class MockResponseManager:
    def __init__(self):
        self.mock_responses = {
            'medical': "I understand your medical concern. Based on general medical knowledge, I recommend consulting with healthcare professionals for proper evaluation. In the meantime, monitor your symptoms and maintain healthy lifestyle habits.",
            'nutrition': "For nutrition guidance, I recommend focusing on balanced meals with proper macronutrients - lean proteins, complex carbohydrates, healthy fats, and plenty of vegetables. Stay hydrated and consider meal timing around your activities.",
            'exercise': "For exercise planning, start with proper warm-up, focus on progressive overload, and ensure adequate recovery. Listen to your body and adjust intensity based on your current fitness level and any limitations.",
            'performance': "Based on performance data patterns, focus on consistent recovery, quality sleep, stress management, and balanced training. Track your metrics regularly and adjust your approach based on trends.",
            'customer_success': "I'm here to help resolve any concerns and ensure you get maximum value from our health program. Let me understand your specific needs and coordinate with the appropriate team members.",
            'general': "I'm processing your request and will coordinate with the appropriate specialist to provide you with the best guidance. Please provide any additional context that might help."
        }
    
    def get_mock_response(self, query_type, query):
        return {
            'content': self.mock_responses.get(query_type, self.mock_responses['general']),
            'agent': 'Ruby',
            'timestamp': datetime.now()
        }

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
    print("✅ Successfully imported agents and tasks")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure your agents.py, tasks2.py, and tool2.py files are in the same directory")
    IMPORTS_SUCCESSFUL = False

class HealthCrewManager:
    def __init__(self):
        print("🔄 Initializing HealthCrewManager...")
        self.mock_manager = MockResponseManager()
        self.api_call_count = 0
        self.api_limit = int(os.getenv('API_USAGE_LIMIT', '50'))
        self.check_environment()
        self.setup_crew()
    
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
            print(f"⚠️ Warning: Missing environment variables: {', '.join(missing_vars)}")
            print("The crew will use fallback mode for queries requiring these APIs")
        
        # Create docs directory if it doesn't exist
        docs_dir = '../docs'
        if not os.path.exists(docs_dir):
            os.makedirs(docs_dir)
            print(f"📁 Created docs directory: {docs_dir}")
        
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
                print(f"📄 Created empty file: {file_path}")
    
    def setup_crew(self):
        """Initialize the CrewAI crew with simplified configuration"""
        try:
            if not IMPORTS_SUCCESSFUL:
                print("⚠️ Imports failed, crew will be None")
                self.crew = None
                return
            
            # Define worker agents (exclude manager agent Ruby from this list)
            self.worker_agents = [drwarren, advik, Carla, Rachel, Neel]
            
            # Use only essential tasks to avoid complexity
            # self.primary_tasks = [
            #     project_task,
            #     medical_research,  # Warren's main task - REMOVED Ruby's task
            #     nutrition_consultation_task,  # Carla's main task
            #     physiotherapy_consultation_task,  # Rachel's main task
            #     customer_success_consultation_task,  
            # ]
            
            # Initialize the crew with SIMPLIFIED configuration
            self.crew = Crew(
                agents=[drwarren, advik, Carla, Rachel, Neel],
                tasks=[project_task],
                process=Process.hierarchical,
                manager_agent=Ruby,
                verbose=False,  # Reduce verbose to avoid log spam
                memory=False,
                max_iter=1,  # Force single iteration
                max_execution_time=45,  # Shorter timeout to prevent hanging
                # step_callback=lambda step: print(f"Step completed: {step.tool_name if hasattr(step, 'tool_name') else 'Task step'}")
            )
            
            print("✅ Health Crew initialized successfully!")
            
        except Exception as e:
            print(f"❌ Error initializing crew: {e}")
            print("Falling back to simple response system")
            self.crew = None
    
    def should_use_mock_response(self):
        """Check if we should use mock response to save API calls"""
        use_mock = os.getenv('USE_MOCK_RESPONSES', 'false').lower() == 'true'
        api_limit_reached = self.api_call_count >= self.api_limit
        return False  # Force actual crew execution for testing
    
    def classify_query(self, query):
        """Classify query type for mock responses and delegation"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['doctor', 'medical', 'health', 'symptom', 'lab', 'test', 'diagnosis', 'medication', 'headache', 'pain', 'hurt']):
            return 'medical'
        elif any(word in query_lower for word in ['nutrition', 'diet', 'food', 'meal', 'eat', 'supplement', 'vitamin']):
            return 'nutrition'
        elif any(word in query_lower for word in ['exercise', 'workout', 'training', 'fitness', 'strength', 'movement', 'physiotherapy']):
            return 'exercise'
        elif any(word in query_lower for word in ['performance', 'data', 'wearable', 'sleep', 'recovery', 'hrv', 'heart rate']):
            return 'performance'
        elif any(word in query_lower for word in ['dissatisfied', 'problem', 'issue', 'complaint', 'unhappy', 'support']):
            return 'customer_success'
        else:
            return 'general'
    
    def get_delegation_info(self, query_type):
        """Get delegation information for frontend"""
        delegation_map = {
            'medical': {
                'agent': 'Dr Warren',
                'reason': 'medical expertise and health analysis'
            },
            'nutrition': {
                'agent': 'Dr Carla',
                'reason': 'nutrition planning and dietary guidance'
            },
            'exercise': {
                'agent': 'Rachel',
                'reason': 'exercise programming and physiotherapy expertise'
            },
            'performance': {
                'agent': 'Dr Advik',
                'reason': 'performance data analysis and wearable insights'
            },
            'customer_success': {
                'agent': 'Neel',
                'reason': 'customer success and relationship management'
            }
        }
        return delegation_map.get(query_type, {'agent': 'Ruby', 'reason': 'general coordination'})
    
    def timeout_handler(self, signum, frame):
        """Handle timeout signal"""
        raise TimeoutError("CrewAI execution timed out")
    
    def _execute_with_timeout(self, func, timeout_seconds=15):
        """Execute a function with timeout using signal alarm (Unix only)"""
        try:
            # For Unix systems, use signal
            if hasattr(signal, 'SIGALRM'):
                signal.signal(signal.SIGALRM, self.timeout_handler)
                signal.alarm(timeout_seconds)
                try:
                    result = func()
                    signal.alarm(0)  # Cancel the alarm
                    return result
                except TimeoutError:
                    print(f"⏰ Timeout after {timeout_seconds} seconds")
                    return None
                finally:
                    signal.alarm(0)  # Ensure alarm is cancelled
            else:
                # Fallback for Windows - use ThreadPoolExecutor
                with ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(func)
                    return future.result(timeout=timeout_seconds)
        except FuturesTimeoutError:
            print(f"⏰ ThreadPool timeout after {timeout_seconds} seconds")
            return None
        except Exception as e:
            print(f"❌ Error in execution: {e}")
            return None
    
    def prepare_inputs(self, query: str) -> dict:
        """Prepare simplified inputs to avoid complexity"""
        return {
            'query': query.strip(),
        }
    
    def process_query(self, query: str) -> dict:
        """Process user query with improved error handling, timeouts, and delegation info"""
        try:
            print(f"🔄 Starting to process query: {query[:50]}...")
            
            if self.crew is None:
                print("⚠️ Crew is None, using fallback")
                return self.fallback_response(query)
            
            # Input validation
            if not query or not query.strip():
                return {
                    'content': "I didn't receive a clear question. Could you please ask me something specific about your health?",
                    'agent': 'Ruby',
                    'delegation_info': None
                }
            
            # Limit query length and clean it
            query = query.strip()
            if len(query) > 500:
                query = query[:500] + "..."
            
            print(f"🔍 Classifying query type...")
            
            # Classify query for delegation
            query_type = self.classify_query(query)
            delegation_info = self.get_delegation_info(query_type)
            print(f"📋 Query type: {query_type}, delegating to: {delegation_info['agent']}")
            
            # Check if we should use mock response
            if self.should_use_mock_response():
                print("🎭 Using mock response")
                response = self.mock_manager.get_mock_response(query_type, query)
                response['delegation_info'] = delegation_info
                return response
            
            # Prepare simplified inputs
            inputs = self.prepare_inputs(query)
            print(f"📝 Prepared inputs: {inputs}")
            
            # Define crew execution with better error handling
            def execute_crew():
                try:
                    print("🚀 Starting crew execution...")
                    self.api_call_count += 1
                    result = self.crew.kickoff(inputs=inputs)
                    print("✅ Crew execution completed")
                    return result
                except Exception as e:
                    print(f"❌ Crew execution error: {e}")
                    return None
            
            # Execute with reduced timeout
            print("⏰ Executing crew with timeout...")
            result = self._execute_with_timeout(execute_crew, timeout_seconds=45)
            
            if result is None:
                print("❌ Crew execution failed or timed out, using fallback")
                fallback = self.fallback_response(query)
                fallback['delegation_info'] = delegation_info
                return fallback
            
            # Parse the result with better error handling
            try:
                print("📄 Parsing crew result...")
                # Handle different result formats more comprehensively
                if hasattr(result, 'raw') and result.raw:
                    content = str(result.raw).strip()
                elif hasattr(result, 'output') and result.output:
                    content = str(result.output).strip()  
                elif hasattr(result, 'content') and result.content:
                    content = str(result.content).strip()
                elif hasattr(result, 'result') and result.result:
                    content = str(result.result).strip()
                else:
                    content = str(result).strip()
                            
                # Clean and validate content
                content = content.strip()
                if not content or len(content) < 10:
                    print("❌ Content too short, using fallback")
                    fallback = self.fallback_response(query)
                    fallback['delegation_info'] = delegation_info
                    return fallback
                
                print(f"✅ Successfully processed query, response length: {len(content)}")
                return {
                    'content': content,
                    'agent': delegation_info['agent'],
                    'delegation_info': delegation_info,
                    'timestamp': datetime.now()
                }
                
            except Exception as e:
                print(f"❌ Result parsing error: {e}")
                fallback = self.fallback_response(query)
                fallback['delegation_info'] = delegation_info
                return fallback
            
        except Exception as e:
            print(f"❌ Error processing query: {e}")
            return self.fallback_response(query)
    
    def fallback_response(self, query: str) -> dict:
        """Provide improved fallback response when crew fails"""
        query_lower = query.lower().strip()
        query_type = self.classify_query(query)
        delegation_info = self.get_delegation_info(query_type)
        
        print(f"🔄 Generating fallback response for query type: {query_type}")
        
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

I'm connecting you with Dr. Warren, our medical strategist, who can provide more personalized guidance based on your health profile."""

        elif any(word in query_lower for word in ['hello', 'hi', 'hey', 'start']):
            content = "Hello! I'm Ruby, your health management assistant. I coordinate your care with our expert medical team including Dr. Warren (medical), Dr. Advik (performance), Dr. Carla (nutrition), Rachel (physiotherapy), and Neel (customer success). How can I help you today?"
            
        elif query_type == 'medical':
            content = f"I'll connect you with {delegation_info['agent']}, our senior medical strategist, who can provide expert medical guidance. He has access to your health profile and can offer personalized recommendations."
            
        elif query_type == 'nutrition':
            content = f"I'll coordinate with {delegation_info['agent']}, our clinical nutritionist, for your nutrition questions. She can help with meal planning, dietary analysis, and nutritional guidance."
            
        elif query_type == 'exercise':
            content = f"{delegation_info['agent']}, our elite physiotherapist, will assist with exercise and movement questions. She can create programs and provide guidance on safe, effective training."
            
        elif query_type == 'performance':
            content = f"I'm coordinating with {delegation_info['agent']}, our performance scientist, to analyze your data and provide insights on optimization strategies."
            
        else:
            content = f"I understand you're asking about: '{query}'. I'm coordinating with the appropriate specialist to provide you with expert guidance. Could you provide more specific details about what you'd like help with?"
        
        print(f"✅ Generated fallback response for {delegation_info['agent']}")
        return {
            'content': content,
            'agent': 'Ruby',
            'delegation_info': delegation_info,
            'timestamp': datetime.now()
        }
    
    def trigger_automation_task(self, task_type: str, context: dict = None) -> dict:
        """Trigger automated tasks with improved error handling"""
        try:
            automation_queries = {
                'weekly_report': "Generate my weekly health progress report",
                'quarterly_medical_report': "Generate my quarterly medical health report based on the last 3 months",
                'diet_plan_update': "Update my nutrition plan based on recent progress",
                'exercise_program_update': "Update my exercise program for the next 2 weeks",
                'performance_analysis': "Analyze my weekly performance data and provide insights",
                'medication_reminder': "Check my medication schedule",
                'health_checkup': "Schedule my health checkup"
            }
            
            query = automation_queries.get(task_type, f"Handle automated task: {task_type}")
            if context:
                query += f" Context: {context}"
            
            # For automated tasks, always include automation flag
            result = self.process_query(query)
            result['automated'] = True
            result['task_type'] = task_type
            
            return result
            
        except Exception as e:
            return {
                'content': f"I encountered an issue with the automation task '{task_type}'. Please try again or contact support if the issue persists.",
                'agent': 'Ruby',
                'automated': True,
                'task_type': task_type,
                'timestamp': datetime.now()
            }
    
    def get_agent_status(self) -> dict:
        """Get status of all agents"""
        if not IMPORTS_SUCCESSFUL:
            return {"System": {"role": "Fallback", "available": True, "specialization": "Basic responses"}}
        
        # Use agent names directly instead of accessing .name attribute
        agent_info = {
            'Assist Ruby': {'role': 'Operations Manager', 'available': True},
            'Assist Warren': {'role': 'Medical Strategist', 'available': True},
            'Assist Advik': {'role': 'Performance Scientist', 'available': True},
            'Assist Carla': {'role': 'Clinical Nutritionist', 'available': True},
            'Rachel': {'role': 'Elite Physiotherapist', 'available': True},
            'Neel': {'role': 'Customer Success Manager', 'available': True}
        }
        
        status = {}
        for agent_name, info in agent_info.items():
            status[agent_name] = {
                'role': info['role'],
                'available': info['available'],
                'specialization': self.get_agent_specialization(agent_name)
            }
        return status
        
    def get_agent_specialization(self, agent_name: str) -> str:
        """Get agent specialization description"""
        specializations = {
            'Assist Ruby': 'General coordination, task delegation, and client management',
            'Assist Warren': 'Medical analysis, lab results, health strategy',
            'Assist Advik': 'Performance data, wearables analysis, recovery optimization',
            'Assist Carla': 'Nutrition planning, dietary analysis, supplement guidance',
            'Rachel': 'Exercise programming, physiotherapy, movement analysis',
            'Neel': 'Customer success, strategic reviews, relationship management'
        }
        return specializations.get(agent_name, 'General assistance')

# Use the improved manager
DefaultHealthCrewManager = HealthCrewManager