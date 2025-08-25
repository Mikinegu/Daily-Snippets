# CSV to Excel Automation using pandas
import pandas as pd

def csv_to_excel(csv_path, excel_path):
	# Read the CSV file
	df = pd.read_csv(csv_path)
	# Write to Excel file
	df.to_excel(excel_path, index=False)

if __name__ == "__main__":
	# Example usage
	csv_file = "sample.csv"  # Change to your CSV file path
	excel_file = "output.xlsx"  # Change to your desired Excel file path
	csv_to_excel(csv_file, excel_file)
