import csv
from collections import defaultdict
from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.layouts import column

print("Preparing data for Bokeh dashboard...")

# We can aggregate top complaints across boroughs using your filtered data or jan_feb_counts.
# Let's read from jan_feb_counts.csv or aggregate a quick top summary safely.
boroughs = []
complaint_types = set()
data_store = defaultdict(lambda: defaultdict(int))

# Let's read your existing jan_feb_counts.csv (or we can aggregate from filtered data)
# jan_feb_counts.csv format: complaint type, borough, count
with open('jan_feb_counts.csv', mode='r', encoding='utf-8', errors='replace') as f:
    reader = csv.DictReader(f)
    for row in reader:
        c_type = row['complaint type']
        borough = row['borough']
        count = int(row['count'])
        data_store[c_type][borough] = count
        complaint_types.add(c_type)

# Get top 5 most frequent complaint types overall for a clean dashboard view
top_complaints = sorted(complaint_types, key=lambda c: sum(data_store[c].values()), reverse=True)[:5]
all_boroughs = sorted(list(set(b for c in top_complaints for b in data_store[c].keys())))

# Format data for Bokeh ColumnDataSource
# Structure: x = boroughs, and keys for each top complaint type
source_data = {'boroughs': all_boroughs}
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

legend_items = []
for i, complaint in enumerate(top_complaints):
    counts = [data_store[complaint].get(b, 0) for b in all_boroughs]
    source_data[complaint] = counts

source = ColumnDataSource(data=source_data)

# Create Bokeh Figure
p = figure(x_range=all_boroughs, height=500, width=800, 
           title="Top 5 311 Complaint Types by Borough (Jan-Feb 2024)",
           toolbar_location="above", tools="pan,wheel_zoom,box_zoom,reset,save")

# Add vertical bars for each top complaint type
renderers = []
for i, complaint in enumerate(top_complaints):
    r = p.vbar(x='boroughs', top=complaint, width=0.15, source=source,
               color=colors[i % len(colors)], legend_label=complaint)
    renderers.append(r)

# Styling the plot
p.xaxis.axis_label = "Borough"
p.yaxis.axis_label = "Number of Complaints"
p.xgrid.grid_line_color = None
p.legend.title = "Complaint Types"
p.legend.click_policy = "hide"  # Click legend items to toggle visibility!
p.title.text_font_size = '14pt'

# Add Hover Tool for interactivity
hover = HoverTool(tooltips=[
    ("Borough", "@boroughs"),
    ("Complaint", "$name"),
    ("Count", "@$name")
])
p.add_tools(hover)

# Output to HTML file
output_file("dashboard.html")
save(p)

print("Bokeh dashboard successfully created and saved as 'dashboard.html'!")
