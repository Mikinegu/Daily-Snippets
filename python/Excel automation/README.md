# Student Grouping Program

This Python script reads an Excel file containing student data and creates balanced groups based on gender, focusing only on engineering and robotics students.

## Features

- Reads Excel files with student data (Name, Stream, Gender)
- Filters for engineering and robotics students only
- Creates balanced groups based on gender distribution
- Supports multiple group sizes (default: 2 groups)
- Saves results to Excel file with separate sheets for each group
- Handles various gender and stream naming conventions

## Requirements

Install the required packages:

```bash
pip install -r requirements.txt
```

## Excel File Format

Your Excel file should have the following columns:
- **Name**: Student's full name
- **Stream**: Student's field of study (e.g., "Computer Engineering", "Mechanical Engineering")
- **Gender**: Student's gender (supports: Male/M/Female/F/Boy/Girl)

## Usage

### Option 1: Run the main script
```bash
python excel.py
```

### Option 2: Create sample data first (for testing)
```bash
python create_sample_data.py
python excel.py
```

## How it works

1. **Data Loading**: Reads your Excel file
2. **Filtering**: Identifies engineering and robotics students (looks for keywords: "engineering", "eng", "engineer", "robotics", "robot", "robotic")
3. **Gender Separation**: Separates students by gender
4. **Balanced Distribution**: Distributes students across groups to maintain gender balance
5. **Output**: Displays groups and optionally saves to Excel

## Example Output

```
STUDENT GROUPING PROGRAM
==============================
Enter the path to your Excel file: sample_students.xlsx
Successfully loaded 30 students from sample_students.xlsx

Original data columns: ['Name', 'Stream', 'Gender']
Total students: 30
Found 18 engineering students
Male students: 9
Female students: 9
Enter number of groups (default 2): 2

==================================================
BALANCED STUDENT GROUPS
==================================================

GROUP 1 (9 students):
------------------------------
Male: 5, Female: 4

Students:
  - John Smith (Computer Engineering) - Male
  - Emma Johnson (Mechanical Engineering) - Female
  ...

GROUP 2 (9 students):
------------------------------
Male: 4, Female: 5

Students:
  - Michael Brown (Electrical Engineering) - Male
  - Sarah Davis (Civil Engineering) - Female
  ...
```

## Supported Gender Formats

- Male: "Male", "M", "Boy"
- Female: "Female", "F", "Girl"

## Supported Engineering and Robotics Streams

The script recognizes any stream containing:
- **Engineering**: "engineering", "eng", "engineer"
- **Robotics**: "robotics", "robot", "robotic"

Examples: 
- Engineering: "Computer Engineering", "Mechanical Engineering", "Electrical Engineering"
- Robotics: "Robotics", "Robotics Engineering", "Robot Engineering", etc.

## Output Files

If you choose to save the results, the script creates an Excel file with:
- One sheet per group (Group_1, Group_2, etc.)
- Each sheet contains the student data for that group 