#!/usr/bin/env python3
"""
System Monitor & Alert Automation
A comprehensive system monitoring automation that tracks resources,
generates alerts, and manages logs automatically.
"""

import psutil
import os
import json
import time
import logging
from datetime import datetime, timedelta
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading
import schedule

class SystemMonitor:
    def __init__(self, config_file="monitor_config.json"):
        self.config_file = config_file
        self.config = self.load_config()
        self.setup_logging()
        self.alert_history = []
        self.monitoring = False
        
    def load_config(self):
        """Load configuration from JSON file or create default"""
        default_config = {
            "cpu_threshold": 80.0,
            "memory_threshold": 85.0,
            "disk_threshold": 90.0,
            "check_interval": 30,  # seconds
            "log_retention_days": 7,
            "email_alerts": {
                "enabled": False,
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "username": "",
                "password": "",
                "recipients": []
            },
            "log_file": "system_monitor.log",
            "data_file": "system_data.json"
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                # Merge with defaults for any missing keys
                for key, value in default_config.items():
                    if key not in config:
                        config[key] = value
                return config
            except Exception as e:
                print(f"Error loading config: {e}. Using defaults.")
                return default_config
        else:
            # Create default config file
            with open(self.config_file, 'w') as f:
                json.dump(default_config, f, indent=2)
            print(f"Created default config file: {self.config_file}")
            return default_config
    
    def setup_logging(self):
        """Setup logging configuration"""
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        logging.basicConfig(
            filename=self.config['log_file'],
            level=logging.INFO,
            format=log_format,
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Also log to console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(log_format)
        console_handler.setFormatter(formatter)
        logging.getLogger().addHandler(console_handler)
    
    def get_system_stats(self):
        """Collect comprehensive system statistics"""
        try:
            stats = {
                'timestamp': datetime.now().isoformat(),
                'cpu': {
                    'percent': psutil.cpu_percent(interval=1),
                    'count': psutil.cpu_count(),
                    'freq': psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None
                },
                'memory': {
                    'total': psutil.virtual_memory().total,
                    'available': psutil.virtual_memory().available,
                    'percent': psutil.virtual_memory().percent,
                    'used': psutil.virtual_memory().used
                },
                'disk': {
                    'total': psutil.disk_usage('/').total,
                    'used': psutil.disk_usage('/').used,
                    'free': psutil.disk_usage('/').free,
                    'percent': psutil.disk_usage('/').percent
                },
                'network': {
                    'bytes_sent': psutil.net_io_counters().bytes_sent,
                    'bytes_recv': psutil.net_io_counters().bytes_recv,
                    'packets_sent': psutil.net_io_counters().packets_sent,
                    'packets_recv': psutil.net_io_counters().packets_recv
                },
                'processes': {
                    'total': len(psutil.pids()),
                    'running': len([p for p in psutil.process_iter(['status']) if p.info['status'] == 'running'])
                }
            }
            return stats
        except Exception as e:
            logging.error(f"Error collecting system stats: {e}")
            return None
    
    def check_thresholds(self, stats):
        """Check if any metrics exceed configured thresholds"""
        alerts = []
        
        if stats['cpu']['percent'] > self.config['cpu_threshold']:
            alerts.append({
                'type': 'CPU',
                'value': stats['cpu']['percent'],
                'threshold': self.config['cpu_threshold'],
                'message': f"High CPU usage: {stats['cpu']['percent']:.1f}%"
            })
        
        if stats['memory']['percent'] > self.config['memory_threshold']:
            alerts.append({
                'type': 'Memory',
                'value': stats['memory']['percent'],
                'threshold': self.config['memory_threshold'],
                'message': f"High memory usage: {stats['memory']['percent']:.1f}%"
            })
        
        if stats['disk']['percent'] > self.config['disk_threshold']:
            alerts.append({
                'type': 'Disk',
                'value': stats['disk']['percent'],
                'threshold': self.config['disk_threshold'],
                'message': f"High disk usage: {stats['disk']['percent']:.1f}%"
            })
        
        return alerts
    
    def send_email_alert(self, alerts):
        """Send email alerts if configured"""
        if not self.config['email_alerts']['enabled']:
            return
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config['email_alerts']['username']
            msg['To'] = ', '.join(self.config['email_alerts']['recipients'])
            msg['Subject'] = f"System Alert - {len(alerts)} Issues Detected"
            
            body = "System monitoring alerts:\n\n"
            for alert in alerts:
                body += f"• {alert['message']}\n"
            
            body += f"\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.config['email_alerts']['smtp_server'], 
                                self.config['email_alerts']['smtp_port'])
            server.starttls()
            server.login(self.config['email_alerts']['username'], 
                        self.config['email_alerts']['password'])
            
            text = msg.as_string()
            server.sendmail(self.config['email_alerts']['username'], 
                          self.config['email_alerts']['recipients'], text)
            server.quit()
            
            logging.info("Email alert sent successfully")
        except Exception as e:
            logging.error(f"Failed to send email alert: {e}")
    
    def save_data(self, stats):
        """Save system data to JSON file"""
        try:
            data_file = self.config['data_file']
            
            # Load existing data
            if os.path.exists(data_file):
                with open(data_file, 'r') as f:
                    data = json.load(f)
            else:
                data = []
            
            # Add new data point
            data.append(stats)
            
            # Keep only last 1000 entries to prevent file from growing too large
            if len(data) > 1000:
                data = data[-1000:]
            
            # Save updated data
            with open(data_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            logging.error(f"Error saving data: {e}")
    
    def cleanup_old_logs(self):
        """Clean up old log files based on retention policy"""
        try:
            log_file = Path(self.config['log_file'])
            if log_file.exists():
                file_age = datetime.now() - datetime.fromtimestamp(log_file.stat().st_mtime)
                if file_age.days > self.config['log_retention_days']:
                    # Archive old log
                    archive_name = f"{log_file.stem}_{datetime.now().strftime('%Y%m%d')}.log"
                    log_file.rename(archive_name)
                    logging.info(f"Archived old log file: {archive_name}")
        except Exception as e:
            logging.error(f"Error cleaning up logs: {e}")
    
    def generate_report(self):
        """Generate a system health report"""
        try:
            data_file = self.config['data_file']
            if not os.path.exists(data_file):
                return "No data available for report generation"
            
            with open(data_file, 'r') as f:
                data = json.load(f)
            
            if not data:
                return "No data available for report generation"
            
            # Calculate averages for last 24 hours
            recent_data = [d for d in data if 
                          datetime.fromisoformat(d['timestamp']) > 
                          datetime.now() - timedelta(hours=24)]
            
            if not recent_data:
                return "No recent data available"
            
            avg_cpu = sum(d['cpu']['percent'] for d in recent_data) / len(recent_data)
            avg_memory = sum(d['memory']['percent'] for d in recent_data) / len(recent_data)
            avg_disk = sum(d['disk']['percent'] for d in recent_data) / len(recent_data)
            
            report = f"""
System Health Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*60}
Data Points Analyzed: {len(recent_data)}
Time Period: Last 24 hours

Average CPU Usage: {avg_cpu:.1f}%
Average Memory Usage: {avg_memory:.1f}%
Average Disk Usage: {avg_disk:.1f}%

Current Status:
- CPU: {'⚠️ HIGH' if avg_cpu > self.config['cpu_threshold'] else '✅ Normal'}
- Memory: {'⚠️ HIGH' if avg_memory > self.config['memory_threshold'] else '✅ Normal'}
- Disk: {'⚠️ HIGH' if avg_disk > self.config['disk_threshold'] else '✅ Normal'}

Total Alerts Generated: {len(self.alert_history)}
"""
            return report
        except Exception as e:
            logging.error(f"Error generating report: {e}")
            return f"Error generating report: {e}"
    
    def monitor_cycle(self):
        """Single monitoring cycle"""
        logging.info("Starting monitoring cycle...")
        
        # Collect system stats
        stats = self.get_system_stats()
        if not stats:
            return
        
        # Check thresholds
        alerts = self.check_thresholds(stats)
        
        # Handle alerts
        if alerts:
            for alert in alerts:
                logging.warning(alert['message'])
                self.alert_history.append({
                    'timestamp': datetime.now().isoformat(),
                    'alert': alert
                })
            
            # Send email alerts
            self.send_email_alert(alerts)
        
        # Save data
        self.save_data(stats)
        
        # Log current status
        logging.info(f"CPU: {stats['cpu']['percent']:.1f}%, "
                    f"Memory: {stats['memory']['percent']:.1f}%, "
                    f"Disk: {stats['disk']['percent']:.1f}%")
    
    def start_monitoring(self):
        """Start continuous monitoring"""
        self.monitoring = True
        logging.info("🚀 System monitoring started")
        
        # Schedule monitoring
        schedule.every(self.config['check_interval']).seconds.do(self.monitor_cycle)
        schedule.every().day.at("02:00").do(self.cleanup_old_logs)
        
        try:
            while self.monitoring:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            logging.info("Monitoring stopped by user")
            self.stop_monitoring()
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.monitoring = False
        logging.info("⏹️ System monitoring stopped")
    
    def run_automation(self):
        """Main automation runner"""
        print("🖥️ System Monitor & Alert Automation")
        print("=" * 50)
        
        # Generate initial report
        print("📊 Generating system report...")
        report = self.generate_report()
        print(report)
        
        # Start monitoring
        print(f"\n🔍 Starting monitoring (interval: {self.config['check_interval']}s)")
        print("Press Ctrl+C to stop monitoring")
        
        try:
            self.start_monitoring()
        except Exception as e:
            logging.error(f"Monitoring failed: {e}")
            print(f"❌ Monitoring failed: {e}")

def main():
    """Main function"""
    try:
        monitor = SystemMonitor()
        monitor.run_automation()
    except KeyboardInterrupt:
        print("\n\n⏹️ Automation interrupted by user")
    except Exception as e:
        print(f"\n❌ Automation failed: {e}")

if __name__ == "__main__":
    main()
