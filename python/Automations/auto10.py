# CSV to Excel Automation using pandas

# Improved CSV to Excel Automation using pandas
import pandas as pd
import sys
import os

def csv_to_excel(csv_path, excel_path):
	try:
		if not os.path.exists(csv_path):
			print(f"Error: CSV file '{csv_path}' does not exist.")
			return
		df = pd.read_csv(csv_path)
		df.to_excel(excel_path, index=False)
		print(f"Successfully converted '{csv_path}' to '{excel_path}'.")
	except Exception as e:
		print(f"Conversion failed: {e}")

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("Usage: python auto10.py <input_csv> <output_excel>")
	else:
		csv_file = sys.argv[1]
		excel_file = sys.argv[2]
		csv_to_excel(csv_file, excel_file)
