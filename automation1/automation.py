import threading
import time
import schedule
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json
import os

class AutomationManager:
    def __init__(self):
        self.reminders = []
        self.automation_running = False
        self.automation_thread = None
        self.data_file = "automation_data.json"
        self.load_automation_data()
        self.setup_scheduled_tasks()
    
    def load_automation_data(self):
        """Load automation data from file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.reminders = [
                        {
                            **reminder,
                            'due_date': datetime.fromisoformat(reminder['due_date']),
                            'created_date': datetime.fromisoformat(reminder['created_date'])
                        }
                        for reminder in data.get('reminders', [])
                    ]
            else:
                self.create_initial_reminders()
        except Exception as e:
            print(f"Error loading automation data: {e}")
            self.create_initial_reminders()
    
    def save_automation_data(self):
        """Save automation data to file"""
        try:
            data = {
                'reminders': [
                    {
                        **reminder,
                        'due_date': reminder['due_date'].isoformat(),
                        'created_date': reminder['created_date'].isoformat()
                    }
                    for reminder in self.reminders
                ]
            }
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving automation data: {e}")
    
    def create_initial_reminders(self):
        """Create initial set of reminders"""
        now = datetime.now()
        
        initial_reminders = [
            {
                'id': 'med_morning',
                'type': 'Medication',
                'message': 'Take your morning medications',
                'due_date': now.replace(hour=8, minute=0, second=0, microsecond=0) + timedelta(days=1),
                'recurring': True,
                'frequency': 'daily',
                'urgent': True,
                'completed': False,
                'created_date': now
            },
            {
                'id': 'weekly_report',
                'type': 'Health Report',
                'message': 'Weekly health progress report is ready for review',
                'due_date': now + timedelta(days=7),
                'recurring': True,
                'frequency': 'weekly',
                'urgent': False,
                'completed': False,
                'created_date': now
            },
            {
                'id': 'exercise_reminder',
                'type': 'Exercise',
                'message': 'Time for your scheduled workout session',
                'due_date': now.replace(hour=17, minute=0, second=0, microsecond=0) + timedelta(days=1),
                'recurring': True,
                'frequency': 'daily',
                'urgent': False,
                'completed': False,
                'created_date': now
            },
            {
                'id': 'hydration_check',
                'type': 'Hydration',
                'message': 'Remember to drink water - stay hydrated!',
                'due_date': now + timedelta(hours=2),
                'recurring': True,
                'frequency': 'hourly',
                'urgent': False,
                'completed': False,
                'created_date': now
            },
            {
                'id': 'monthly_checkup',
                'type': 'Medical Checkup',
                'message': 'Schedule your monthly health checkup',
                'due_date': now + timedelta(days=30),
                'recurring': True,
                'frequency': 'monthly',
                'urgent': False,
                'completed': False,
                'created_date': now
            }
        ]
        
        self.reminders = initial_reminders
        self.save_automation_data()
    
    def setup_scheduled_tasks(self):
        """Setup scheduled automation tasks"""
        # Daily tasks
        schedule.every().day.at("08:00").do(self.trigger_daily_medication_reminder)
        schedule.every().day.at("17:00").do(self.trigger_exercise_reminder)
        schedule.every().day.at("22:00").do(self.trigger_sleep_reminder)
        
        # Weekly tasks
        schedule.every().monday.at("09:00").do(self.trigger_weekly_report)
        
        # Monthly tasks
        schedule.every(30).days.do(self.trigger_monthly_checkup)
        
        # Hydration reminders every 2 hours during awake time
        for hour in range(8, 22, 2):
            schedule.every().day.at(f"{hour:02d}:00").do(self.trigger_hydration_reminder)
    
    def start_automation(self):
        """Start the automation background process"""
        if not self.automation_running:
            self.automation_running = True
            self.automation_thread = threading.Thread(target=self._automation_loop, daemon=True)
            self.automation_thread.start()
            print("Automation system started")
    
    def stop_automation(self):
        """Stop the automation background process"""
        self.automation_running = False
        if self.automation_thread:
            self.automation_thread.join()
        print("Automation system stopped")
    
    def _automation_loop(self):
        """Main automation loop running in background"""
        while self.automation_running:
            try:
                # Run scheduled tasks
                schedule.run_pending()
                
                # Check for due reminders
                self.check_due_reminders()
                
                # Clean up old completed reminders
                self.cleanup_old_reminders()
                
                # Save data periodically
                self.save_automation_data()
                
                time.sleep(60)  # Check every minute
                
            except Exception as e:
                print(f"Error in automation loop: {e}")
                time.sleep(60)
    
    def check_due_reminders(self):
        """Check for reminders that are due"""
        now = datetime.now()
        for reminder in self.reminders:
            if not reminder['completed'] and reminder['due_date'] <= now:
                self.trigger_reminder(reminder)
    
    def trigger_reminder(self, reminder: Dict):
        """Trigger a specific reminder"""
        print(f"Reminder triggered: {reminder['message']}")
        
        # Mark as triggered and schedule next occurrence if recurring
        if reminder['recurring']:
            self.schedule_next_occurrence(reminder)
        else:
            reminder['completed'] = True
    
    def schedule_next_occurrence(self, reminder: Dict):
        """Schedule the next occurrence of a recurring reminder"""
        frequency = reminder['frequency']
        current_due = reminder['due_date']
        
        if frequency == 'daily':
            next_due = current_due + timedelta(days=1)
        elif frequency == 'weekly':
            next_due = current_due + timedelta(weeks=1)
        elif frequency == 'monthly':
            next_due = current_due + timedelta(days=30)
        elif frequency == 'hourly':
            next_due = current_due + timedelta(hours=2)  # Every 2 hours for hydration
        else:
            next_due = current_due + timedelta(days=1)
        
        reminder['due_date'] = next_due
        reminder['completed'] = False
    
    def setup_scheduled_tasks(self):
    # "Setup scheduled automation tasks"
    # Existing tasks...
    
    # Agent-specific automated tasks
    # Dr Warren: 3-month report generation
        schedule.every(90).days.do(self.trigger_warren_quarterly_report)
        
        # Carla: Diet plan updates every 2 weeks  
        schedule.every(14).days.do(self.trigger_carla_diet_update)
        
        # Rachel: Exercise program updates every 2 weeks
        schedule.every(14).days.do(self.trigger_rachel_exercise_update)
        
        # Advik: Weekly performance analysis
        schedule.every().week.do(self.trigger_advik_performance_analysis)
        
        # Ruby: Weekly progress reports
        schedule.every().monday.at("09:00").do(self.trigger_ruby_weekly_report)


    def cleanup_old_reminders(self):
        """Remove old completed reminders"""
        cutoff_date = datetime.now() - timedelta(days=7)
        self.reminders = [
            reminder for reminder in self.reminders
            if not (reminder['completed'] and reminder['due_date'] < cutoff_date)
        ]
    
    def get_current_reminders(self) -> List[Dict]:
        """Get current active reminders"""
        now = datetime.now()
        upcoming_cutoff = now + timedelta(days=1)
        
        current_reminders = [
            reminder for reminder in self.reminders
            if not reminder['completed'] and reminder['due_date'] <= upcoming_cutoff
        ]
        
        # Sort by due date
        current_reminders.sort(key=lambda x: x['due_date'])
        return current_reminders
    
    def add_reminder(self, reminder_type: str, message: str, due_date: datetime, 
                    recurring: bool = False, frequency: str = 'daily', urgent: bool = False):
        """Add a new reminder"""
        reminder = {
            'id': f"{reminder_type.lower()}_{datetime.now().timestamp()}",
            'type': reminder_type,
            'message': message,
            'due_date': due_date,
            'recurring': recurring,
            'frequency': frequency,
            'urgent': urgent,
            'completed': False,
            'created_date': datetime.now()
        }
        
        self.reminders.append(reminder)
        self.save_automation_data()
        return reminder['id']
    
    def complete_reminder(self, reminder_id: str):
        """Mark a reminder as completed"""
        for reminder in self.reminders:
            if reminder['id'] == reminder_id:
                reminder['completed'] = True
                if reminder['recurring']:
                    self.schedule_next_occurrence(reminder)
                self.save_automation_data()
                return True
        return False
    
    def schedule_follow_up(self, event_type: str):
        """Schedule follow-up reminders based on events"""
        now = datetime.now()
        
        follow_ups = {
            'report_generated': {
                'type': 'Follow-up',
                'message': 'Review your health report and discuss with your care team',
                'due_date': now + timedelta(days=2),
                'urgent': False
            },
            'medication_check': {
                'type': 'Medication',
                'message': 'Medication adherence check - confirm you\'re taking medications as prescribed',
                'due_date': now + timedelta(days=7),
                'urgent': True
            },
            'exercise_plan_update': {
                'type': 'Exercise',
                'message': 'Exercise plan updated - review new routines',
                'due_date': now + timedelta(hours=24),
                'urgent': False
            }
        }
        
        if event_type in follow_ups:
            follow_up = follow_ups[event_type]
            self.add_reminder(
                follow_up['type'],
                follow_up['message'],
                follow_up['due_date'],
                urgent=follow_up['urgent']
            )
    
    # Scheduled task methods
    def trigger_daily_medication_reminder(self):
        """Trigger daily medication reminder"""
        self.add_reminder(
            'Medication',
            'Time to take your prescribed medications',
            datetime.now() + timedelta(minutes=5),
            urgent=True
        )
    
    def trigger_exercise_reminder(self):
        """Trigger exercise reminder"""
        self.add_reminder(
            'Exercise',
            'Scheduled workout time - check your exercise plan',
            datetime.now() + timedelta(minutes=10),
            urgent=False
        )
    
    def trigger_sleep_reminder(self):
        """Trigger sleep preparation reminder"""
        self.add_reminder(
            'Sleep',
            'Wind down time - prepare for optimal sleep',
            datetime.now() + timedelta(minutes=15),
            urgent=False
        )
    
    def trigger_weekly_report(self):
        """Trigger weekly health report generation"""
        self.add_reminder(
            'Health Report',
            'Your weekly health progress report is being prepared',
            datetime.now() + timedelta(hours=1),
            urgent=False
        )
    
    def trigger_monthly_checkup(self):
        """Trigger monthly health checkup reminder"""
        self.add_reminder(
            'Medical Checkup',
            'Time to schedule your monthly health assessment',
            datetime.now() + timedelta(days=1),
            urgent=True
        )
    
    def trigger_hydration_reminder(self):
        """Trigger hydration reminder"""
        self.add_reminder(
            'Hydration',
            'Hydration check - remember to drink water',
            datetime.now() + timedelta(minutes=5),
            urgent=False
        )
    
    def get_automation_status(self) -> Dict:
        """Get current automation system status"""
        return {
            'running': self.automation_running,
            'total_reminders': len(self.reminders),
            'active_reminders': len([r for r in self.reminders if not r['completed']]),
            'due_now': len([
                r for r in self.reminders 
                if not r['completed'] and r['due_date'] <= datetime.now()
            ])
        }
    
    def trigger_warren_quarterly_report(self):
    # """Trigger Warren's quarterly medical report"""
        self.add_reminder(
            'Medical Report',
            'Dr Warren is generating your quarterly health report',
            datetime.now() + timedelta(minutes=30),
            urgent=False
        )
        # Trigger the actual agent task
        from crew_manager import DefaultHealthCrewManager
        response = DefaultHealthCrewManager.trigger_automation_task('quarterly_medical_report')
        return response

    def trigger_carla_diet_update(self):
            # """Trigger Carla's diet plan update"""
        self.add_reminder(
            'Nutrition Update',
            'Dr Carla is updating your nutrition plan based on recent progress',
            datetime.now() + timedelta(minutes=15),
            urgent=False
    )

    def trigger_rachel_exercise_update(self):
        """Trigger Rachel's exercise program update"""
        self.add_reminder(
            'Exercise Update', 
            'Rachel is updating your exercise program for the next 2 weeks',
            datetime.now() + timedelta(minutes=20),
            urgent=False
        )

    def trigger_advik_performance_analysis(self):
        """Trigger Advik's weekly performance analysis"""
        self.add_reminder(
            'Performance Analysis',
            'Dr Advik is analyzing your weekly performance data',
            datetime.now() + timedelta(minutes=25),
            urgent=False
        )

    def trigger_ruby_weekly_report(self):
        """Trigger Ruby's weekly progress report"""
        self.add_reminder(
            'Progress Report',
            'Ruby is compiling your weekly progress report',
            datetime.now() + timedelta(minutes=10),
            urgent=False
        )