import csv
from collections import Counter
import matplotlib.pyplot as plt

print("Analyzing 2024 urban rodent and property complaints...")

filename = '311_Service_Requests_from_2010_to_Present_20250928.csv'
location_counter = Counter()
row_count = 0
matched_count = 0

with open(filename, mode='r', encoding='utf-8-sig', errors='replace') as f:
    reader = csv.DictReader(f)
    headers = reader.fieldnames
    
    complaint_type_col = next((h for h in headers if 'Complaint Type' in h), 'Complaint Type')
    location_type_col = next((h for h in headers if 'Location Type' in h), 'Location Type')
    created_date_col = next((h for h in headers if 'Created Date' in h), 'Created Date')

    for row in reader:
        row_count += 1
        if row_count % 3000000 == 0:
            print(f"Processed {row_count:,} rows... (Matched rodents: {matched_count:,})")
            
        date_str = row.get(created_date_col, '').strip()
        if len(date_str) >= 10 and date_str[6:10] == '2024':
            c_type = row.get(complaint_type_col, '').strip()
            # Filter for rodent-related complaints
            if 'Rodent' in c_type:
                loc_type = row.get(location_type_col, '').strip() or 'Unspecified'
                location_counter[loc_type] += 1
                matched_count += 1

print(f"Finished processing. Total 2024 rodent complaints matched: {matched_count:,}")

if not location_counter:
    print("Error: No rodent complaint data found for 2024!")
    exit(1)

# Get top 8 location types for clear visualization
top_locations = location_counter.most_common(8)
loc_names = [item[0] for item in top_locations][::-1]
loc_counts = [item[1] for item in top_locations][::-1]

print("Generating Task 2 visualization...")
plt.figure(figsize=(11, 6))
bars = plt.barh(loc_names, loc_counts, color='#2b5c8f', edgecolor='black', alpha=0.85)

plt.title('Top 2024 NYC Location Types for Rodent Complaints', fontsize=14, fontweight='bold')
plt.xlabel('Number of Complaints', fontsize=12)
plt.ylabel('Location / Property Type', fontsize=12)
plt.grid(axis='x', linestyle='--', alpha=0.6)

# Add value labels on bars
for bar in bars:
    width = bar.get_width()
    plt.text(width + (max(loc_counts)*0.01), bar.get_y() + bar.get_height()/2, 
             f'{width:,}', va='center', fontsize=10, fontweight='semibold')

plt.tight_layout()
output_filename = 'task2_plot.png'
plt.savefig(output_filename, dpi=300)
print(f"Plot saved successfully as '{output_filename}'!")
