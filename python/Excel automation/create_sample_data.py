import pandas as pd
import random

def create_sample_data():
    """
    Create a sample Excel file with student data for testing
    """
    # Sample data
    names = [
        "John Smith", "Emma Johnson", "Michael Brown", "Sarah Davis", "David Wilson",
        "Lisa Anderson", "James Taylor", "Jennifer Martinez", "Robert Garcia", "Amanda Rodriguez",
        "William Lopez", "Michelle Gonzalez", "Christopher Perez", "Jessica Torres", "Daniel Moore",
        "Ashley Jackson", "Matthew Martin", "Nicole Lee", "Joshua Thompson", "Stephanie White",
        "Andrew Harris", "Rebecca Clark", "Ryan Lewis", "Laura Hall", "Kevin Young",
        "Kimberly Allen", "Brian King", "Heather Wright", "Steven Green", "Melissa Baker"
    ]
    
    streams = [
        "Computer Engineering", "Mechanical Engineering", "Electrical Engineering", 
        "Civil Engineering", "Chemical Engineering", "Biomedical Engineering",
        "Computer Science", "Mathematics", "Physics", "Chemistry", "Biology"
    ]
    
    genders = ["Male", "Female"]
    
    # Generate random student data
    data = []
    for i in range(30):
        student = {
            'Name': names[i],
            'Stream': random.choice(streams),
            'Gender': random.choice(genders)
        }
        data.append(student)
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save to Excel
    df.to_excel('sample_students.xlsx', index=False)
    print("Sample data created: sample_students.xlsx")
    print(f"Total students: {len(df)}")
    print(f"Engineering students: {len(df[df['Stream'].str.contains('Engineering', case=False)])}")
    print(f"Male students: {len(df[df['Gender'] == 'Male'])}")
    print(f"Female students: {len(df[df['Gender'] == 'Female'])}")

if __name__ == "__main__":
    create_sample_data() 