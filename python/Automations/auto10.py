# CSV to Excel Automation using pandas

# Improved CSV to Excel Automation using pandas

import pandas as pd
import sys
import os
import glob
from datetime import datetime

def convert_folder_csvs_to_excel(folder_path, excel_path, log_path):
	csv_files = glob.glob(os.path.join(folder_path, '*.csv'))
	if not csv_files:
		print(f"No CSV files found in '{folder_path}'.")
		return
	with pd.ExcelWriter(excel_path) as writer:
		log_entries = []
		for csv_file in csv_files:
			try:
				df = pd.read_csv(csv_file)
				sheet_name = os.path.splitext(os.path.basename(csv_file))[0][:31]  # Excel sheet name max length 31
				df.to_excel(writer, sheet_name=sheet_name, index=False)
				log_entries.append(f"SUCCESS: {csv_file} -> {sheet_name}")
			except Exception as e:
				log_entries.append(f"FAIL: {csv_file} - {e}")
	# Write log
	with open(log_path, 'a', encoding='utf-8') as log_file:
		log_file.write(f"\nRun at {datetime.now()}\n")
		for entry in log_entries:
			log_file.write(entry + '\n')
	print(f"Conversion complete. See log: {log_path}")

if __name__ == "__main__":
	if len(sys.argv) != 4:
		print("Usage: python auto10.py <csv_folder> <output_excel> <log_file>")
	else:
		folder = sys.argv[1]
		excel_file = sys.argv[2]
		log_file = sys.argv[3]
		convert_folder_csvs_to_excel(folder, excel_file, log_file)
