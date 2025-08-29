# CSV to Excel Automation using pandas

# Improved CSV to Excel Automation using pandas


import pandas as pd
import sys
import os
import glob
from datetime import datetime
from tqdm import tqdm
import time

def convert_folder_csvs_to_excel(folder_path, excel_path, log_path, filter_keyword=None, delimiter=',', encoding='utf-8'):
	csv_files = glob.glob(os.path.join(folder_path, '*.csv'))
	if not csv_files:
		print(f"No CSV files found in '{folder_path}'.")
		return
	with pd.ExcelWriter(excel_path) as writer:
		log_entries = []
		for csv_file in tqdm(csv_files, desc="Converting CSVs", unit="file"):
			max_retries = 3
			for attempt in range(max_retries):
				try:
					df = pd.read_csv(csv_file, delimiter=delimiter, encoding=encoding)
					if filter_keyword:
						filtered_cols = [col for col in df.columns if filter_keyword.lower() in col.lower()]
						if filtered_cols:
							df = df[filtered_cols]
					sheet_name = os.path.splitext(os.path.basename(csv_file))[0][:31]  # Excel sheet name max length 31
					df.to_excel(writer, sheet_name=sheet_name, index=False)
					log_entries.append(f"SUCCESS: {csv_file} -> {sheet_name} | Rows: {df.shape[0]}, Cols: {df.shape[1]}")
					break  # Success, exit retry loop
				except Exception as e:
					if attempt < max_retries - 1:
						time.sleep(1)  # Wait 1 second before retry
					else:
						log_entries.append(f"FAIL: {csv_file} - {e} (after {max_retries} attempts)")
	# Write log
	with open(log_path, 'a', encoding='utf-8') as log_file:
		log_file.write(f"\nRun at {datetime.now()}\n")
		for entry in log_entries:
			log_file.write(entry + '\n')
	print(f"Conversion complete. See log: {log_path}")

def interactive_mode():
	print("Interactive CSV to Excel Converter")
	folder = input("Enter folder containing CSV files: ").strip()
	excel_file = input("Enter output Excel file name (e.g., output.xlsx): ").strip()
	log_file = input("Enter log file name (e.g., conversion.log): ").strip()
	filter_keyword = input("Enter column filter keyword (optional, press Enter to skip): ").strip()
	filter_keyword = filter_keyword if filter_keyword else None
	delimiter = input("Enter CSV delimiter (default is comma ','): ").strip()
	delimiter = delimiter if delimiter else ','
	encoding = input("Enter file encoding (default is utf-8): ").strip()
	encoding = encoding if encoding else 'utf-8'
	convert_folder_csvs_to_excel(folder, excel_file, log_file, filter_keyword, delimiter, encoding)

if __name__ == "__main__":
	if len(sys.argv) == 1:
		interactive_mode()
	elif 4 <= len(sys.argv) <= 6:
		folder = sys.argv[1]
		excel_file = sys.argv[2]
		log_file = sys.argv[3]
		filter_keyword = sys.argv[4] if len(sys.argv) > 4 else None
		delimiter = sys.argv[5] if len(sys.argv) > 5 else ','
		encoding = sys.argv[6] if len(sys.argv) > 6 else 'utf-8'
		convert_folder_csvs_to_excel(folder, excel_file, log_file, filter_keyword, delimiter, encoding)
	else:
		print("Usage: python auto10.py <csv_folder> <output_excel> <log_file> [filter_keyword] [delimiter] [encoding]")
