# hw6_task1_main.py
from data_loader import load_2024_noise_data
from analyzer import aggregate_monthly_noise
from visualizer import plot_monthly_trends

def main():
    filename = '311_Service_Requests_from_2010_to_Present_20250928.csv'
    print("Executing modular pipeline for Task 1...")
    
    data_gen = load_2024_noise_data(filename)
    aggregated_data = aggregate_monthly_noise(data_gen, top_n=5)
    plot_monthly_trends(aggregated_data, output_filename='task1_plot.png')
    
    print("Task 1 pipeline execution complete.")

if __name__ == '__main__':
    main()
