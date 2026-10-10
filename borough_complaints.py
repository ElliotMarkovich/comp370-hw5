import csv
from datetime import datetime
import argparse

def parse_date(date_str):
    """Attempt to parse various common datetime formats from the NYC 311 CSV."""
    for fmt in ('%m/%d/%Y %I:%M:%S %p', '%m/%d/%Y %H:%M:%S', '%m/%d/%Y'):
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue
    return None

def main():
    parser = argparse.ArgumentParser(description="Aggregate 311 complaints by type and borough within a date range.")
    parser.add_argument('-i', '--input', required=True, help="Path to input CSV file")
    parser.add_argument('-s', '--start', required=True, help="Start date in YYYY-MM-DD format")
    parser.add_argument('-e', '--end', required=True, help="End date in YYYY-MM-DD format")
    parser.add_argument('-o', '--output', required=True, help="Path to output CSV file")
    args = parser.parse_args()

    # Parse start and end dates
    start_date = datetime.strptime(args.start, '%Y-%m-%d')
    # Extend end date to the end of the day so inclusive filtering works properly
    end_date = datetime.strptime(args.end, '%Y-%m-%d').replace(hour=23, minute=59, second=59)

    counts = {}

    with open(args.input, mode='r', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        for row in reader:
            created_str = row.get('Created Date', '')
            dt = parse_date(created_str)
            
            if dt and start_date <= dt <= end_date:
                complaint = row.get('Complaint Type', 'Unknown')
                borough = row.get('Borough', 'Unknown')
                key = (complaint, borough)
                counts[key] = counts.get(key, 0) + 1

    with open(args.output, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['complaint type', 'borough', 'count'])
        for (complaint, borough), count in counts.items():
            writer.writerow([complaint, borough, count])

if __name__ == '__main__':
    main()
