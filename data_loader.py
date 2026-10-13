# data_loader.py
import csv

def load_2024_noise_data(filename):
    """Parses the master CSV and yields 2024 noise complaint rows."""
    with open(filename, mode='r', encoding='utf-8-sig', errors='replace') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        
        complaint_type_col = next((h for h in headers if 'Complaint Type' in h), 'Complaint Type')
        created_date_col = next((h for h in headers if 'Created Date' in h), 'Created Date')

        for row in reader:
            date_str = row.get(created_date_col, '').strip()
            if len(date_str) >= 10 and date_str[6:10] == '2024':
                c_type = row.get(complaint_type_col, '').strip()
                if 'Noise' in c_type:
                    yield date_str, c_type
