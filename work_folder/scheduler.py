# scheduler.py - Create this new file
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import json
import os

class SimpleHealthScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.users_file = 'user_schedules.json'
        self.crew = None  # Will be set later
        self.load_user_schedules()
    
    def set_crew(self, crew):
        """Set the crew instance after it's created"""
        self.crew = crew
    
    def load_user_schedules(self):
        """Load user schedules from JSON file"""
        try:
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r') as f:
                    self.users = json.load(f)
            else:
                self.users = {}
        except Exception as e:
            print(f"Error loading schedules: {e}")
            self.users = {}
    
    def save_user_schedules(self):
        """Save user schedules to JSON file"""
        try:
            with open(self.users_file, 'w') as f:
                json.dump(self.users, f, indent=2)
        except Exception as e:
            print(f"Error saving schedules: {e}")
    
    def register_user(self, user_id):
        """Register new user and schedule their first report"""
        if user_id not in self.users:
            try:
                join_date = datetime.now()
                next_report = join_date + timedelta(days=90)  # 3 months
                
                self.users[user_id] = {
                    'join_date': join_date.isoformat(),
                    'next_report_date': next_report.isoformat(),
                    'last_report_date': None
                }
                self.save_user_schedules()
                
                # Schedule the report
                self.scheduler.add_job(
                    func=self._generate_health_report,
                    trigger='date',
                    run_date=next_report,
                    args=[user_id],
                    id=f'health_report_{user_id}',
                    replace_existing=True
                )
                print(f"✅ User {user_id} registered. Health report scheduled for {next_report.strftime('%Y-%m-%d')}")
            except Exception as e:
                print(f"Error registering user {user_id}: {e}")
    
    def _generate_health_report(self, user_id):
        """Internal method to trigger health report generation"""
        if not self.crew:
            print(f"❌ Crew not set, cannot generate report for user {user_id}")
            return
        
        try:
            print(f"🔄 Generating automated health report for user {user_id}")
            
            # Create a query that triggers your existing medical_report_automation task
            automated_query = f"Generate automated 3-month health report for user {user_id}"
            
            # Use your existing crew kickoff
            result = self.crew.kickoff(inputs={'query': automated_query})
            
            # Update the schedule for next report
            self._schedule_next_report(user_id)
            
            print(f"✅ Health report completed for user {user_id}")
            return result
            
        except Exception as e:
            print(f"❌ Error generating health report for user {user_id}: {e}")
            # Still schedule next report even if this one failed
            self._schedule_next_report(user_id)
    
    def _schedule_next_report(self, user_id):
        """Schedule the next report for this user"""
        try:
            now = datetime.now()
            next_report = now + timedelta(days=90)  # Next 3 months
            
            # Update user schedule
            if user_id in self.users:
                self.users[user_id]['last_report_date'] = now.isoformat()
                self.users[user_id]['next_report_date'] = next_report.isoformat()
                self.save_user_schedules()
            
            # Schedule next report
            self.scheduler.add_job(
                func=self._generate_health_report,
                trigger='date',
                run_date=next_report,
                args=[user_id],
                id=f'health_report_{user_id}',
                replace_existing=True
            )
            print(f"📅 Next health report for user {user_id} scheduled for {next_report.strftime('%Y-%m-%d')}")
        except Exception as e:
            print(f"Error scheduling next report for user {user_id}: {e}")
    
    def start(self):
        """Start the scheduler and reload existing schedules"""
        try:
            self._reload_existing_schedules()
            self.scheduler.start()
            print("🚀 Health report scheduler started")
        except Exception as e:
            print(f"Error starting scheduler: {e}")
    
    def _reload_existing_schedules(self):
        """Reload schedules for existing users on startup"""
        try:
            now = datetime.now()
            for user_id, schedule in self.users.items():
                next_report_date = datetime.fromisoformat(schedule['next_report_date'])
                
                if next_report_date > now:
                    # Schedule is still in the future
                    self.scheduler.add_job(
                        func=self._generate_health_report,
                        trigger='date',
                        run_date=next_report_date,
                        args=[user_id],
                        id=f'health_report_{user_id}',
                        replace_existing=True
                    )
                    print(f"📋 Reloaded schedule for user {user_id}")
                else:
                    # Schedule is overdue, trigger soon
                    self.scheduler.add_job(
                        func=self._generate_health_report,
                        trigger='date',
                        run_date=now + timedelta(seconds=10),
                        args=[user_id],
                        id=f'health_report_{user_id}',
                        replace_existing=True
                    )
                    print(f"⚠️  Overdue report for user {user_id} will be generated in 10 seconds")
        except Exception as e:
            print(f"Error reloading schedules: {e}")
    
    def stop(self):
        """Stop the scheduler"""
        try:
            self.scheduler.shutdown(wait=False)
            print("🛑 Health report scheduler stopped")
        except Exception as e:
            print(f"Error stopping scheduler: {e}")

# main.py - Your main file with minimal changes
from crewai import Crew
from agents import Ruby, drwarren, advik, carla, rachel, neel  # Import your agents
from tasks import project_task, medical_research, medical_report_automation, collaboration_by_warren  # Import your tasks
from scheduler import SimpleHealthScheduler  # Import the new scheduler

def main():
    # Initialize scheduler first
    scheduler = SimpleHealthScheduler()
    
    try:
        # Your existing crew setup - NO CHANGES
        crew = Crew(
            agents=[Ruby, drwarren, advik, carla, rachel, neel],
            tasks=[project_task, medical_research, medical_report_automation, collaboration_by_warren],
            verbose=True
        )
        
        # Connect scheduler to crew
        scheduler.set_crew(crew)
        scheduler.start()
        
        print("🏥 Health monitoring system is ready!")
        print("💡 Tip: Each new user will automatically get scheduled for 3-month health reports")
        
        # Your main loop
        while True:
            print("\n" + "="*50)
            user_id = input("Enter user ID: ").strip()
            if not user_id:
                print("Please enter a valid user ID")
                continue
                
            query = input("Enter your query: ").strip()
            if not query:
                print("Please enter a valid query")
                continue
            
            # Register user if new (ONLY NEW LINE)
            scheduler.register_user(user_id)
            
            # Your existing query processing - NO CHANGES
            print(f"\n🔄 Processing query for user {user_id}...")
            result = crew.kickoff(inputs={'query': query})
            print(f"\n✅ Response:\n{result}")
            
    except KeyboardInterrupt:
        print("\n🔄 Shutting down system...")
        scheduler.stop()
        print("👋 System stopped gracefully")
    except Exception as e:
        print(f"❌ System error: {e}")
        scheduler.stop()

if __name__ == "__main__":
    main()

# requirements.txt - Add this to your project
# """
# apscheduler==3.10.4
# crewai
# # ... your other existing dependencies
# """

# Installation command:
# pip install apscheduler

# File structure after implementation:
# """
# your_project/
# ├── agents.py          # Your existing agents file
# ├── tasks.py           # Your existing tasks file  
# ├── tools.py           # Your existing tools file
# ├── scheduler.py       # New file (from above)
# ├── main.py            # Your main file (modified)
# ├── user_schedules.json # Auto-created for storing schedules
# └── requirements.txt   # Add apscheduler
# """

# Example of how your existing files should import in main.py:
# """
# # agents.py should have:
# Ruby = Agent(...)
# drwarren = Agent(...)
# advik = Agent(...)
# carla = Agent(...)
# rachel = Agent(...)
# neel = Agent(...)

# # tasks.py should have:
# project_task = Task(...)
# medical_research = Task(...)
# medical_report_automation = Task(...)
# collaboration_by_warren = Task(...)

# # tools.py should have:
# past_search_data_tool = Tool(...)
# general_search_tool = Tool(...)
# research_paper_reader_tool = Tool(...)
# # ... etc
# """