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
    
    def duplicate_template(self, original_name: str, new_name: str) -> Optional[Dict]:
        """Duplicate an existing template with a new name"""
        original_template = self.get_template(original_name)
        if not original_template:
            return None
        
        # Create a copy of the template
        new_template = original_template.copy()
        new_template['duplicated_from'] = original_name
        new_template['created_at'] = datetime.now().isoformat()
        new_template['version'] = 1
        
        # Add version to original template if not present
        if 'version' not in original_template:
            original_template['version'] = 1
            self.save_templates()
        
        self.templates[new_name] = new_template
        self.save_templates()
        self.logger.info(f"Duplicated template '{original_name}' to '{new_name}'")
        return new_template
    
    def get_template_versions(self, base_name: str) -> List[Dict]:
        """Get all versions of a template"""
        versions = []
        for name, template in self.templates.items():
            if name == base_name or template.get('duplicated_from') == base_name:
                versions.append({
                    'name': name,
                    'version': template.get('version', 1),
                    'created_at': template.get('created_at'),
                    'is_original': name == base_name
                })
        
        return sorted(versions, key=lambda x: x['version'])
    
    def update_template_version(self, name: str) -> bool:
        """Increment version number of a template"""
        if name in self.templates:
            current_version = self.templates[name].get('version', 1)
            self.templates[name]['version'] = current_version + 1
            self.templates[name]['last_updated'] = datetime.now().isoformat()
            self.save_templates()
            self.logger.info(f"Updated version of template '{name}' to {current_version + 1}")
            return True
        return False
    
    def export_templates(self, filename: str = None, include_contacts: bool = False) -> str:
        """Export templates to a JSON file"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'email_templates_backup_{timestamp}.json'
        
        export_data = {
            'export_info': {
                'exported_at': datetime.now().isoformat(),
                'total_templates': len(self.templates),
                'version': '1.0'
            },
            'templates': self.templates
        }
        
        if include_contacts:
            export_data['contacts'] = self.contacts
            export_data['export_info']['total_contacts'] = len(self.contacts)
        
        try:
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2)
            self.logger.info(f"Exported {len(self.templates)} templates to {filename}")
            return filename
        except Exception as e:
            self.logger.error(f"Failed to export templates: {e}")
            raise
    
    def import_templates(self, filename: str, overwrite: bool = False) -> Dict:
        """Import templates from a JSON file"""
        try:
            with open(filename, 'r') as f:
                import_data = json.load(f)
            
            imported_count = 0
            skipped_count = 0
            overwritten_count = 0
            
            if 'templates' not in import_data:
                raise ValueError("Invalid backup file: no templates found")
            
            for template_name, template_data in import_data['templates'].items():
                if template_name in self.templates and not overwrite:
                    skipped_count += 1
                    continue
                
                if template_name in self.templates and overwrite:
                    overwritten_count += 1
                
                self.templates[template_name] = template_data
                imported_count += 1
            
            # Import contacts if available
            if 'contacts' in import_data and import_data['contacts']:
                for contact_name, contact_data in import_data['contacts'].items():
                    if contact_name not in self.contacts or overwrite:
                        self.contacts[contact_name] = contact_data
            
            self.save_templates()
            self.save_contacts()
            
            self.logger.info(f"Imported {imported_count} templates, skipped {skipped_count}, overwritten {overwritten_count}")
            
            return {
                'imported': imported_count,
                'skipped': skipped_count,
                'overwritten': overwritten_count,
                'export_info': import_data.get('export_info', {})
            }
            
        except Exception as e:
            self.logger.error(f"Failed to import templates: {e}")
            raise
    
    def create_backup(self) -> str:
        """Create a complete backup of all data"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir = Path('backups')
        backup_dir.mkdir(exist_ok=True)
        
        backup_data = {
            'backup_info': {
                'created_at': datetime.now().isoformat(),
                'total_templates': len(self.templates),
                'total_contacts': len(self.contacts),
                'total_sent_emails': len(self.sent_emails)
            },
            'templates': self.templates,
            'contacts': self.contacts,
            'sent_emails': self.sent_emails
        }
        
        backup_file = backup_dir / f'complete_backup_{timestamp}.json'
        
        try:
            with open(backup_file, 'w') as f:
                json.dump(backup_data, f, indent=2)
            self.logger.info(f"Created complete backup: {backup_file}")
            return str(backup_file)
        except Exception as e:
            self.logger.error(f"Failed to create backup: {e}")
            raise
    
    def restore_from_backup(self, backup_file: str) -> bool:
        """Restore all data from a backup file"""
        try:
            with open(backup_file, 'r') as f:
                backup_data = json.load(f)
            
            if 'templates' in backup_data:
                self.templates = backup_data['templates']
                self.save_templates()
            
            if 'contacts' in backup_data:
                self.contacts = backup_data['contacts']
                self.save_contacts()
            
            if 'sent_emails' in backup_data:
                self.sent_emails = backup_data['sent_emails']
                self.save_sent_emails()
            
            self.logger.info(f"Restored from backup: {backup_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to restore from backup: {e}")
            return False
    
    def list_backups(self) -> List[Dict]:
        """List all available backup files"""
        backup_dir = Path('backups')
        if not backup_dir.exists():
            return []
        
        backups = []
        for backup_file in backup_dir.glob('complete_backup_*.json'):
            try:
                with open(backup_file, 'r') as f:
                    backup_data = json.load(f)
                
                backup_info = backup_data.get('backup_info', {})
                backups.append({
                    'filename': backup_file.name,
                    'path': str(backup_file),
                    'created_at': backup_info.get('created_at'),
                    'total_templates': backup_info.get('total_templates', 0),
                    'total_contacts': backup_info.get('total_contacts', 0),
                    'total_sent_emails': backup_info.get('total_sent_emails', 0),
                    'size': backup_file.stat().st_size
                })
            except:
                continue
        
        return sorted(backups, key=lambda x: x['created_at'], reverse=True)
    
    def analyze_template_performance(self, template_name: str) -> Dict:
        """Analyze performance metrics for a specific template"""
        if not self.sent_emails:
            return {'error': 'No sent emails to analyze'}
        
        template_emails = [email for email in self.sent_emails 
                          if email['template_name'] == template_name]
        
        if not template_emails:
            return {'error': f'No emails sent using template "{template_name}"'}
        
        # Basic metrics
        total_sent = len(template_emails)
        unique_recipients = len(set(email['recipient'] for email in template_emails))
        
        # Time analysis
        sent_dates = [datetime.fromisoformat(email['sent_at']) for email in template_emails]
        first_sent = min(sent_dates)
        last_sent = max(sent_dates)
        days_active = (last_sent - first_sent).days + 1
        
        # Frequency analysis
        daily_sends = {}
        for date in sent_dates:
            date_str = date.strftime('%Y-%m-%d')
            daily_sends[date_str] = daily_sends.get(date_str, 0) + 1
        
        avg_daily_sends = sum(daily_sends.values()) / len(daily_sends) if daily_sends else 0
        max_daily_sends = max(daily_sends.values()) if daily_sends else 0
        
        # Variable usage analysis
        variable_usage = {}
        for email in template_emails:
            for var, value in email.get('variables', {}).items():
                if var not in variable_usage:
                    variable_usage[var] = {'count': 0, 'values': set()}
                variable_usage[var]['count'] += 1
                variable_usage[var]['values'].add(value)
        
        # Convert sets to lists for JSON serialization
        for var in variable_usage:
            variable_usage[var]['values'] = list(variable_usage[var]['values'])
        
        return {
            'template_name': template_name,
            'total_sent': total_sent,
            'unique_recipients': unique_recipients,
            'first_sent': first_sent.isoformat(),
            'last_sent': last_sent.isoformat(),
            'days_active': days_active,
            'avg_daily_sends': round(avg_daily_sends, 2),
            'max_daily_sends': max_daily_sends,
            'variable_usage': variable_usage,
            'daily_send_pattern': daily_sends
        }
    
    def get_template_engagement_score(self, template_name: str) -> Dict:
        """Calculate engagement score for a template based on various factors"""
        template = self.get_template(template_name)
        if not template:
            return {'error': 'Template not found'}
        
        score = 0
        factors = {}
        
        # Length analysis
        subject_length = len(template['subject'])
        body_length = len(template['body'])
        
        if 30 <= subject_length <= 60:
            score += 20
            factors['subject_length'] = 'Optimal (30-60 chars)'
        elif 20 <= subject_length <= 80:
            score += 15
            factors['subject_length'] = 'Good (20-80 chars)'
        else:
            factors['subject_length'] = 'Could be optimized'
        
        if 100 <= body_length <= 300:
            score += 25
            factors['body_length'] = 'Optimal (100-300 chars)'
        elif 50 <= body_length <= 500:
            score += 20
            factors['body_length'] = 'Good (50-500 chars)'
        else:
            factors['body_length'] = 'Could be optimized'
        
        # Variable analysis
        variable_count = len(template['variables'])
        if 3 <= variable_count <= 7:
            score += 20
            factors['variables'] = f'Good balance ({variable_count} variables)'
        elif variable_count < 3:
            score += 10
            factors['variables'] = f'Low personalization ({variable_count} variables)'
        else:
            factors['variables'] = f'High complexity ({variable_count} variables)'
        
        # Content analysis
        content_score = 0
        
        # Check for call-to-action
        cta_words = ['click', 'visit', 'call', 'email', 'contact', 'schedule', 'book', 'register']
        if any(word in template['body'].lower() for word in cta_words):
            content_score += 15
            factors['call_to_action'] = 'Present'
        else:
            factors['call_to_action'] = 'Missing'
        
        # Check for questions
        if '?' in template['body']:
            content_score += 10
            factors['questions'] = 'Present'
        else:
            factors['questions'] = 'Missing'
        
        # Check for personalization
        personal_words = ['you', 'your', 'name', 'company']
        personal_count = sum(1 for word in personal_words if word in template['body'].lower())
        if personal_count >= 2:
            content_score += 10
            factors['personalization'] = 'Good'
        else:
            factors['personalization'] = 'Could be improved'
        
        score += content_score
        
        # Category bonus
        category = template.get('category', 'custom')
        if category in ['business', 'marketing']:
            score += 5
            factors['category'] = f'Professional category ({category})'
        else:
            factors['category'] = f'Category: {category}'
        
        return {
            'template_name': template_name,
            'overall_score': min(score, 100),
            'factors': factors,
            'recommendations': self._generate_template_recommendations(factors)
        }
    
    def _generate_template_recommendations(self, factors: Dict) -> List[str]:
        """Generate recommendations based on template analysis factors"""
        recommendations = []
        
        if factors.get('subject_length') == 'Could be optimized':
            recommendations.append("Consider optimizing subject line length (30-60 characters ideal)")
        
        if factors.get('body_length') == 'Could be optimized':
            recommendations.append("Email body length could be optimized (100-300 characters ideal)")
        
        if factors.get('call_to_action') == 'Missing':
            recommendations.append("Add a clear call-to-action to improve engagement")
        
        if factors.get('questions') == 'Missing':
            recommendations.append("Consider adding questions to encourage responses")
        
        if factors.get('personalization') == 'Could be improved':
            recommendations.append("Increase personalization by using more 'you' and 'your' references")
        
        if 'variables' in factors and 'Low personalization' in factors['variables']:
            recommendations.append("Consider adding more variables for better personalization")
        
        if 'variables' in factors and 'High complexity' in factors['variables']:
            recommendations.append("Consider reducing variables to simplify template usage")
        
        return recommendations
    
    def get_trending_templates(self, days: int = 30) -> List[Dict]:
        """Get templates that are trending in usage"""
        if not self.sent_emails:
            return []
        
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_emails = [email for email in self.sent_emails 
                        if datetime.fromisoformat(email['sent_at']) >= cutoff_date]
        
        template_counts = {}
        for email in recent_emails:
            template = email['template_name']
            template_counts[template] = template_counts.get(template, 0) + 1
        
        trending = []
        for template, count in template_counts.items():
            # Get historical data for comparison
            all_template_emails = [email for email in self.sent_emails 
                                 if email['template_name'] == template]
            
            if len(all_template_emails) > count:  # Has historical data
                historical_avg = len(all_template_emails) / (len(self.sent_emails) / len(template_counts))
                growth_rate = (count / days) / (historical_avg / 30) if historical_avg > 0 else 0
            else:
                growth_rate = 1.0  # New template
            
            trending.append({
                'template_name': template,
                'recent_usage': count,
                'growth_rate': round(growth_rate, 2),
                'days_analyzed': days
            })
        
        return sorted(trending, key=lambda x: x['recent_usage'], reverse=True)
    
    def generate_performance_report(self) -> str:
        """Generate a comprehensive performance report"""
        if not self.sent_emails:
            return "No email data available for performance analysis."
        
        report = []
        report.append("=" * 70)
        report.append("EMAIL TEMPLATE PERFORMANCE ANALYTICS REPORT")
        report.append("=" * 70)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Overall statistics
        total_emails = len(self.sent_emails)
        unique_templates = len(set(email['template_name'] for email in self.sent_emails))
        unique_recipients = len(set(email['recipient'] for email in self.sent_emails))
        
        report.append("📊 OVERALL STATISTICS")
        report.append(f"Total emails sent: {total_emails}")
        report.append(f"Unique templates used: {unique_templates}")
        report.append(f"Unique recipients: {unique_recipients}")
        report.append(f"Average emails per template: {total_emails/unique_templates:.1f}")
        report.append("")
        
        # Top performing templates
        template_usage = {}
        for email in self.sent_emails:
            template = email['template_name']
            template_usage[template] = template_usage.get(template, 0) + 1
        
        top_templates = sorted(template_usage.items(), key=lambda x: x[1], reverse=True)[:5]
        report.append("🏆 TOP PERFORMING TEMPLATES")
        for i, (template, count) in enumerate(top_templates, 1):
            percentage = (count / total_emails) * 100
            report.append(f"{i}. {template}: {count} emails ({percentage:.1f}%)")
        report.append("")
        
        # Trending templates
        trending = self.get_trending_templates(30)
        if trending:
            report.append("📈 TRENDING TEMPLATES (Last 30 days)")
            for i, trend in enumerate(trending[:5], 1):
                report.append(f"{i}. {trend['template_name']}: {trend['recent_usage']} emails")
                if trend['growth_rate'] > 1.5:
                    report.append(f"   ⬆️  High growth rate: {trend['growth_rate']}x")
        report.append("")
        
        # Template engagement scores
        report.append("🎯 TEMPLATE ENGAGEMENT SCORES")
        for template_name in template_usage.keys():
            engagement = self.get_template_engagement_score(template_name)
            if 'error' not in engagement:
                score = engagement['overall_score']
                status = "🟢 Excellent" if score >= 80 else "🟡 Good" if score >= 60 else "🔴 Needs Improvement"
                report.append(f"{template_name}: {score}/100 {status}")
        report.append("")
        
        # Recommendations
        report.append("💡 TOP RECOMMENDATIONS")
        all_recommendations = []
        for template_name in template_usage.keys():
            engagement = self.get_template_engagement_score(template_name)
            if 'error' not in engagement:
                all_recommendations.extend(engagement['recommendations'])
        
        # Get unique recommendations and count frequency
        rec_counts = {}
        for rec in all_recommendations:
            rec_counts[rec] = rec_counts.get(rec, 0) + 1
        
        top_recs = sorted(rec_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        for i, (rec, count) in enumerate(top_recs, 1):
            report.append(f"{i}. {rec} (applies to {count} templates)")
        
        report.append("=" * 70)
        return "\n".join(report)
    
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
        print("8. Duplicate & Version Templates")
        print("9. Import/Export & Backup")
        print("10. Analytics & Performance")
        print("11. Exit")
        
        choice = input("\nEnter your choice (1-11): ").strip()
        
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
            print("\n📋 Template Duplication & Versioning")
            print("1. Duplicate template")
            print("2. View template versions")
            print("3. Update template version")
            print("4. Back to main menu")
            
            version_choice = input("Choose option: ").strip()
            
            if version_choice == '1':
                templates = manager.list_templates()
                if not templates:
                    print("❌ No templates available to duplicate!")
                    continue
                
                print("\n📝 Available templates:")
                for i, template_name in enumerate(templates, 1):
                    template = manager.get_template(template_name)
                    version = template.get('version', 1)
                    print(f"{i}. {template_name} (v{version})")
                
                template_choice = input("\nChoose template to duplicate: ").strip()
                if not template_choice.isdigit() or not (1 <= int(template_choice) <= len(templates)):
                    print("❌ Invalid choice!")
                    continue
                
                original_name = templates[int(template_choice) - 1]
                new_name = input(f"Enter new name for '{original_name}': ").strip()
                
                if not new_name:
                    print("❌ New name is required!")
                    continue
                
                if new_name in manager.templates:
                    print("❌ Template with that name already exists!")
                    continue
                
                duplicated = manager.duplicate_template(original_name, new_name)
                if duplicated:
                    print(f"✅ Template '{original_name}' duplicated to '{new_name}'!")
                    print(f"Version: {duplicated.get('version', 1)}")
                else:
                    print("❌ Failed to duplicate template!")
            
            elif version_choice == '2':
                templates = manager.list_templates()
                if not templates:
                    print("❌ No templates available!")
                    continue
                
                print("\n📝 Available templates:")
                for i, template_name in enumerate(templates, 1):
                    template = manager.get_template(template_name)
                    version = template.get('version', 1)
                    print(f"{i}. {template_name} (v{version})")
                
                template_choice = input("\nChoose template to view versions: ").strip()
                if not template_choice.isdigit() or not (1 <= int(template_choice) <= len(templates)):
                    print("❌ Invalid choice!")
                    continue
                
                template_name = templates[int(template_choice) - 1]
                versions = manager.get_template_versions(template_name)
                
                if len(versions) == 1:
                    print(f"\n📋 Template '{template_name}' has only one version (v{versions[0]['version']})")
                else:
                    print(f"\n📋 Versions of '{template_name}':")
                    for version_info in versions:
                        status = "Original" if version_info['is_original'] else "Duplicate"
                        created = datetime.fromisoformat(version_info['created_at']).strftime('%Y-%m-%d %H:%M')
                        print(f"  {version_info['name']} - v{version_info['version']} ({status}) - {created}")
            
            elif version_choice == '3':
                templates = manager.list_templates()
                if not templates:
                    print("❌ No templates available!")
                    continue
                
                print("\n📝 Available templates:")
                for i, template_name in enumerate(templates, 1):
                    template = manager.get_template(template_name)
                    version = template.get('version', 1)
                    print(f"{i}. {template_name} (v{version})")
                
                template_choice = input("\nChoose template to update version: ").strip()
                if not template_choice.isdigit() or not (1 <= int(template_choice) <= len(templates)):
                    print("❌ Invalid choice!")
                    continue
                
                template_name = templates[int(template_choice) - 1]
                if manager.update_template_version(template_name):
                    new_version = manager.get_template(template_name).get('version', 1)
                    print(f"✅ Template '{template_name}' updated to version {new_version}!")
                else:
                    print("❌ Failed to update template version!")
        
        elif choice == '9':
            print("\n📦 Import/Export & Backup System")
            print("1. Export templates")
            print("2. Import templates")
            print("3. Create complete backup")
            print("4. Restore from backup")
            print("5. List available backups")
            print("6. Back to main menu")
            
            backup_choice = input("Choose option: ").strip()
            
            if backup_choice == '1':
                print("\n📤 Export Templates")
                include_contacts = input("Include contacts in export? (y/n): ").lower().strip() == 'y'
                custom_filename = input("Custom filename (or press Enter for auto-generated): ").strip()
                
                try:
                    filename = manager.export_templates(custom_filename if custom_filename else None, include_contacts)
                    print(f"✅ Templates exported successfully to: {filename}")
                    if include_contacts:
                        print(f"📋 Included {len(manager.contacts)} contacts")
                except Exception as e:
                    print(f"❌ Export failed: {e}")
            
            elif backup_choice == '2':
                print("\n📥 Import Templates")
                filename = input("Enter backup filename: ").strip()
                
                if not filename:
                    print("❌ Filename is required!")
                    continue
                
                if not Path(filename).exists():
                    print("❌ File not found!")
                    continue
                
                overwrite = input("Overwrite existing templates? (y/n): ").lower().strip() == 'y'
                
                try:
                    result = manager.import_templates(filename, overwrite)
                    print(f"✅ Import completed!")
                    print(f"  Imported: {result['imported']} templates")
                    print(f"  Skipped: {result['skipped']} templates")
                    print(f"  Overwritten: {result['overwritten']} templates")
                    
                    if result['export_info']:
                        exported_at = result['export_info'].get('exported_at')
                        if exported_at:
                            export_date = datetime.fromisoformat(exported_at).strftime('%Y-%m-%d %H:%M')
                            print(f"  Original export date: {export_date}")
                except Exception as e:
                    print(f"❌ Import failed: {e}")
            
            elif backup_choice == '3':
                print("\n💾 Creating Complete Backup...")
                try:
                    backup_file = manager.create_backup()
                    print(f"✅ Complete backup created: {backup_file}")
                    
                    # Show backup info
                    backup_info = {
                        'templates': len(manager.templates),
                        'contacts': len(manager.contacts),
                        'sent_emails': len(manager.sent_emails)
                    }
                    print(f"📊 Backup contains:")
                    print(f"  Templates: {backup_info['templates']}")
                    print(f"  Contacts: {backup_info['contacts']}")
                    print(f"  Sent emails: {backup_info['sent_emails']}")
                except Exception as e:
                    print(f"❌ Backup failed: {e}")
            
            elif backup_choice == '4':
                print("\n🔄 Restore from Backup")
                backups = manager.list_backups()
                
                if not backups:
                    print("❌ No backup files found!")
                    continue
                
                print(f"\n📋 Available backups ({len(backups)}):")
                for i, backup in enumerate(backups, 1):
                    created_date = datetime.fromisoformat(backup['created_at']).strftime('%Y-%m-%d %H:%M')
                    size_kb = backup['size'] / 1024
                    print(f"{i}. {backup['filename']}")
                    print(f"   Created: {created_date}")
                    print(f"   Templates: {backup['total_templates']}, Contacts: {backup['total_contacts']}")
                    print(f"   Size: {size_kb:.1f} KB")
                    print()
                
                backup_choice = input("Choose backup to restore (or press Enter to cancel): ").strip()
                if not backup_choice.isdigit() or not (1 <= int(backup_choice) <= len(backups)):
                    print("❌ Invalid choice!")
                    continue
                
                selected_backup = backups[int(backup_choice) - 1]
                confirm = input(f"⚠️  This will overwrite all current data. Continue? (y/n): ").lower().strip()
                
                if confirm == 'y':
                    if manager.restore_from_backup(selected_backup['path']):
                        print("✅ Restore completed successfully!")
                        print(f"📊 Restored data:")
                        print(f"  Templates: {selected_backup['total_templates']}")
                        print(f"  Contacts: {selected_backup['total_contacts']}")
                        print(f"  Sent emails: {selected_backup['total_sent_emails']}")
                    else:
                        print("❌ Restore failed!")
                else:
                    print("🔄 Restore cancelled.")
            
            elif backup_choice == '5':
                print("\n📋 Available Backups")
                backups = manager.list_backups()
                
                if not backups:
                    print("❌ No backup files found!")
                    continue
                
                print(f"\n📦 Found {len(backups)} backup(s):")
                for i, backup in enumerate(backups, 1):
                    created_date = datetime.fromisoformat(backup['created_at']).strftime('%Y-%m-%d %H:%M')
                    size_kb = backup['size'] / 1024
                    print(f"{i}. {backup['filename']}")
                    print(f"   📅 Created: {created_date}")
                    print(f"   📊 Templates: {backup['total_templates']}")
                    print(f"   👥 Contacts: {backup['total_contacts']}")
                    print(f"   📧 Sent emails: {backup['total_sent_emails']}")
                    print(f"   💾 Size: {size_kb:.1f} KB")
                    print()
        
        elif choice == '10':
            print("\n📊 Analytics & Performance Tracking")
            print("1. Analyze template performance")
            print("2. Get template engagement score")
            print("3. View trending templates")
            print("4. Generate performance report")
            print("5. Back to main menu")
            
            analytics_choice = input("Choose option: ").strip()
            
            if analytics_choice == '1':
                templates = manager.list_templates()
                if not templates:
                    print("❌ No templates available!")
                    continue
                
                print("\n📝 Available templates:")
                for i, template_name in enumerate(templates, 1):
                    template = manager.get_template(template_name)
                    print(f"{i}. {template_name} ({template.get('category', 'custom')})")
                
                template_choice = input("\nChoose template to analyze: ").strip()
                if not template_choice.isdigit() or not (1 <= int(template_choice) <= len(templates)):
                    print("❌ Invalid choice!")
                    continue
                
                template_name = templates[int(template_choice) - 1]
                performance = manager.analyze_template_performance(template_name)
                
                if 'error' in performance:
                    print(f"❌ {performance['error']}")
                else:
                    print(f"\n📊 Performance Analysis for '{template_name}':")
                    print(f"  Total emails sent: {performance['total_sent']}")
                    print(f"  Unique recipients: {performance['unique_recipients']}")
                    print(f"  Days active: {performance['days_active']}")
                    print(f"  Average daily sends: {performance['avg_daily_sends']}")
                    print(f"  Maximum daily sends: {performance['max_daily_sends']}")
                    
                    if performance['variable_usage']:
                        print(f"\n  Variable Usage:")
                        for var, data in performance['variable_usage'].items():
                            print(f"    {var}: {data['count']} times ({len(data['values'])} unique values)")
            
            elif analytics_choice == '2':
                templates = manager.list_templates()
                if not templates:
                    print("❌ No templates available!")
                    continue
                
                print("\n📝 Available templates:")
                for i, template_name in enumerate(templates, 1):
                    template = manager.get_template(template_name)
                    print(f"{i}. {template_name} ({template.get('category', 'custom')})")
                
                template_choice = input("\nChoose template for engagement analysis: ").strip()
                if not template_choice.isdigit() or not (1 <= int(template_choice) <= len(templates)):
                    print("❌ Invalid choice!")
                    continue
                
                template_name = templates[int(template_choice) - 1]
                engagement = manager.get_template_engagement_score(template_name)
                
                if 'error' in engagement:
                    print(f"❌ {engagement['error']}")
                else:
                    print(f"\n🎯 Engagement Analysis for '{template_name}':")
                    print(f"  Overall Score: {engagement['overall_score']}/100")
                    
                    score = engagement['overall_score']
                    if score >= 80:
                        print("  Status: 🟢 Excellent")
                    elif score >= 60:
                        print("  Status: 🟡 Good")
                    else:
                        print("  Status: 🔴 Needs Improvement")
                    
                    print(f"\n  Analysis Factors:")
                    for factor, status in engagement['factors'].items():
                        print(f"    {factor.replace('_', ' ').title()}: {status}")
                    
                    if engagement['recommendations']:
                        print(f"\n  💡 Recommendations:")
                        for i, rec in enumerate(engagement['recommendations'], 1):
                            print(f"    {i}. {rec}")
            
            elif analytics_choice == '3':
                print("\n📈 Trending Templates Analysis")
                days = input("Analyze last N days (default: 30): ").strip()
                days = int(days) if days.isdigit() else 30
                
                trending = manager.get_trending_templates(days)
                
                if not trending:
                    print(f"❌ No email data available for the last {days} days!")
                    continue
                
                print(f"\n📈 Trending Templates (Last {days} days):")
                for i, trend in enumerate(trending, 1):
                    print(f"{i}. {trend['template_name']}")
                    print(f"   Recent usage: {trend['recent_usage']} emails")
                    print(f"   Growth rate: {trend['growth_rate']}x")
                    
                    if trend['growth_rate'] > 1.5:
                        print(f"   ⬆️  High growth trend!")
                    elif trend['growth_rate'] < 0.5:
                        print(f"   ⬇️  Declining usage")
                    print()
            
            elif analytics_choice == '4':
                print("\n📊 Generating Performance Report...")
                report = manager.generate_performance_report()
                print("\n" + report)
        
        elif choice == '11':
            print("👋 Thanks for using Email Template Manager!")
            break
        
        else:
            print("❌ Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
