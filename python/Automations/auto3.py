import json
import os
import re
from datetime import datetime, timedelta
from pathlib import Path
import logging
import random
from typing import Dict, List, Optional

class EmailTemplateManager:
    def __init__(self):
        self.templates_file = Path('email_templates.json')
        self.sent_emails_file = Path('sent_emails.json')
        self.contacts_file = Path('contacts.json')
        
        # Default email templates
        self.default_templates = {
            'business_intro': {
                'subject': 'Introduction - {company_name}',
                'body': """Dear {recipient_name},

I hope this email finds you well. My name is {sender_name} and I'm reaching out from {company_name}.

{intro_message}

I would love to connect and discuss how we might collaborate or share insights in our respective fields.

Looking forward to hearing from you.

Best regards,
{sender_name}
{company_name}
{contact_info}""",
                'variables': ['recipient_name', 'sender_name', 'company_name', 'intro_message', 'contact_info'],
                'category': 'business'
            },
            'follow_up': {
                'subject': 'Following up - {topic}',
                'body': """Hi {recipient_name},

I hope you're doing well. I wanted to follow up on our previous conversation about {topic}.

{follow_up_message}

Please let me know if you have any questions or if there's anything else I can help you with.

Best regards,
{sender_name}""",
                'variables': ['recipient_name', 'sender_name', 'topic', 'follow_up_message'],
                'category': 'follow_up'
            },
            'thank_you': {
                'subject': 'Thank you for {reason}',
                'body': """Dear {recipient_name},

I wanted to take a moment to express my sincere gratitude for {reason}.

{thank_you_message}

Your {gesture_type} means a lot to me and I truly appreciate it.

Thank you again.

Best regards,
{sender_name}""",
                'variables': ['recipient_name', 'sender_name', 'reason', 'thank_you_message', 'gesture_type'],
                'category': 'gratitude'
            },
            'meeting_request': {
                'subject': 'Meeting Request - {purpose}',
                'body': """Hi {recipient_name},

I hope this email finds you well. I would like to schedule a meeting to discuss {purpose}.

{meeting_details}

Please let me know what times work best for you, and I'll be happy to accommodate your schedule.

Looking forward to our conversation.

Best regards,
{sender_name}
{company_name}""",
                'variables': ['recipient_name', 'sender_name', 'company_name', 'purpose', 'meeting_details'],
                'category': 'meeting'
            },
            'marketing_promo': {
                'subject': 'Special Offer: {offer_title}',
                'body': """Dear {recipient_name},

I hope you're having a great day! I wanted to share an exciting opportunity with you.

{offer_description}

{call_to_action}

This offer is available until {expiry_date}.

Best regards,
{sender_name}
{company_name}""",
                'variables': ['recipient_name', 'sender_name', 'company_name', 'offer_title', 'offer_description', 'call_to_action', 'expiry_date'],
                'category': 'marketing'
            }
        }
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('email_manager.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Load data
        self.templates = self.load_templates()
        self.contacts = self.load_contacts()
        self.sent_emails = self.load_sent_emails()
    
    def load_templates(self) -> Dict:
        """Load templates from file or create default ones"""
        if self.templates_file.exists():
            try:
                with open(self.templates_file, 'r') as f:
                    return json.load(f)
            except:
                return self.default_templates.copy()
        return self.default_templates.copy()
    
    def save_templates(self):
        """Save templates to file"""
        with open(self.templates_file, 'w') as f:
            json.dump(self.templates, f, indent=2)
    
    def load_contacts(self) -> Dict:
        """Load contacts from file"""
        if self.contacts_file.exists():
            try:
                with open(self.contacts_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_contacts(self):
        """Save contacts to file"""
        with open(self.contacts_file, 'w') as f:
            json.dump(self.contacts, f, indent=2)
    
    def load_sent_emails(self) -> List:
        """Load sent emails history"""
        if self.sent_emails_file.exists():
            try:
                with open(self.sent_emails_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_sent_emails(self):
        """Save sent emails history"""
        with open(self.sent_emails_file, 'w') as f:
            json.dump(self.sent_emails, f, indent=2)
    
    def create_template(self, name: str, subject: str, body: str, category: str = 'custom'):
        """Create a new email template"""
        # Extract variables from template
        variables = re.findall(r'\{(\w+)\}', body + ' ' + subject)
        variables = list(set(variables))  # Remove duplicates
        
        template = {
            'subject': subject,
            'body': body,
            'variables': variables,
            'category': category,
            'created_at': datetime.now().isoformat()
        }
        
        self.templates[name] = template
        self.save_templates()
        self.logger.info(f"Created template: {name}")
        return template
    
    def get_template(self, name: str) -> Optional[Dict]:
        """Get a specific template by name"""
        return self.templates.get(name)
    
    def list_templates(self, category: str = None) -> List[str]:
        """List all templates or templates by category"""
        if category:
            return [name for name, template in self.templates.items() 
                   if template.get('category') == category]
        return list(self.templates.keys())
    
    def delete_template(self, name: str) -> bool:
        """Delete a template"""
        if name in self.templates:
            del self.templates[name]
            self.save_templates()
            self.logger.info(f"Deleted template: {name}")
            return True
        return False
    
    def add_contact(self, name: str, email: str, company: str = '', notes: str = ''):
        """Add a new contact"""
        self.contacts[name] = {
            'email': email,
            'company': company,
            'notes': notes,
            'added_at': datetime.now().isoformat()
        }
        self.save_contacts()
        self.logger.info(f"Added contact: {name}")
    
    def get_contact(self, name: str) -> Optional[Dict]:
        """Get contact information"""
        return self.contacts.get(name)
    
    def list_contacts(self) -> List[str]:
        """List all contacts"""
        return list(self.contacts.keys())
    
    def generate_email(self, template_name: str, variables: Dict[str, str]) -> Dict:
        """Generate an email using a template and variables"""
        template = self.get_template(template_name)
        if not template:
            raise ValueError(f"Template '{template_name}' not found")
        
        subject = template['subject']
        body = template['body']
        
        # Replace variables in subject and body
        for var, value in variables.items():
            subject = subject.replace(f'{{{var}}}', str(value))
            body = body.replace(f'{{{var}}}', str(value))
        
        return {
            'template_name': template_name,
            'subject': subject,
            'body': body,
            'variables': variables,
            'generated_at': datetime.now().isoformat()
        }
    
    def record_sent_email(self, email_data: Dict, recipient: str):
        """Record a sent email"""
        sent_email = {
            'template_name': email_data['template_name'],
            'subject': email_data['subject'],
            'recipient': recipient,
            'sent_at': datetime.now().isoformat(),
            'variables': email_data.get('variables', {})
        }
        self.sent_emails.append(sent_email)
        self.save_sent_emails()
        self.logger.info(f"Recorded sent email to: {recipient}")
    
    def get_email_statistics(self) -> Dict:
        """Get statistics about sent emails"""
        if not self.sent_emails:
            return {'total_sent': 0, 'templates_used': {}, 'recent_activity': []}
        
        # Template usage statistics
        template_usage = {}
        for email in self.sent_emails:
            template = email['template_name']
            template_usage[template] = template_usage.get(template, 0) + 1
        
        # Recent activity (last 10 emails)
        recent_activity = sorted(self.sent_emails, 
                               key=lambda x: x['sent_at'], 
                               reverse=True)[:10]
        
        return {
            'total_sent': len(self.sent_emails),
            'templates_used': template_usage,
            'recent_activity': recent_activity
        }
    
    def suggest_templates(self, purpose: str) -> List[str]:
        """Suggest templates based on purpose"""
        purpose_lower = purpose.lower()
        suggestions = []
        
        purpose_keywords = {
            'introduction': ['business_intro'],
            'follow': ['follow_up'],
            'thank': ['thank_you'],
            'meeting': ['meeting_request'],
            'promotion': ['marketing_promo'],
            'marketing': ['marketing_promo'],
            'offer': ['marketing_promo']
        }
        
        for keyword, templates in purpose_keywords.items():
            if keyword in purpose_lower:
                suggestions.extend(templates)
        
        # Add custom templates
        custom_templates = [name for name, template in self.templates.items() 
                          if template.get('category') == 'custom']
        suggestions.extend(custom_templates)
        
        return list(set(suggestions))  # Remove duplicates
    
    def validate_email(self, email: str) -> bool:
        """Basic email validation"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def generate_report(self) -> str:
        """Generate a comprehensive report"""
        stats = self.get_email_statistics()
        
        report = []
        report.append("=" * 60)
        report.append("EMAIL TEMPLATE MANAGER REPORT")
        report.append("=" * 60)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Template statistics
        report.append(f"Total templates: {len(self.templates)}")
        report.append(f"Total contacts: {len(self.contacts)}")
        report.append(f"Total emails sent: {stats['total_sent']}")
        
        # Template categories
        categories = {}
        for template in self.templates.values():
            cat = template.get('category', 'uncategorized')
            categories[cat] = categories.get(cat, 0) + 1
        
        report.append("")
        report.append("Template Categories:")
        for cat, count in categories.items():
            report.append(f"  {cat.title()}: {count} templates")
        
        # Most used templates
        if stats['templates_used']:
            report.append("")
            report.append("Most Used Templates:")
            sorted_templates = sorted(stats['templates_used'].items(), 
                                    key=lambda x: x[1], reverse=True)
            for template, count in sorted_templates[:5]:
                report.append(f"  {template}: {count} times")
        
        # Recent activity
        if stats['recent_activity']:
            report.append("")
            report.append("Recent Activity:")
            for email in stats['recent_activity'][:5]:
                sent_date = datetime.fromisoformat(email['sent_at']).strftime('%Y-%m-%d %H:%M')
                report.append(f"  {sent_date} - {email['subject'][:40]}... to {email['recipient']}")
        
        report.append("=" * 60)
        return "\n".join(report)

def main():
    """Main function to run the email template manager"""
    print("📧 Email Template Generator & Manager")
    print("=" * 45)
    
    manager = EmailTemplateManager()
    
    while True:
        print("\n🎯 Choose an option:")
        print("1. Create new template")
        print("2. Generate email from template")
        print("3. Manage contacts")
        print("4. View templates")
        print("5. Get template suggestions")
        print("6. View email statistics")
        print("7. Generate report")
        print("8. Exit")
        
        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == '1':
            print("\n📝 Creating new email template")
            name = input("Template name: ").strip()
            if not name:
                print("❌ Template name is required!")
                continue
            
            subject = input("Email subject (use {variable} for placeholders): ").strip()
            if not subject:
                print("❌ Subject is required!")
                continue
            
            print("\nEmail body (use {variable} for placeholders):")
            print("(Type 'END' on a new line when finished)")
            body_lines = []
            while True:
                line = input()
                if line.strip().upper() == 'END':
                    break
                body_lines.append(line)
            
            body = '\n'.join(body_lines)
            if not body:
                print("❌ Body is required!")
                continue
            
            category = input("Category (business, marketing, custom, etc.): ").strip() or 'custom'
            
            try:
                template = manager.create_template(name, subject, body, category)
                print(f"✅ Template '{name}' created successfully!")
                print(f"Variables detected: {', '.join(template['variables'])}")
            except Exception as e:
                print(f"❌ Error creating template: {e}")
        
        elif choice == '2':
            templates = manager.list_templates()
            if not templates:
                print("❌ No templates available!")
                continue
            
            print("\n📝 Available templates:")
            for i, template_name in enumerate(templates, 1):
                template = manager.get_template(template_name)
                print(f"{i}. {template_name} ({template.get('category', 'custom')})")
            
            template_choice = input("\nChoose template number: ").strip()
            if not template_choice.isdigit() or not (1 <= int(template_choice) <= len(templates)):
                print("❌ Invalid choice!")
                continue
            
            template_name = templates[int(template_choice) - 1]
            template = manager.get_template(template_name)
            
            print(f"\n📧 Generating email from '{template_name}'")
            print(f"Variables needed: {', '.join(template['variables'])}")
            
            # Collect variables
            variables = {}
            for var in template['variables']:
                value = input(f"Enter value for {var}: ").strip()
                variables[var] = value
            
            try:
                email = manager.generate_email(template_name, variables)
                print(f"\n✨ Generated Email:")
                print(f"Subject: {email['subject']}")
                print(f"Body:\n{email['body']}")
                
                # Simulate sending
                recipient = input("\nEnter recipient email: ").strip()
                if recipient and manager.validate_email(recipient):
                    manager.record_sent_email(email, recipient)
                    print("✅ Email recorded as sent!")
                else:
                    print("❌ Invalid email address!")
                    
            except Exception as e:
                print(f"❌ Error generating email: {e}")
        
        elif choice == '3':
            print("\n👥 Contact Management")
            print("1. Add new contact")
            print("2. View contacts")
            print("3. Back to main menu")
            
            contact_choice = input("Choose option: ").strip()
            
            if contact_choice == '1':
                name = input("Contact name: ").strip()
                email = input("Email address: ").strip()
                company = input("Company (optional): ").strip()
                notes = input("Notes (optional): ").strip()
                
                if name and email and manager.validate_email(email):
                    manager.add_contact(name, email, company, notes)
                    print("✅ Contact added successfully!")
                else:
                    print("❌ Invalid input or email address!")
            
            elif contact_choice == '2':
                contacts = manager.list_contacts()
                if not contacts:
                    print("❌ No contacts found!")
                    continue
                
                print(f"\n📋 Contacts ({len(contacts)}):")
                for i, name in enumerate(contacts, 1):
                    contact = manager.get_contact(name)
                    print(f"{i}. {name} - {contact['email']}")
                    if contact['company']:
                        print(f"   Company: {contact['company']}")
                    if contact['notes']:
                        print(f"   Notes: {contact['notes']}")
                    print()
        
        elif choice == '4':
            templates = manager.list_templates()
            if not templates:
                print("❌ No templates available!")
                continue
            
            print(f"\n📝 Templates ({len(templates)}):")
            for i, template_name in enumerate(templates, 1):
                template = manager.get_template(template_name)
                print(f"{i}. {template_name}")
                print(f"   Category: {template.get('category', 'custom')}")
                print(f"   Variables: {', '.join(template['variables'])}")
                print(f"   Subject: {template['subject']}")
                print()
            
            # Option to delete template
            delete_choice = input("Enter template number to delete (or press Enter to skip): ").strip()
            if delete_choice.isdigit() and 1 <= int(delete_choice) <= len(templates):
                template_name = templates[int(delete_choice) - 1]
                confirm = input(f"Are you sure you want to delete '{template_name}'? (y/n): ").lower().strip()
                if confirm == 'y':
                    if manager.delete_template(template_name):
                        print("✅ Template deleted!")
                    else:
                        print("❌ Template not found!")
        
        elif choice == '5':
            purpose = input("What type of email do you want to send? ").strip()
            if not purpose:
                print("❌ Please describe the purpose!")
                continue
            
            suggestions = manager.suggest_templates(purpose)
            if not suggestions:
                print("❌ No templates match your purpose. Try creating a custom template!")
                continue
            
            print(f"\n💡 Suggested templates for '{purpose}':")
            for i, template_name in enumerate(suggestions, 1):
                template = manager.get_template(template_name)
                print(f"{i}. {template_name} ({template.get('category', 'custom')})")
                print(f"   Subject: {template['subject']}")
        
        elif choice == '6':
            stats = manager.get_email_statistics()
            print(f"\n📊 Email Statistics:")
            print(f"Total emails sent: {stats['total_sent']}")
            
            if stats['templates_used']:
                print("\nTemplate Usage:")
                for template, count in stats['templates_used'].items():
                    print(f"  {template}: {count} times")
            
            if stats['recent_activity']:
                print("\nRecent Activity:")
                for email in stats['recent_activity'][:5]:
                    sent_date = datetime.fromisoformat(email['sent_at']).strftime('%Y-%m-%d %H:%M')
                    print(f"  {sent_date} - {email['subject'][:40]}...")
        
        elif choice == '7':
            print("\n" + manager.generate_report())
        
        elif choice == '8':
            print("👋 Thanks for using Email Template Manager!")
            break
        
        else:
            print("❌ Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
