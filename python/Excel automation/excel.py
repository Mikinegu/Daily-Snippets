import pandas as pd
import random
from collections import defaultdict

def read_student_data(file_path):
    """
    Read student data from Excel file
    Expected columns: Name, Stream, Gender
    """
    try:
        # Try to read the Excel file
        df = pd.read_excel(file_path)
        print(f"Successfully loaded {len(df)} students from {file_path}")
        
        # Show the first few rows to debug
        print(f"\nFirst few rows of your data:")
        print(df.head())
        print(f"\nColumn names: {list(df.columns)}")
        
        # Check if required columns exist
        required_columns = ['Name', 'Stream', 'Gender']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"⚠️  WARNING: Missing required columns: {missing_columns}")
            print(f"Available columns in your file: {list(df.columns)}")
            print("\nPlease ensure your Excel file has these columns:")
            print("- Name: Student's full name")
            print("- Stream: Student's field of study")
            print("- Gender: Student's gender (Male/Female/M/F/Boy/Girl)")
            
            # Try to suggest column mapping
            print("\n🔍 Column mapping suggestions:")
            for col in df.columns:
                if 'name' in col.lower():
                    print(f"  '{col}' might be the Name column")
                elif 'stream' in col.lower() or 'course' in col.lower() or 'field' in col.lower():
                    print(f"  '{col}' might be the Stream column")
                elif 'gender' in col.lower() or 'sex' in col.lower():
                    print(f"  '{col}' might be the Gender column")
            
            return None
        
        return df
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def filter_engineering_and_robotics_students(df):
    """
    Filter students to only include engineering and robotics students
    """
    # Convert stream column to lowercase for case-insensitive matching
    df['Stream_Lower'] = df['Stream'].str.lower()
    
    # Filter for engineering and robotics students (various possible spellings)
    engineering_keywords = ['engineering', 'eng', 'engineer']
    robotics_keywords = ['robotics', 'robot', 'robotic']
    
    # Separate engineering and robotics students
    engineering_mask = df['Stream_Lower'].str.contains('|'.join(engineering_keywords), na=False)
    robotics_mask = df['Stream_Lower'].str.contains('|'.join(robotics_keywords), na=False)
    
    engineering_students = df[engineering_mask].copy()
    robotics_students = df[robotics_mask].copy()
    
    # Remove the temporary column
    engineering_students = engineering_students.drop('Stream_Lower', axis=1)
    robotics_students = robotics_students.drop('Stream_Lower', axis=1)
    
    print(f"Found {len(engineering_students)} engineering students")
    print(f"Found {len(robotics_students)} robotics students")
    
    return engineering_students, robotics_students

def create_balanced_groups(students, num_groups=2):
    """
    Create balanced groups based on gender
    """
    if len(students) == 0:
        print("No students to group!")
        return []
    
    # Separate students by gender
    male_students = students[students['Gender'].str.lower().isin(['male', 'm', 'boy'])].copy()
    female_students = students[students['Gender'].str.lower().isin(['female', 'f', 'girl'])].copy()
    
    print(f"Male students: {len(male_students)}")
    print(f"Female students: {len(female_students)}")
    
    # Shuffle students for random distribution
    male_students = male_students.sample(frac=1).reset_index(drop=True)
    female_students = female_students.sample(frac=1).reset_index(drop=True)
    
    # Initialize groups
    groups = [[] for _ in range(num_groups)]
    
    # Distribute male students
    for i, student in male_students.iterrows():
        group_index = i % num_groups
        groups[group_index].append(student)
    
    # Distribute female students
    for i, student in female_students.iterrows():
        group_index = i % num_groups
        groups[group_index].append(student)
    
    return groups

def display_groups(groups):
    """
    Display the created groups
    """
    print("\n" + "="*50)
    print("BALANCED STUDENT GROUPS")
    print("="*50)
    
    for i, group in enumerate(groups, 1):
        print(f"\nGROUP {i} ({len(group)} students):")
        print("-" * 30)
        
        # Count gender distribution in this group
        male_count = sum(1 for student in group if str(student['Gender']).lower() in ['male', 'm', 'boy'])
        female_count = sum(1 for student in group if str(student['Gender']).lower() in ['female', 'f', 'girl'])
        
        print(f"Male: {male_count}, Female: {female_count}")
        print("\nStudents:")
        
        for student in group:
            print(f"  - {student['Name']} ({student['Stream']}) - {student['Gender']}")

def display_separate_groups(engineering_groups, robotics_groups):
    """
    Display engineering and robotics groups separately
    """
    print("\n" + "="*60)
    print("ENGINEERING STUDENT GROUPS")
    print("="*60)
    
    for i, group in enumerate(engineering_groups, 1):
        print(f"\nENGINEERING GROUP {i} ({len(group)} students):")
        print("-" * 40)
        
        # Count gender distribution in this group
        male_count = sum(1 for student in group if str(student['Gender']).lower() in ['male', 'm', 'boy'])
        female_count = sum(1 for student in group if str(student['Gender']).lower() in ['female', 'f', 'girl'])
        
        print(f"Male: {male_count}, Female: {female_count}")
        print("\nStudents:")
        
        for student in group:
            print(f"  - {student['Name']} ({student['Stream']}) - {student['Gender']}")
    
    print("\n" + "="*60)
    print("ROBOTICS STUDENT GROUPS")
    print("="*60)
    
    for i, group in enumerate(robotics_groups, 1):
        print(f"\nROBOTICS GROUP {i} ({len(group)} students):")
        print("-" * 40)
        
        # Count gender distribution in this group
        male_count = sum(1 for student in group if str(student['Gender']).lower() in ['male', 'm', 'boy'])
        female_count = sum(1 for student in group if str(student['Gender']).lower() in ['female', 'f', 'girl'])
        
        print(f"Male: {male_count}, Female: {female_count}")
        print("\nStudents:")
        
        for student in group:
            print(f"  - {student['Name']} ({student['Stream']}) - {student['Gender']}")

def save_groups_to_excel(groups, output_file="student_groups.xlsx"):
    """
    Save groups to Excel file
    """
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        for i, group in enumerate(groups, 1):
            if group:
                group_df = pd.DataFrame(group)
                group_df.to_excel(writer, sheet_name=f'Group_{i}', index=False)
    
    print(f"\nGroups saved to {output_file}")

def save_separate_groups_to_excel(engineering_groups, robotics_groups, output_file="student_groups.xlsx"):
    """
    Save engineering and robotics groups to Excel file with separate sheets
    """
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Save engineering groups
        for i, group in enumerate(engineering_groups, 1):
            if group:
                group_df = pd.DataFrame(group)
                group_df.to_excel(writer, sheet_name=f'Engineering_Group_{i}', index=False)
        
        # Save robotics groups
        for i, group in enumerate(robotics_groups, 1):
            if group:
                group_df = pd.DataFrame(group)
                group_df.to_excel(writer, sheet_name=f'Robotics_Group_{i}', index=False)
    
    print(f"\nGroups saved to {output_file}")
    print(f"  - Engineering Groups: {len([g for g in engineering_groups if g])}")
    print(f"  - Robotics Groups: {len([g for g in robotics_groups if g])}")

def create_template_excel():
    """
    Create a template Excel file with the correct format
    """
    template_data = {
        'Name': ['John Smith', 'Emma Johnson', 'Michael Brown', 'Sarah Davis', 'Alex Chen', 'Lisa Wang'],
        'Stream': ['Computer Engineering', 'Mechanical Engineering', 'Robotics', 'Electrical Engineering', 'Robotics Engineering', 'Civil Engineering'],
        'Gender': ['Male', 'Female', 'Male', 'Female', 'Male', 'Female']
    }
    
    df = pd.DataFrame(template_data)
    template_file = 'student_template.xlsx'
    df.to_excel(template_file, index=False)
    print(f"✅ Template file created: {template_file}")
    print("Please fill in your student data using this template.")

def rename_columns(df):
    """
    Allow user to rename columns if they have different names
    """
    print("\n🔧 Column Renaming Tool")
    print("If your columns have different names, you can rename them here.")
    
    current_columns = list(df.columns)
    print(f"Current columns: {current_columns}")
    
    # Define the required column names
    required_columns = ['Name', 'Stream', 'Gender']
    
    # Create a mapping dictionary
    column_mapping = {}
    
    for required_col in required_columns:
        print(f"\nWhich column should be '{required_col}'?")
        print("Available columns:", current_columns)
        
        while True:
            choice = input(f"Enter column name for '{required_col}' (or press Enter to skip): ").strip()
            if choice == "":
                break
            elif choice in current_columns:
                column_mapping[choice] = required_col
                current_columns.remove(choice)  # Remove from available options
                break
            else:
                print(f"❌ Column '{choice}' not found. Available columns: {current_columns}")
    
    if column_mapping:
        df_renamed = df.rename(columns=column_mapping)
        print(f"✅ Columns renamed: {column_mapping}")
        return df_renamed
    else:
        print("No columns were renamed.")
        return df

def main():
    """
    Main function to run the student grouping program
    """
    print("STUDENT GROUPING PROGRAM")
    print("="*30)
    
    # Check if user wants to create a template
    create_template = input("Do you want to create a template Excel file first? (y/n): ").lower()
    if create_template in ['y', 'yes']:
        create_template_excel()
        print("\nPlease fill in the template with your student data, then run this script again.")
        return
    
    # Get file path from user
    file_path = input("Enter the path to your Excel file: ").strip()
    
    # Read student data
    df = read_student_data(file_path)
    if df is None:
        return
    
    # Check if we need to rename columns
    required_columns = ['Name', 'Stream', 'Gender']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        print(f"\n⚠️  Some required columns are missing: {missing_columns}")
        rename_choice = input("Do you want to rename your existing columns to match the required format? (y/n): ").lower()
        if rename_choice in ['y', 'yes']:
            df = rename_columns(df)
            # Check again after renaming
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                print(f"❌ Still missing required columns: {missing_columns}")
                return
        else:
            print("❌ Cannot proceed without the required columns.")
            return
    
    # Display original data
    print(f"\nOriginal data columns: {list(df.columns)}")
    print(f"Total students: {len(df)}")
    
    # Filter for engineering and robotics students
    engineering_students, robotics_students = filter_engineering_and_robotics_students(df)
    
    if len(engineering_students) == 0 and len(robotics_students) == 0:
        print("No engineering or robotics students found!")
        return
    
    # Get number of groups for each stream
    try:
        engineering_groups = int(input("Enter number of engineering groups (default 2): ") or "2")
        robotics_groups = int(input("Enter number of robotics groups (default 2): ") or "2")
    except ValueError:
        engineering_groups = 2
        robotics_groups = 2
    
    # Create balanced groups for each stream
    engineering_group_list = create_balanced_groups(engineering_students, engineering_groups) if len(engineering_students) > 0 else []
    robotics_group_list = create_balanced_groups(robotics_students, robotics_groups) if len(robotics_students) > 0 else []
    
    # Display groups separately
    display_separate_groups(engineering_group_list, robotics_group_list)
    
    # Save to Excel
    save_choice = input("\nDo you want to save groups to Excel? (y/n): ").lower()
    if save_choice in ['y', 'yes']:
        output_file = input("Enter output filename (default: student_groups.xlsx): ").strip()
        if not output_file:
            output_file = "student_groups.xlsx"
        save_separate_groups_to_excel(engineering_group_list, robotics_group_list, output_file)

if __name__ == "__main__":
    main()
