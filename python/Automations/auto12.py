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
import hashlib
import shutil
import subprocess
import platform
import socket
import requests
from collections import deque
import statistics

class SystemMonitor:
    def __init__(self, config_file="monitor_config.json"):
        self.config_file = config_file
        self.config = self.load_config()
        self.setup_logging()
        self.alert_history = []
        self.monitoring = False
        self.performance_trends = deque(maxlen=100)
        self.network_status = {}
        self.backup_status = {}
        
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
            "data_file": "system_data.json",
            "web_dashboard": {
                "enabled": True,
                "port": 8080,
                "host": "localhost"
            },
            "backup_monitoring": {
                "enabled": True,
                "backup_paths": [],
                "check_interval_hours": 6
            },
            "auto_actions": {
                "enabled": False,
                "clear_temp_on_disk_full": True,
                "restart_service_on_cpu_high": False,
                "service_name": ""
            },
            "performance_analysis": {
                "enabled": True,
                "trend_window_hours": 24,
                "prediction_enabled": True
            },
            "network_monitoring": {
                "enabled": True,
                "ping_hosts": ["8.8.8.8", "1.1.1.1"],
                "check_interval_minutes": 5
            }
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
    
    def check_network_connectivity(self):
        """Check network connectivity to configured hosts"""
        if not self.config['network_monitoring']['enabled']:
            return {}
        
        network_status = {}
        for host in self.config['network_monitoring']['ping_hosts']:
            try:
                # Use ping command (cross-platform)
                if platform.system().lower() == "windows":
                    result = subprocess.run(['ping', '-n', '1', host], 
                                          capture_output=True, text=True, timeout=5)
                else:
                    result = subprocess.run(['ping', '-c', '1', host], 
                                          capture_output=True, text=True, timeout=5)
                
                network_status[host] = {
                    'reachable': result.returncode == 0,
                    'response_time': self._extract_ping_time(result.stdout),
                    'timestamp': datetime.now().isoformat()
                }
            except Exception as e:
                network_status[host] = {
                    'reachable': False,
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                }
        
        self.network_status = network_status
        return network_status
    
    def _extract_ping_time(self, ping_output):
        """Extract response time from ping output"""
        try:
            if platform.system().lower() == "windows":
                # Windows ping format: "time=123ms"
                import re
                match = re.search(r'time[<=](\d+)ms', ping_output)
                return int(match.group(1)) if match else None
            else:
                # Linux/Mac ping format: "time=123 ms"
                import re
                match = re.search(r'time=(\d+\.?\d*)\s*ms', ping_output)
                return float(match.group(1)) if match else None
        except:
            return None
    
    def monitor_backup_files(self):
        """Monitor backup files for integrity and age"""
        if not self.config['backup_monitoring']['enabled']:
            return {}
        
        backup_status = {}
        for backup_path in self.config['backup_monitoring']['backup_paths']:
            if os.path.exists(backup_path):
                try:
                    stat = os.stat(backup_path)
                    file_age = datetime.now() - datetime.fromtimestamp(stat.st_mtime)
                    
                    # Calculate file hash for integrity check
                    file_hash = self._calculate_file_hash(backup_path)
                    
                    backup_status[backup_path] = {
                        'exists': True,
                        'size': stat.st_size,
                        'age_hours': file_age.total_seconds() / 3600,
                        'last_modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        'hash': file_hash,
                        'status': 'fresh' if file_age.days < 1 else 'stale'
                    }
                except Exception as e:
                    backup_status[backup_path] = {
                        'exists': True,
                        'error': str(e),
                        'status': 'error'
                    }
            else:
                backup_status[backup_path] = {
                    'exists': False,
                    'status': 'missing'
                }
        
        self.backup_status = backup_status
        return backup_status
    
    def _calculate_file_hash(self, filepath):
        """Calculate MD5 hash of a file"""
        try:
            hash_md5 = hashlib.md5()
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            logging.error(f"Error calculating hash for {filepath}: {e}")
            return None
    
    def analyze_performance_trends(self, stats):
        """Analyze performance trends and make predictions"""
        if not self.config['performance_analysis']['enabled']:
            return {}
        
        # Add current stats to trends
        self.performance_trends.append({
            'timestamp': datetime.now(),
            'cpu': stats['cpu']['percent'],
            'memory': stats['memory']['percent'],
            'disk': stats['disk']['percent']
        })
        
        if len(self.performance_trends) < 10:
            return {'status': 'insufficient_data'}
        
        # Calculate trends
        cpu_values = [t['cpu'] for t in self.performance_trends]
        memory_values = [t['memory'] for t in self.performance_trends]
        disk_values = [t['disk'] for t in self.performance_trends]
        
        analysis = {
            'cpu_trend': self._calculate_trend(cpu_values),
            'memory_trend': self._calculate_trend(memory_values),
            'disk_trend': self._calculate_trend(disk_values),
            'cpu_prediction': self._predict_next_value(cpu_values) if self.config['performance_analysis']['prediction_enabled'] else None,
            'memory_prediction': self._predict_next_value(memory_values) if self.config['performance_analysis']['prediction_enabled'] else None,
            'disk_prediction': self._predict_next_value(disk_values) if self.config['performance_analysis']['prediction_enabled'] else None,
            'data_points': len(self.performance_trends)
        }
        
        return analysis
    
    def _calculate_trend(self, values):
        """Calculate trend direction and strength"""
        if len(values) < 2:
            return 'stable'
        
        # Simple linear regression slope
        n = len(values)
        x = list(range(n))
        y = values
        
        x_mean = sum(x) / n
        y_mean = sum(y) / n
        
        numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            return 'stable'
        
        slope = numerator / denominator
        
        if slope > 0.5:
            return 'increasing'
        elif slope < -0.5:
            return 'decreasing'
        else:
            return 'stable'
    
    def _predict_next_value(self, values):
        """Simple prediction based on recent trend"""
        if len(values) < 3:
            return None
        
        # Use last 3 values to predict next
        recent = values[-3:]
        trend = (recent[-1] - recent[0]) / 2
        prediction = recent[-1] + trend
        
        return max(0, min(100, prediction))  # Clamp between 0 and 100
    
    def perform_auto_actions(self, alerts):
        """Perform automatic actions based on alerts"""
        if not self.config['auto_actions']['enabled']:
            return
        
        actions_taken = []
        
        for alert in alerts:
            if alert['type'] == 'Disk' and self.config['auto_actions']['clear_temp_on_disk_full']:
                # Clear temporary files
                temp_cleared = self._clear_temp_files()
                if temp_cleared > 0:
                    actions_taken.append(f"Cleared {temp_cleared} MB of temporary files")
            
            elif alert['type'] == 'CPU' and self.config['auto_actions']['restart_service_on_cpu_high']:
                # Restart specified service
                service_name = self.config['auto_actions']['service_name']
                if service_name:
                    success = self._restart_service(service_name)
                    if success:
                        actions_taken.append(f"Restarted service: {service_name}")
        
        if actions_taken:
            logging.info(f"Auto-actions taken: {', '.join(actions_taken)}")
            return actions_taken
    
    def _clear_temp_files(self):
        """Clear temporary files to free up disk space"""
        temp_dirs = []
        total_cleared = 0
        
        if platform.system().lower() == "windows":
            temp_dirs = [
                os.environ.get('TEMP', ''),
                os.environ.get('TMP', ''),
                os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Temp')
            ]
        else:
            temp_dirs = ['/tmp', '/var/tmp']
        
        for temp_dir in temp_dirs:
            if os.path.exists(temp_dir):
                try:
                    for root, dirs, files in os.walk(temp_dir):
                        for file in files:
                            filepath = os.path.join(root, file)
                            try:
                                size = os.path.getsize(filepath)
                                os.remove(filepath)
                                total_cleared += size
                            except:
                                pass
                except:
                    pass
        
        return total_cleared // (1024 * 1024)  # Return MB
    
    def _restart_service(self, service_name):
        """Restart a system service"""
        try:
            if platform.system().lower() == "windows":
                subprocess.run(['net', 'stop', service_name], check=True)
                time.sleep(2)
                subprocess.run(['net', 'start', service_name], check=True)
            else:
                subprocess.run(['sudo', 'systemctl', 'restart', service_name], check=True)
            return True
        except Exception as e:
            logging.error(f"Failed to restart service {service_name}: {e}")
            return False
    
    def get_system_info(self):
        """Get comprehensive system information"""
        return {
            'hostname': socket.gethostname(),
            'platform': platform.platform(),
            'processor': platform.processor(),
            'python_version': platform.python_version(),
            'boot_time': datetime.fromtimestamp(psutil.boot_time()).isoformat(),
            'uptime_seconds': time.time() - psutil.boot_time(),
            'users': [user._asdict() for user in psutil.users()],
            'disk_partitions': [partition._asdict() for partition in psutil.disk_partitions()]
        }
    
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
        
        # Check network connectivity
        network_status = self.check_network_connectivity()
        
        # Monitor backup files
        backup_status = self.monitor_backup_files()
        
        # Analyze performance trends
        trend_analysis = self.analyze_performance_trends(stats)
        
        # Check thresholds
        alerts = self.check_thresholds(stats)
        
        # Perform auto-actions if alerts exist
        auto_actions = self.perform_auto_actions(alerts)
        
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
        
        # Enhanced stats with new data
        enhanced_stats = {
            **stats,
            'network_status': network_status,
            'backup_status': backup_status,
            'trend_analysis': trend_analysis,
            'auto_actions_taken': auto_actions
        }
        
        # Save data
        self.save_data(enhanced_stats)
        
        # Log current status with additional info
        log_msg = f"CPU: {stats['cpu']['percent']:.1f}%, Memory: {stats['memory']['percent']:.1f}%, Disk: {stats['disk']['percent']:.1f}%"
        
        if network_status:
            reachable_hosts = sum(1 for host in network_status.values() if host.get('reachable', False))
            log_msg += f", Network: {reachable_hosts}/{len(network_status)} hosts reachable"
        
        if trend_analysis and 'cpu_trend' in trend_analysis:
            log_msg += f", CPU Trend: {trend_analysis['cpu_trend']}"
        
        logging.info(log_msg)
    
    def start_monitoring(self):
        """Start continuous monitoring"""
        self.monitoring = True
        logging.info("🚀 System monitoring started")
        
        # Schedule monitoring
        schedule.every(self.config['check_interval']).seconds.do(self.monitor_cycle)
        schedule.every().day.at("02:00").do(self.cleanup_old_logs)
        
        # Schedule network monitoring
        if self.config['network_monitoring']['enabled']:
            schedule.every(self.config['network_monitoring']['check_interval_minutes']).minutes.do(self.check_network_connectivity)
        
        # Schedule backup monitoring
        if self.config['backup_monitoring']['enabled']:
            schedule.every(self.config['backup_monitoring']['check_interval_hours']).hours.do(self.monitor_backup_files)
        
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
    
    def start_web_dashboard(self):
        """Start a simple web dashboard (if enabled)"""
        if not self.config['web_dashboard']['enabled']:
            return
        
        def create_dashboard():
            try:
                from http.server import HTTPServer, BaseHTTPRequestHandler
                import json
                
                class DashboardHandler(BaseHTTPRequestHandler):
                    def do_GET(self):
                        if self.path == '/':
                            self.send_response(200)
                            self.send_header('Content-type', 'text/html')
                            self.end_headers()
                            
                            # Simple HTML dashboard
                            html = f"""
                            <!DOCTYPE html>
                            <html>
                            <head>
                                <title>System Monitor Dashboard</title>
                                <meta http-equiv="refresh" content="5">
                                <style>
                                    body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
                                    .container {{ max-width: 1200px; margin: 0 auto; }}
                                    .card {{ background: white; padding: 20px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                                    .status {{ display: inline-block; padding: 4px 8px; border-radius: 4px; color: white; }}
                                    .good {{ background: #4CAF50; }}
                                    .warning {{ background: #FF9800; }}
                                    .danger {{ background: #F44336; }}
                                    .metric {{ display: flex; justify-content: space-between; margin: 10px 0; }}
                                    .progress-bar {{ width: 100%; height: 20px; background: #e0e0e0; border-radius: 10px; overflow: hidden; }}
                                    .progress-fill {{ height: 100%; background: #4CAF50; transition: width 0.3s; }}
                                    .progress-fill.warning {{ background: #FF9800; }}
                                    .progress-fill.danger {{ background: #F44336; }}
                                </style>
                            </head>
                            <body>
                                <div class="container">
                                    <h1>🖥️ System Monitor Dashboard</h1>
                                    <p>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                                    
                                    <div class="card">
                                        <h2>System Status</h2>
                                        <div class="metric">
                                            <span>CPU Usage:</span>
                                            <span id="cpu-status">Loading...</span>
                                        </div>
                                        <div class="progress-bar">
                                            <div class="progress-fill" id="cpu-bar" style="width: 0%"></div>
                                        </div>
                                        
                                        <div class="metric">
                                            <span>Memory Usage:</span>
                                            <span id="memory-status">Loading...</span>
                                        </div>
                                        <div class="progress-bar">
                                            <div class="progress-fill" id="memory-bar" style="width: 0%"></div>
                                        </div>
                                        
                                        <div class="metric">
                                            <span>Disk Usage:</span>
                                            <span id="disk-status">Loading...</span>
                                        </div>
                                        <div class="progress-bar">
                                            <div class="progress-fill" id="disk-bar" style="width: 0%"></div>
                                        </div>
                                    </div>
                                    
                                    <div class="card">
                                        <h2>Network Status</h2>
                                        <div id="network-info">Loading...</div>
                                    </div>
                                    
                                    <div class="card">
                                        <h2>Recent Alerts</h2>
                                        <div id="alerts-info">Loading...</div>
                                    </div>
                                </div>
                                
                                <script>
                                    // Simple JavaScript to update dashboard
                                    function updateDashboard() {{
                                        fetch('/api/status')
                                        .then(response => response.json())
                                        .then(data => {{
                                            // Update CPU
                                            document.getElementById('cpu-status').textContent = data.cpu + '%';
                                            document.getElementById('cpu-bar').style.width = data.cpu + '%';
                                            document.getElementById('cpu-bar').className = 'progress-fill ' + 
                                                (data.cpu > 80 ? 'danger' : data.cpu > 60 ? 'warning' : '');
                                            
                                            // Update Memory
                                            document.getElementById('memory-status').textContent = data.memory + '%';
                                            document.getElementById('memory-bar').style.width = data.memory + '%';
                                            document.getElementById('memory-bar').className = 'progress-fill ' + 
                                                (data.memory > 85 ? 'danger' : data.memory > 70 ? 'warning' : '');
                                            
                                            // Update Disk
                                            document.getElementById('disk-status').textContent = data.disk + '%';
                                            document.getElementById('disk-bar').style.width = data.disk + '%';
                                            document.getElementById('disk-bar').className = 'progress-fill ' + 
                                                (data.disk > 90 ? 'danger' : data.disk > 80 ? 'warning' : '');
                                        }})
                                        .catch(error => console.error('Error:', error));
                                    }}
                                    
                                    // Update every 5 seconds
                                    setInterval(updateDashboard, 5000);
                                    updateDashboard();
                                </script>
                            </body>
                            </html>
                            """
                            self.wfile.write(html.encode())
                        
                        elif self.path == '/api/status':
                            self.send_response(200)
                            self.send_header('Content-type', 'application/json')
                            self.end_headers()
                            
                            # Get latest stats
                            stats = self.get_system_stats()
                            if stats:
                                response = {
                                    'cpu': round(stats['cpu']['percent'], 1),
                                    'memory': round(stats['memory']['percent'], 1),
                                    'disk': round(stats['disk']['percent'], 1),
                                    'timestamp': stats['timestamp']
                                }
                            else:
                                response = {'error': 'No data available'}
                            
                            self.wfile.write(json.dumps(response).encode())
                    
                    def log_message(self, format, *args):
                        pass  # Suppress log messages
                
                server = HTTPServer((self.config['web_dashboard']['host'], 
                                   self.config['web_dashboard']['port']), DashboardHandler)
                logging.info(f"🌐 Web dashboard started at http://{self.config['web_dashboard']['host']}:{self.config['web_dashboard']['port']}")
                server.serve_forever()
                
            except ImportError:
                logging.warning("Web dashboard requires Python's built-in http.server module")
            except Exception as e:
                logging.error(f"Failed to start web dashboard: {e}")
        
        # Start dashboard in a separate thread
        dashboard_thread = threading.Thread(target=create_dashboard, daemon=True)
        dashboard_thread.start()
    
    def run_automation(self):
        """Main automation runner"""
        print("🖥️ System Monitor & Alert Automation")
        print("=" * 50)
        
        # Start web dashboard
        self.start_web_dashboard()
        
        # Generate initial report
        print("📊 Generating system report...")
        report = self.generate_report()
        print(report)
        
        # Show system info
        print("\n🖥️ System Information:")
        system_info = self.get_system_info()
        print(f"Hostname: {system_info['hostname']}")
        print(f"Platform: {system_info['platform']}")
        print(f"Uptime: {system_info['uptime_seconds']/3600:.1f} hours")
        
        # Start monitoring
        print(f"\n🔍 Starting monitoring (interval: {self.config['check_interval']}s)")
        if self.config['web_dashboard']['enabled']:
            print(f"🌐 Web dashboard: http://{self.config['web_dashboard']['host']}:{self.config['web_dashboard']['port']}")
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
