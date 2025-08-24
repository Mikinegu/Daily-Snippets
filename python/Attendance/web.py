from flask import Flask, request, jsonify
import csv
from datetime import datetime

app = Flask(__name__)

# Student ID to name mapping dictionary - update with your real student data
student_dict = {
    "FSP2025001": "John Doe",
    "FSP2025002": "Jane Smith",
    "FSP2025003": "Michael Lee"
    # Add all student IDs and names here
}

@app.route('/attendance', methods=['POST'])
def attendance():
    data = request.json
    if not data or 'student_id' not in data:
        return jsonify({'status': 'error', 'message': 'Missing student ID'}), 400
    student_id = data.get('student_id')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if not student_id:
        return jsonify({'status': 'error', 'message': 'Missing student ID'}), 400
    
    # Lookup student name or mark as Unknown if ID not found
    student_name = student_dict.get(student_id, "Unknown Student")
    
    # Save attendance in CSV with ID, name, and timestamp
    with open('attendance.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([student_id, student_name, timestamp])
    
    return jsonify({'status': 'success', 'message': f'Attendance recorded for {student_name}'}), 200

if __name__ == "__main__":
    # Run server accessible on local network: http://0.0.0.0:5000
    app.run(host='0.0.0.0', port=5000)
