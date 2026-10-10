import csv
from datetime import datetime
import matplotlib.pyplot as plt

print("Streaming dataset to count 'HEAT/HOT WATER' by month...")

# Target months we care about
target_months = {'2024-01': 0, '2024-02': 0, '2024-06': 0, '2024-07': 0}

def parse_month(date_str):
    for fmt in ('%m/%d/%Y %I:%M:%S %p', '%m/%d/%Y %H:%M:%S', '%m/%d/%Y'):
        try:
            dt = datetime.strptime(date_str.strip(), fmt)
            return dt.strftime('%Y-%m')
        except ValueError:
            continue
    return None

# Stream line-by-line to avoid OOM
with open('nyc_2024_filtered.csv', mode='r', encoding='utf-8', errors='replace') as f:
    reader = csv.DictReader(f)
    for row in reader:
        complaint = row.get('Complaint Type', '')
        if complaint == 'HEAT/HOT WATER':
            created_str = row.get('Created Date', '')
            ym = parse_month(created_str)
            if ym in target_months:
                target_months[ym] += 1

print("Counts found:", target_months)

# Plotting and saving to file
months_order = ['2024-01', '2024-02', '2024-06', '2024-07']
counts = [target_months[m] for m in months_order]

plt.figure(figsize=(9, 5))
ax = plt.bar(['January', 'February', 'June', 'July'], counts, color=['#2b5c8f', '#2b5c8f', '#d95f02', '#d95f02'])
plt.title("Monthly Comparison of 'HEAT/HOT WATER' Complaints (2024)", fontsize=13, fontweight='bold')
plt.xlabel("Month", fontsize=11)
plt.ylabel("Number of Incidents", fontsize=11)
plt.grid(axis='y', linestyle='--', alpha=0.7)

for bar in ax:
    height = bar.get_height()
    plt.annotate(f"{int(height):,}",
                 xy=(bar.get_x() + bar.get_width() / 2, height),
                 xytext=(0, 4), textcoords="offset points",
                 ha='center', va='bottom', fontsize=9, fontweight='semibold')

plt.tight_layout()
plt.savefig('complaint_comparison.png', dpi=300)
print("Chart saved successfully as 'complaint_comparison.png'!")
