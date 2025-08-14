import random
import string
import os
import time
import json
from datetime import datetime, timedelta
import csv

class RandomAutomation:
    def __init__(self):
        self.output_dir = "random_output"
        self.ensure_output_directory()
        
    def ensure_output_directory(self):
        """Create output directory if it doesn't exist"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"Created directory: {self.output_dir}")
    
    def generate_random_string(self, length=10):
        """Generate a random string of specified length"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    def generate_random_data(self, count=100):
        """Generate random data records"""
        data = []
        for i in range(count):
            record = {
                'id': i + 1,
                'name': f"User_{self.generate_random_string(8)}",
                'email': f"{self.generate_random_string(8)}@example.com",
                'age': random.randint(18, 80),
                'score': round(random.uniform(0, 100), 2),
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'category': random.choice(['A', 'B', 'C', 'D']),
                'active': random.choice([True, False])
            }
            data.append(record)
        return data
    
    def create_random_files(self, num_files=5):
        """Create random text files with random content"""
        file_types = ['.txt', '.log', '.md', '.json']
        
        for i in range(num_files):
            file_type = random.choice(file_types)
            filename = f"random_file_{i+1}_{self.generate_random_string(5)}{file_type}"
            filepath = os.path.join(self.output_dir, filename)
            
            if file_type == '.json':
                content = {
                    'file_id': i + 1,
                    'random_data': [self.generate_random_string(10) for _ in range(random.randint(3, 8))],
                    'metadata': {
                        'created': datetime.now().isoformat(),
                        'version': f"1.{random.randint(0, 9)}.{random.randint(0, 9)}"
                    }
                }
                with open(filepath, 'w') as f:
                    json.dump(content, f, indent=2)
            else:
                lines = [self.generate_random_string(random.randint(20, 50)) for _ in range(random.randint(5, 15))]
                with open(filepath, 'w') as f:
                    f.write('\n'.join(lines))
            
            print(f"Created file: {filename}")
    
    def generate_csv_report(self, data):
        """Generate a CSV report from random data"""
        csv_file = os.path.join(self.output_dir, f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
        
        with open(csv_file, 'w', newline='') as f:
            if data:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
        
        print(f"Generated CSV report: {os.path.basename(csv_file)}")
        return csv_file
    
    def perform_random_operations(self):
        """Perform various random operations"""
        operations = [
            self.create_random_files,
            lambda: self.generate_random_data(random.randint(50, 200)),
            lambda: time.sleep(random.uniform(0.1, 0.5)),
            lambda: print(f"Random operation at {datetime.now().strftime('%H:%M:%S')}"),
            lambda: self.generate_random_string(random.randint(15, 25))
        ]
        
        # Randomly select and execute operations
        for _ in range(random.randint(3, 8)):
            operation = random.choice(operations)
            try:
                result = operation()
                if result:
                    print(f"Operation result: {str(result)[:50]}...")
            except Exception as e:
                print(f"Operation failed: {e}")
    
    def cleanup_old_files(self, max_age_hours=1):
        """Clean up files older than specified age"""
        current_time = datetime.now()
        deleted_count = 0
        
        for filename in os.listdir(self.output_dir):
            filepath = os.path.join(self.output_dir, filename)
            if os.path.isfile(filepath):
                file_time = datetime.fromtimestamp(os.path.getctime(filepath))
                age = current_time - file_time
                
                if age > timedelta(hours=max_age_hours):
                    try:
                        os.remove(filepath)
                        deleted_count += 1
                        print(f"Deleted old file: {filename}")
                    except Exception as e:
                        print(f"Failed to delete {filename}: {e}")
        
        if deleted_count > 0:
            print(f"Cleaned up {deleted_count} old files")
        else:
            print("No old files to clean up")
    
    def run_automation(self):
        """Main automation runner"""
        print("🚀 Starting Random Automation...")
        print("=" * 50)
        
        # Generate random data
        print("📊 Generating random data...")
        data = self.generate_random_data(random.randint(100, 300))
        print(f"Generated {len(data)} records")
        
        # Create random files
        print("\n📁 Creating random files...")
        self.create_random_files(random.randint(3, 8))
        
        # Generate CSV report
        print("\n📈 Generating CSV report...")
        self.generate_csv_report(data)
        
        # Perform random operations
        print("\n⚡ Performing random operations...")
        self.perform_random_operations()
        
        # Cleanup old files
        print("\n🧹 Cleaning up old files...")
        self.cleanup_old_files()
        
        print("\n" + "=" * 50)
        print("✅ Random Automation completed successfully!")
        print(f"📂 Check the '{self.output_dir}' directory for generated files")

def main():
    """Main function to run the automation"""
    try:
        automation = RandomAutomation()
        automation.run_automation()
    except KeyboardInterrupt:
        print("\n\n⏹️ Automation interrupted by user")
    except Exception as e:
        print(f"\n❌ Automation failed: {e}")

if __name__ == "__main__":
    main()
