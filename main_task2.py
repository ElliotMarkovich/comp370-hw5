# main_task2.py
import csv
from collections import Counter
import matplotlib.pyplot as plt

def load_2024_rodent_data(filename):
    """Parses the master CSV and yields 2024 rodent complaint location types."""
    with open(filename, mode='r', encoding='utf-8-sig', errors='replace') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        
        complaint_type_col = next((h for h in headers if 'Complaint Type' in h), 'Complaint Type')
        location_type_col = next((h for h in headers if 'Location Type' in h), 'Location Type')
        created_date_col = next((h for h in headers if 'Created Date' in h), 'Created Date')

        for row in reader:
            date_str = row.get(created_date_col, '').strip()
            if len(date_str) >= 10 and date_str[6:10] == '2024':
                c_type = row.get(complaint_type_col, '').strip()
                if 'Rodent' in c_type:
                    loc_type = row.get(location_type_col, '').strip() or 'Unspecified'
                    yield loc_type

def aggregate_rodent_locations(data_generator, top_n=8):
    """Aggregates rodent complaints by top location/property types."""
    location_counter = Counter(data_generator)
    return location_counter.most_common(top_n)

def plot_rodent_locations(top_locations, output_filename='task2_plot.png'):
    """Generates and saves the horizontal bar chart for rodent location types."""
    loc_names = [item[0] for item in top_locations][::-1]
    loc_counts = [item[1] for item in top_locations][::-1]

    plt.figure(figsize=(11, 6))
    bars = plt.barh(loc_names, loc_counts, color='#2b5c8f', edgecolor='black', alpha=0.85)

    plt.title('Top 2024 NYC Location Types for Rodent Complaints', fontsize=14, fontweight='bold')
    plt.xlabel('Number of Complaints', fontsize=12)
    plt.ylabel('Location / Property Type', fontsize=12)
    plt.grid(axis='x', linestyle='--', alpha=0.6)

    for bar in bars:
        width = bar.get_width()
        plt.text(width + (max(loc_counts)*0.01), bar.get_y() + bar.get_height()/2, 
                 f'{width:,}', va='center', fontsize=10, fontweight='bold')

    plt.tight_layout()
    plt.savefig(output_filename, dpi=300)
    plt.close()
    print(f"Refactored Task 2 plot saved successfully as '{output_filename}'!")

def main():
    filename = '311_Service_Requests_from_2010_to_Present_20250928.csv'
    print("Executing modular pipeline for Task 2...")
    
    data_gen = load_2024_rodent_data(filename)
    top_locations = aggregate_rodent_locations(data_gen, top_n=8)
    plot_rodent_locations(top_locations, output_filename='task2_plot.png')
    
    print("Task 2 pipeline execution complete.")

if __name__ == '__main__':
    main()
