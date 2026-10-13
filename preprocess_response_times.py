import csv
from datetime import datetime
from collections import defaultdict

print("Processing 2024 response times across the dataset...")

global_stats = {m: [0.0, 0] for m in range(1, 13)}
zip_stats = defaultdict(lambda: {m: [0.0, 0] for m in range(1, 13)})

def parse_date(date_str):
    if not date_str or not date_str.strip():
        return None
    date_str = date_str.strip()
    for fmt in ('%m/%d/%Y %I:%M:%S %p', '%m/%d/%Y %H:%M:%S', '%m/%d/%Y', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d'):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None

filename = '311_Service_Requests_from_2010_to_Present_20250928.csv'

row_count = 0
matched_2024 = 0

with open(filename, mode='r', encoding='utf-8-sig', errors='replace') as f:
    reader = csv.DictReader(f)
    
    for row in reader:
        row_count += 1
        if row_count % 3000000 == 0:
            print(f"Scanned {row_count:,} rows... (Matched 2024: {matched_2024:,})")
            
        row_clean = {k.strip(): v for k, v in row.items() if k is not None}
        
        created_str = row_clean.get('Created Date', '')
        if '2024' not in created_str:
            continue
            
        closed_str = row_clean.get('Closed Date', '')
        if not closed_str or not closed_str.strip():
            continue
            
        zip_code = row_clean.get('Incident Zip', '')
        if not zip_code or not zip_code.strip():
            continue
            
        created_dt = parse_date(created_str)
        if not created_dt or created_dt.year != 2024:
            continue
            
        closed_dt = parse_date(closed_str)
        if not closed_dt:
            continue
            
        duration_hours = (closed_dt - created_dt).total_seconds() / 3600.0
        if duration_hours < 0:
            continue
            
        matched_2024 += 1
        month = created_dt.month
        
        global_stats[month][0] += duration_hours
        global_stats[month][1] += 1
        
        zip_clean = zip_code.strip().zfill(5)[:5]
        zip_stats[zip_clean][month][0] += duration_hours
        zip_stats[zip_clean][month][1] += 1

print(f"Finished scanning. Total 2024 closed incidents matched: {matched_2024:,}")
print("Writing output to 'zip_response_times_2020.csv'...")

# We keep the filename 'zip_response_times_2020.csv' so create_dashboard.py works seamlessly without changes
with open('zip_response_times_2020.csv', mode='w', newline='', encoding='utf-8') as out_f:
    writer = csv.writer(out_f)
    writer.writerow(['Zipcode', 'Month', 'duration_hours'])
    
    for m in range(1, 13):
        total_sum, count = global_stats[m]
        avg = (total_sum / count) if count > 0 else 0.0
        writer.writerow(['ALL', m, avg])
        
    for z, months_dict in zip_stats.items():
        for m in range(1, 13):
            total_sum, count = months_dict[m]
            if count > 0:
                avg = total_sum / count
                writer.writerow([z, m, avg])

print("Preprocessing complete! Saved summary to 'zip_response_times_2020.csv'.")
