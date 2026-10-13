import pandas as pd
from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource, Select, CustomJS
from bokeh.layouts import column

# Load pre-processed summary data
df = pd.read_csv('zip_response_times_2020.csv')

# Ensure all 12 months are represented for clean lines
months = list(range(1, 13))
month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Global baseline (ALL 2020 data)
all_data_avg = df[df['Zipcode'] == 'ALL'].set_index('Month')['duration_hours'].reindex(months).values

# Get list of available zipcodes
available_zips = sorted([str(z) for z in df['Zipcode'].unique() if z != 'ALL'])
default_zip1 = available_zips[0]
default_zip2 = available_zips[1] if len(available_zips) > 1 else available_zips[0]

def get_zip_data(zip_code):
    subset = df[df['Zipcode'] == str(zip_code)].set_index('Month')['duration_hours'].reindex(months)
    return subset.fillna(0).values

# Set up ColumnDataSource containing all series
source_data = {
    'month': month_names,
    'all_data': all_data_avg,
    'zip1_data': get_zip_data(default_zip1),
    'zip2_data': get_zip_data(default_zip2),
}
source = ColumnDataSource(data=source_data)

# Master lookup table embedded for JavaScript callback so it runs instantly (< 5s)
lookup_dict = {'ALL': list(all_data_avg)}
for z in available_zips:
    lookup_dict[z] = list(get_zip_data(z))

# Create Figure
p = figure(x_range=month_names, height=450, width=800,
           title="Monthly Average Incident Response Time (2020)",
           toolbar_location="above", tools="pan,wheel_zoom,box_zoom,reset,save")

p.line('month', 'all_data', source=source, line_width=3, color='gray', legend_label="ALL 2020 Data")
p.line('month', 'zip1_data', source=source, line_width=3, color='blue', legend_label=f"Zipcode: {default_zip1}")
p.line('month', 'zip2_data', source=source, line_width=3, color='orange', legend_label=f"Zipcode: {default_zip2}")

p.xaxis.axis_label = "Month"
p.yaxis.axis_label = "Average Create-to-Closed Time (Hours)"
p.legend.title = "Curves"
p.legend.click_policy = "hide"

# Dropdowns for Zipcode 1 and Zipcode 2
zip_select1 = Select(title="Select Zipcode 1:", value=default_zip1, options=available_zips)
zip_select2 = Select(title="Select Zipcode 2:", value=default_zip2, options=available_zips)

# JavaScript callback for instant updating (< 5 seconds requirement)
callback_code = """
    const lookup = lookup_data;
    const z1 = zip1_select.value;
    const z2 = zip2_select.value;
    
    const d1 = lookup[z1] || Array(12).fill(0);
    const d2 = lookup[z2] || Array(12).fill(0);
    
    source.data['zip1_data'] = d1;
    source.data['zip2_data'] = d2;
    source.change.emit();
    
    // Update legend labels dynamically if desired
    // (Handled visually via interactive UI)
"""

# Pass lookup dictionary safely into JS
from bokeh.models import CustomJS
callback = CustomJS(args=dict(source=source, zip1_select=zip_select1, zip2_select=zip_select2, lookup_data=lookup_dict), code=callback_code)

zip_select1.js_on_change('value', callback)
zip_select2.js_on_change('value', callback)

# Layout in a single column per instructions
layout = column(zip_select1, zip_select2, p)

output_file("dashboard.html")
save(layout)

print("Updated response-time Bokeh dashboard successfully created as 'dashboard.html'!")
