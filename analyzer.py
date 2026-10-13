# analyzer.py
from collections import defaultdict

def aggregate_monthly_noise(data_generator, top_n=5):
    """Aggregates noise complaints by month for the top N complaint types."""
    noise_monthly = defaultdict(lambda: [0] * 12)
    
    for date_str, c_type in data_generator:
        try:
            month = int(date_str[:2])
            if 1 <= month <= 12:
                noise_monthly[c_type][month - 1] += 1
        except ValueError:
            continue
            
    # Select top N most frequent noise types
    top_noises = sorted(noise_monthly.keys(), key=lambda k: sum(noise_monthly[k]), reverse=True)[:top_n]
    
    filtered_data = {noise: noise_monthly[noise] for noise in top_noises}
    return filtered_data
