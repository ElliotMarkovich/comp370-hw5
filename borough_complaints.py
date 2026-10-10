#!/usr/bin/env python3
import argparse
import csv
from collections import defaultdict
from datetime import datetime

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="CLI tool to output complaint counts per complaint type and borough for a date range."
    )
    parser.add_argument("-i", "--input", required=True, help="Path to the input CSV file")
    parser.add_argument("-s", "--start", required=True, help="Start date (YYYY-MM-DD or similar string format matching data)")
    parser.add_argument("-e", "--end", required=True, help="End date (YYYY-MM-DD or similar string format matching data)")
    parser.add_argument("-o", "--output", help="Optional output CSV file path. If omitted, prints to stdout.")
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    # Dictionary to hold counts: counts[(complaint_type, borough)] = count
    counts = defaultdict(int)
    
    # Open and parse the CSV file line-by-line
    with open(args.input, mode="r", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            # Note: Depending on your exact column headers in the CSV, 
            # adapt 'Created Date', 'Complaint Type', and 'Borough' to match the dataset.
            created_date_str = row.get("Created Date", "").strip()
            complaint_type = row.get("Complaint Type", "").strip()
            borough = row.get("Borough", "").strip()
            
            if not created_date_str or not complaint_type or not borough:
                continue
                
            # Extract date portion (e.g., '2024-01-01' from '2024-01-01 12:30:00')
            # Adjust slicing or parsing based on how dates are formatted in your CSV file
            incident_date = created_date_str.split(" ")[0]
            
           # Filter by date range (lexicographical string comparison works if format is YYYY-MM-DD)
            if args.start <= incident_date <= args.end:
                counts[(complaint_type, borough)] += 1

    # Prepare output rows
    output_data = [["complaint type", "borough", "count"]]
    for (comp_type, bor), count in sorted(counts.items()):
        output_data.append([comp_type, bor, str(count)])
        
    # Write to file or stdout
    if args.output:
        with open(args.output, mode="w", newline="", encoding="utf-8") as out_f:
            writer = csv.writer(out_f)
            writer.writerows(output_data)
    else:
        for row in output_data:
            print(", ".join(row))

if __name__ == "__main__":
    main()
