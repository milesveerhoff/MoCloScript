import pandas as pd
import tkinter as tk
from tkinter import filedialog

# Template script with placeholders
template_script = open("template_script.py").read()

def select_file_1():
    global path_fragments
    path_fragments = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if path_fragments:
        select_button_1.config(text=f"Selected: {path_fragments}")

def select_file_2():
    global path_constructs
    path_constructs = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if path_constructs:
        select_button_2.config(text=f"Selected: {path_constructs}")

def accept_files():
    root.destroy()
    load_data_and_display_confirmation()

def load_data_and_display_confirmation():
    global constructs_df, num_inserts, insert_locations, buffer, assembly_mix, h2o, construct_tubes, constructs, vol_h2o_list

    # Load volume data from CSV files
    fragments = pd.read_csv(path_fragments)
    constructs_df = pd.read_csv(path_constructs)

    # Remove unnecessary columns
    constructs_df.drop(columns=[col for col in constructs_df.columns if "Overhang" in col], inplace=True, errors='ignore')
    constructs_df.drop(columns=["Status"], inplace=True, errors='ignore')

    # Debugging: Print the dataframes
    print(fragments)
    print(constructs_df)

    # Calculate the number of inserts
    num_inserts = len(fragments)

    # Define locations based on the number of inserts
    locations = [f"{chr(65 + i // 6)}{i % 6 + 1}" for i in range(24)]
    inserts = locations[:num_inserts]
    remaining_locations = locations[num_inserts:]
    buffer = remaining_locations[0]
    assembly_mix = remaining_locations[1]
    h2o = remaining_locations[2]
    
    #Assign locations in thermocycler to constructs
    construct_tubes = [f"{chr(65 + i // 12)}{i % 12 + 1}" for i in range(len(constructs_df))]

    # Create a dictionary mapping insert names to their locations
    insert_locations = {fragments.iloc[i, 0]: inserts[i] for i in range(num_inserts)}

    # Extract constructs as a list of lists and get construct names if available
    constructs = [row[1:].tolist() for _, row in constructs_df.iterrows()]
    
    if 'Name' in constructs_df.columns:
        construct_names = constructs_df['Name'].tolist()
    else:
        construct_names = [f"Construct {i+1}" for i in range(len(constructs))]

    # Calculate the volume of h2o needed for each construct to reach 50 uL after other volumes have been added
    vol_h2o_list = [50 - 6 - len(construct) for construct in constructs]

    # Display the confirmation window
    display_confirmation_window(constructs_df, num_inserts, insert_locations, construct_tubes, construct_names)

def display_confirmation_window(constructs_df, num_inserts, insert_locations, construct_tubes, construct_names):
    global confirmation_window, file_name_entry
    confirmation_window = tk.Tk()
    confirmation_window.title("Confirm Placements")
    confirmation_window.configure(padx=20, pady=20)

    # Create a canvas and scrollbar for scrollable content
    canvas = tk.Canvas(confirmation_window)
    scrollbar = tk.Scrollbar(confirmation_window, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    # Configure the canvas to work with the scrollbar
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Pack the canvas and scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Create a readable format for tube placements
    global tube_placements
    tube_placements = (
        "\n".join([f"[{location}]: {insert}, " for insert, location in insert_locations.items()]) +
        f"\n\n[{buffer}]: Buffer, \n"
        f"[{assembly_mix}]: Assembly Mix, \n"
        f"[{h2o}]: Sterile DI Water, \n"
        "\nConstructs will be built at the following locations in the thermocycler module:\n" +
        "\n".join([f"[{location}]: {construct_names[i]}, " for i, location in enumerate(construct_tubes)])
    )

    # Display confirmation message with details
    confirmation_message = (
        f"Loaded {len(constructs_df)} constructs using {path_constructs} and\n"
        f"{num_inserts} fragments using {path_fragments}.\n\n"
        "Place the following tubes in their respective locations:\n\n"
        f"{tube_placements}\n\n"
        "Are you ready to generate the script?"
    )
    label_confirmation = tk.Label(scrollable_frame, text=confirmation_message, justify=tk.LEFT, wraplength=500)
    label_confirmation.pack(pady=10)

    # Input box for thermocycler temps
    tc_temp_label = tk.Label(scrollable_frame, text="Enter the Reaction and Inactivation temperatures (in °C) for thermocycler protocol:\n\nReaction Temp:")
    tc_temp_label.pack(pady=5)
    tc_temp_activation = tk.Entry(scrollable_frame)
    tc_temp_activation.insert(0, "37")  # Default value
    tc_temp_activation.pack(pady=5)
    tc_temp_label2 = tk.Label(scrollable_frame, text="Inactivation Temp:")
    tc_temp_label2.pack(pady=5)
    tc_temp_inactivation = tk.Entry(scrollable_frame)
    tc_temp_inactivation.insert(0, "65")  # Default value
    tc_temp_inactivation.pack(pady=5)

    # Input box for file name with default value
    file_name_label = tk.Label(scrollable_frame, text="File will be saved in the same directory as this script, and overwrite files with the same name.\nEnter name to save file as:")
    file_name_label.pack(pady=5)
    file_name_entry = tk.Entry(scrollable_frame)
    file_name_entry.insert(0, "saved_moclo_script.py")  # Default value
    file_name_entry.pack(pady=5)

    # Confirm button to generate the script
    confirm_button = tk.Button(scrollable_frame, text="Confirm", command=lambda: generate_script(file_name_entry, tc_temp_activation, tc_temp_inactivation))
    confirm_button.pack(pady=20)

def generate_script(file_name_entry, tc_temp_activation, tc_temp_inactivation):
    # Get the file name from the input box
    file_name = file_name_entry.get()

    # Fill in the template for the output protocol
    script = template_script.format(
        tube_placements=tube_placements,
        inserts=insert_locations,
        buffer=buffer,
        assembly_mix=assembly_mix,
        h2o=h2o,
        construct_tubes=construct_tubes,
        vol_h2o=vol_h2o_list,
        vol_per_insert=1,
        reaction_temp=tc_temp_activation.get(),
        inactivation_temp=tc_temp_inactivation.get(),
        constructs=constructs
    )

    # Save the generated script to the specified file
    with open(file_name, 'w') as file:
        file.write(script)

    print(f"Script generated successfully and saved as {file_name}.")
    confirmation_window.destroy()

# Initialize output variables
path_fragments = ""
path_constructs = ""

# Create the main window
root = tk.Tk()
root.title("File Input")
# root.geometry("600x300") # Optional: Set window size
root.configure(padx=20, pady=20)

# Create labels and buttons to open the file dialogs
label_1 = tk.Label(root, text="Select Fragments CSV table from Benchling")
label_1.pack(pady=5)
select_button_1 = tk.Button(root, text="Select File", command=select_file_1)
select_button_1.pack(pady=5)
label_2 = tk.Label(root, text="Select Constructs CSV table from Benchling")
label_2.pack(pady=5)
select_button_2 = tk.Button(root, text="Select File", command=select_file_2)
select_button_2.pack(pady=5)

# Accept button to close the window
accept_button = tk.Button(root, text="Accept", command=accept_files)
accept_button.pack(pady=20)

# Run the application
root.mainloop()