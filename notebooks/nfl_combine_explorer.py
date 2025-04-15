# -*- coding: utf-8 -*-
"""nfl_combine_explorer.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1KgGIk3e98_yljEcIPX0bQvlzSDRBRgyp
"""

# Commented out IPython magic to ensure Python compatibility.
# %run ../scripts/scraper.py  #adjust path if needed

import pandas as pd
import ipywidgets as widgets
from IPython.display import display, clear_output

from scripts.metrics import rate  #This is okay to import

# Prepare the dropdown options in the format "Player, School"
df['Dropdown_Label'] = df['Player'] + ', ' + df['School'].astype(str)
all_players = [''] + sorted(df['Dropdown_Label'].dropna().unique())

# Create an output widget to display the dynamic dropdown
output = widgets.Output()

# Create a text input for filtering
filter_input = widgets.Text(
    value='',
    description='Filter:',
    layout={'width': '50%', 'margin': '0 0 10px 0'}
)

# Create an initial dropdown (optional, can be hidden if not needed)
player_dropdown = widgets.Dropdown(
    options=[''],
    description='Select a player:',
    layout={'width': '50%'},
    style={'description_width': 'initial'}
)

# Function to update filtered results and create a dropdown
def on_filter_change(change):
    with output:
        clear_output()
        search_term = change['new'].strip()
        if search_term:
            search_term_lower = search_term.lower()
            filtered_df = df[df['Player'].str.lower().str.startswith(search_term_lower, na=False)][['Player', 'School']]
            if not filtered_df.empty:
                # Create dropdown options from filtered results
                filtered_labels = [''] + sorted(filtered_df['Player'] + ', ' + filtered_df['School'].astype(str))
                # Define a new dropdown for filtered results
                filtered_dropdown = widgets.Dropdown(
                    options=filtered_labels,
                    description='Select:',
                    layout={'width': '50%'},
                    style={'description_width': 'initial'}
                )
                # Define what happens when a selection is made
                def on_filtered_dropdown_change(change):
                    selected_label = change['new']
                    if selected_label:
                        player_name = selected_label.split(',')[0].strip()
                        filter_input.value = ''
                        with output:
                            clear_output()
                        rate(player_name)  # Call rate() with the selected player
                # Attach the handler to the filtered dropdown
                filtered_dropdown.observe(on_filtered_dropdown_change, names='value')
                # Display the filtered dropdown
                display(filtered_dropdown)
            else:
                print(f"No players found starting with '{search_term}'")
        else:
            print("Type a player's name to filter")

# Observe changes in the filter input
filter_input.observe(on_filter_change, names='value')

# Display the filter input and output
display(filter_input)
display(output)
