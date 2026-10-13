import csv
from collections import defaultdict
import matplotlib.pyplot as plt

noise_monthly = defaultdict(lambda: [0] * 12)

filename = '311_Service_Requests_from_2010_to_Present_20250928.csv'

print("Scanning master dataset for 2024 noise complaints...")
row_count = 0
matched_count = 0

with open(filename, mode='r', encoding='utf-8-sig', errors='replace') as f:
    reader = csv.DictReader(f)
    headers = reader.fieldnames
    
    complaint_type_col = next((h for h in headers if 'Complaint Type' in h), 'Complaint Type')
    created_date_col = next((h for h in headers if 'Created Date' in h), 'Created Date')

    for row in reader:
        row_count += 1
        if row_count % 3000000 == 0:
            print(f"Processed {row_count:,} rows... (Matched 2024 noise: {matched_count:,})")
            
        date_str = row.get(created_date_col, '').strip()
        # Check if 2024 is the year (position 6 to 10 in MM/DD/YYYY format)
        if len(date_str) >= 10 and date_str[6:10] == '2024':
            c_type = row.get(complaint_type_col, '').strip()
            if 'Noise' in c_type:
                try:
                    month = int(date_str[:2])
                    if 1 <= month <= 12:
                        noise_monthly[c_type][month - 1] += 1
                        matched_count += 1
                except ValueError:
                    continue

print(f"Finished processing. Total 2024 noise complaints matched: {matched_count:,}")

if not noise_monthly:
    print("Error: No 2024 noise data found!")
    exit(1)

print("Generating visualization...")
top_noises = sorted(noise_monthly.keys(), key=lambda k: sum(noise_monthly[k]), reverse=True)[:5]
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

plt.figure(figsize=(11, 6))
for noise_type in top_noises:
    plt.plot(months, noise_monthly[noise_type], marker='o', linewidth=2, label=noise_type)

plt.title('Monthly Trends of Top NYC Noise Complaints (2024)', fontsize=14, fontweight='bold')
plt.xlabel('Month', fontsize=12)
plt.ylabel('Number of Complaints', fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.legend(title='Complaint Type', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()

output_filename = 'task1_plot.png'
plt.savefig(output_filename, dpi=300)
print(f"Plot saved successfully as '{output_filename}'!")
