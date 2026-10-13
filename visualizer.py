# visualizer.py
import matplotlib.pyplot as plt

def plot_monthly_trends(aggregated_data, output_filename='task1_plot.png'):
    """Generates and saves the monthly trend line plot."""
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    plt.figure(figsize=(11, 6))
    for noise_type, counts in aggregated_data.items():
        plt.plot(months, counts, marker='o', linewidth=2, label=noise_type)

    plt.title('Monthly Trends of Top NYC Noise Complaints (2024)', fontsize=14, fontweight='bold')
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Number of Complaints', fontsize=12)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.legend(title='Complaint Type', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()

    plt.savefig(output_filename, dpi=300)
    plt.close()
    print(f"Refactored plot saved successfully as '{output_filename}'!")
