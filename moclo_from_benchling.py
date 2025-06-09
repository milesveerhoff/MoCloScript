import pandas as pd
import tkinter as tk
from tkinter import filedialog
import re

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

def get_base_pmyt_name(fragment_name):
    """Extracts the base pMYT name (e.g., pMYT029) from a fragment name like pMYT029_nan_URA3."""
    match = re.match(r"(pMYT\d+)", fragment_name)
    if match:
        return match.group(1)
    return None

def load_data_and_display_confirmation():
    global constructs_df, num_inserts, insert_locations, master_mix, construct_tubes, constructs, vol_h2o_list, vol_master_mix, vol_master_mix_per_reaction, myt_plate_wells

    # Load volume data from CSV files
    fragments = pd.read_csv(path_fragments)
    constructs_df = pd.read_csv(path_constructs)

    # --- Check for "pMYT" in fragment names ---
    fragment_names = fragments.iloc[:, 0].astype(str)
    has_pmyt = fragment_names.str.contains("pMYT").any()

    # Only use MYT_Parts_Data.csv if the checkbox is selected and pMYT fragments are present
    myt_locations = {}
    myt_plate_wells = {}
    if use_myt_var.get() and has_pmyt:
        myt_parts_df = pd.read_csv("MYT_Parts_Data.csv")
        myt_locations = dict(zip(myt_parts_df['Plasmid name'].astype(str), myt_parts_df['Plate position'].astype(str)))
        myt_plate_wells = {plasmid: well for plasmid, well in myt_locations.items()}

    # Remove unnecessary columns
    constructs_df.drop(columns=[col for col in constructs_df.columns if "Overhang" in col], inplace=True, errors='ignore')
    constructs_df.drop(columns=["Status"], inplace=True, errors='ignore')

    # Calculate the number of inserts
    num_inserts = len(fragments)

    # Define locations for non-pMYT fragments
    locations = [f"{chr(65 + i // 6)}{i % 6 + 1}" for i in range(24)]
    inserts = []
    insert_plate_map = {}  # Map fragment name to (plate, well)

    non_pmyt_idx = 0
    for i, frag_name in enumerate(fragment_names):
        base_pmyt = get_base_pmyt_name(frag_name)
        if use_myt_var.get() and base_pmyt and base_pmyt in myt_locations:
            insert_plate_map[frag_name] = ("myt_plate", myt_locations[base_pmyt])
            inserts.append(("myt_plate", myt_locations[base_pmyt]))
        else:
            insert_plate_map[frag_name] = ("tube_rack", locations[non_pmyt_idx])
            inserts.append(("tube_rack", locations[non_pmyt_idx]))
            non_pmyt_idx += 1

    remaining_locations = locations[non_pmyt_idx:]
    master_mix = remaining_locations[0]  # Use first remaining location for MM

    #Assign locations in thermocycler to constructs
    construct_tubes = [f"{chr(65 + i // 12)}{i % 12 + 1}" for i in range(len(constructs_df))]

    # Create a dictionary mapping insert names to their locations (well only, for script compatibility)
    insert_locations = {fragments.iloc[i, 0]: inserts[i] for i in range(num_inserts)}

    # Extract constructs as a list of lists and get construct names if available
    constructs = [row[1:].tolist() for _, row in constructs_df.iterrows()]
    
    if 'Name' in constructs_df.columns:
        construct_names = constructs_df['Name'].tolist()
    else:
        construct_names = [f"Construct {i+1}" for i in range(len(constructs))]

    # Calculate the volume of h2o needed for each construct to reach 50 uL after other volumes have been added
    vol_buffer = 5
    vol_assembly_mix = 1
    vol_per_insert = 1
    vol_h2o_list = [50 - (vol_buffer + vol_assembly_mix + len(construct)*vol_per_insert) for construct in constructs]

    # Calculate master mix volume per reaction and total
    # MM per reaction = buffer + assembly mix + h2o for that construct
    vol_master_mix_per_reaction = [vol_buffer + vol_assembly_mix + vol_h2o for vol_h2o in vol_h2o_list]
    vol_master_mix = sum(vol_master_mix_per_reaction)
    # Optionally add 5% excess
    vol_master_mix_total = int(vol_master_mix * 1.05 + 0.5)

    # Calculate total volumes of each reagent for the master mix (with 5% excess)
    n_reactions = len(constructs)
    buffer_total = vol_buffer * n_reactions * 1.05
    assembly_mix_total = vol_assembly_mix * n_reactions * 1.05
    h2o_total = sum(vol_h2o_list) * 1.05

    # Display the confirmation window, passing MM info and MYT info
    display_confirmation_window(
        constructs_df, num_inserts, insert_locations, construct_tubes, construct_names,
        vol_master_mix_per_reaction, vol_master_mix_total,
        buffer_total, assembly_mix_total, h2o_total,
        insert_plate_map
    )

def display_confirmation_window(
    constructs_df, num_inserts, insert_locations, construct_tubes, construct_names,
    vol_master_mix_per_reaction, vol_master_mix_total,
    buffer_total, assembly_mix_total, h2o_total,
    insert_plate_map
):
    global confirmation_window, file_name_entry, excess_entry
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

    # Bind mouse wheel to canvas scrolling
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    # Pack the canvas and scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Create a readable format for tube placements, including plate info for pMYT
    global tube_placements
    tube_placements = ""
    for insert, (plate, well) in insert_plate_map.items():
        if plate == "myt_plate":
            tube_placements += f"[{well}] (MYT Plate): {insert}, \n"
        else:
            tube_placements += f"[{well}] (Tube Rack): {insert}, \n"
    tube_placements += f"\n[{master_mix}]: Master Mix (MM), \n"
    tube_placements += "\nConstructs will be built at the following locations in the thermocycler module:\n"
    tube_placements += "\n".join([f"[{location}]: {construct_names[i]}, " for i, location in enumerate(construct_tubes)])

    # Display confirmation message with details (excluding MM info, now live above)
    confirmation_message = (
        f"Loaded {len(constructs_df)} constructs using {path_constructs} and\n"
        f"{num_inserts} fragments using {path_fragments}.\n\n"
        "Place reagents at their respective locations:\n\n"
        f"{tube_placements}\n\n"
        "Are you ready to generate the script?"
    )
    label_confirmation = tk.Label(scrollable_frame, text=confirmation_message, justify=tk.LEFT, wraplength=500)
    label_confirmation.pack(pady=10)

    # Input box for total reaction volume
    reaction_vol_label = tk.Label(scrollable_frame, text="Total reaction volume per construct (µL):")
    reaction_vol_label.pack(pady=5)
    reaction_vol_entry = tk.Entry(scrollable_frame)
    reaction_vol_entry.insert(0, "50")  # Default value
    reaction_vol_entry.pack(pady=5)

    # --- Excess percentage input and live update (moved below info) ---
    excess_label = tk.Label(scrollable_frame, text="Excess percentage for master mix (e.g., 5 for 5%):")
    excess_label.pack(pady=5)
    excess_entry = tk.Entry(scrollable_frame)
    excess_entry.insert(0, "5")  # Default value
    excess_entry.pack(pady=5)

    # Info label for master mix, to be updated live
    mm_info_var = tk.StringVar()
    def update_mm_info(*args):
        try:
            excess_percent = float(excess_entry.get())
        except Exception:
            excess_percent = 5.0
        try:
            reaction_vol = float(reaction_vol_entry.get())
        except Exception:
            reaction_vol = 50.0
        n_reactions = len(constructs)
        vol_buffer = 5
        vol_assembly_mix = 1
        vol_per_insert = 1
        vol_h2o_list = [
            reaction_vol - (vol_buffer + vol_assembly_mix + len(construct) * vol_per_insert)
            for construct in constructs
        ]
        vol_master_mix_per_reaction = [
            vol_buffer + vol_assembly_mix + vol_h2o for vol_h2o in vol_h2o_list
        ]
        vol_master_mix = sum(vol_master_mix_per_reaction)
        vol_master_mix_total = int(vol_master_mix * (1 + excess_percent / 100) + 0.5)
        buffer_total = vol_buffer * n_reactions * (1 + excess_percent / 100)
        assembly_mix_total = vol_assembly_mix * n_reactions * (1 + excess_percent / 100)
        h2o_total = sum(vol_h2o_list) * (1 + excess_percent / 100)
        mm_info_var.set(
            f"Master Mix per reaction: {vol_master_mix_per_reaction} uL\n"
            f"Total Master Mix (with {excess_percent:.1f}% excess): {vol_master_mix_total} uL\n\n"
            "Prepare the Master Mix with the following reagent volumes (including excess):\n"
            f"  Buffer: {buffer_total:.2f} uL\n"
            f"  Assembly Mix: {assembly_mix_total:.2f} uL\n"
            f"  Water: {h2o_total:.2f} uL"
        )
    excess_entry.bind("<KeyRelease>", update_mm_info)
    reaction_vol_entry.bind("<KeyRelease>", update_mm_info)
    update_mm_info()  # Initialize with default

    mm_info_label = tk.Label(scrollable_frame, textvariable=mm_info_var, justify=tk.LEFT, wraplength=500)
    mm_info_label.pack(pady=10)

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
    file_name_label = tk.Label(scrollable_frame, text="File will be saved in the same directory as this script, and overwrite files with the same name.\nSave as:")
    file_name_label.pack(pady=5)
    file_name_entry = tk.Entry(scrollable_frame)
    file_name_entry.insert(0, "saved_moclo_script.py")  # Default value
    file_name_entry.pack(pady=5)

    # Confirm button to generate the script
    confirm_button = tk.Button(
        scrollable_frame,
        text="Confirm",
        command=lambda: generate_script(
            file_name_entry, tc_temp_activation, tc_temp_inactivation, excess_entry, reaction_vol_entry
        )
    )
    confirm_button.pack(pady=20)

def generate_script(file_name_entry, tc_temp_activation, tc_temp_inactivation, excess_entry, reaction_vol_entry):
    file_name = file_name_entry.get()
    try:
        excess_percent = float(excess_entry.get())
    except Exception:
        excess_percent = 5.0  # fallback to default if invalid
    try:
        reaction_vol = float(reaction_vol_entry.get())
    except Exception:
        reaction_vol = 50.0  # fallback to default if invalid

    n_reactions = len(constructs)
    vol_buffer = 5
    vol_assembly_mix = 1
    vol_per_insert = 1
    # Use reaction_vol instead of 50
    vol_h2o_list = [
        reaction_vol - (vol_buffer + vol_assembly_mix + len(construct) * vol_per_insert)
        for construct in constructs
    ]
    vol_master_mix_per_reaction = [
        vol_buffer + vol_assembly_mix + vol_h2o for vol_h2o in vol_h2o_list
    ]
    vol_master_mix = sum(vol_master_mix_per_reaction)
    vol_master_mix_total = int(vol_master_mix * (1 + excess_percent / 100) + 0.5)
    buffer_total = vol_buffer * n_reactions * (1 + excess_percent / 100)
    assembly_mix_total = vol_assembly_mix * n_reactions * (1 + excess_percent / 100)
    h2o_total = sum(vol_h2o_list) * (1 + excess_percent / 100)

    num_master_mix_transfers = len(construct_tubes)
    num_insert_transfers = sum(len(construct) for construct in constructs)
    total_p20_tips = num_insert_transfers + sum(1 for v in vol_master_mix_per_reaction if v < 20)
    total_p300_tips = sum(1 for v in vol_master_mix_per_reaction if v >= 20)

    script = template_script.format(
        tube_placements=tube_placements,
        inserts=insert_locations,
        master_mix=master_mix,
        construct_tubes=construct_tubes,
        vol_master_mix_per_reaction=vol_master_mix_per_reaction,
        vol_per_insert=1,
        reaction_temp=tc_temp_activation.get(),
        inactivation_temp=tc_temp_inactivation.get(),
        constructs=constructs,
        total_p20_tips=total_p20_tips,
        total_p300_tips=total_p300_tips
    )

    with open(file_name, 'w') as file:
        file.write(script)

    print(f"Script generated successfully and saved as {file_name}.")
    confirmation_window.destroy()

# Initialize output variables
path_fragments = ""
path_constructs = ""

# Create the main window
root = tk.Tk()

# Add a variable to track the checkbox state
use_myt_var = tk.BooleanVar(value=False)

def on_myt_checkbox():
    if use_myt_var.get():
        handle_myt_toolkit_selected()
    else:
        handle_myt_toolkit_unselected()

def handle_myt_toolkit_selected():
    # Placeholder for your custom logic when MYT is selected
    print("Multiplex Yeast Toolkit option selected.")

def handle_myt_toolkit_unselected():
    # Placeholder for your custom logic when MYT is unselected
    print("Multiplex Yeast Toolkit option unselected.")

# Create labels and buttons to open the file dialogs
label_1 = tk.Label(root, text="Select Fragments CSV table from Benchling")
label_1.pack(pady=5)
select_button_1 = tk.Button(root, text="Select File", command=select_file_1)
select_button_1.pack(pady=5)
label_2 = tk.Label(root, text="Select Constructs CSV table from Benchling")
label_2.pack(pady=5)
select_button_2 = tk.Button(root, text="Select File", command=select_file_2)
select_button_2.pack(pady=5)

# Add the MYT checkbox
myt_checkbox = tk.Checkbutton(
    root,
    text="My constructs use plasmids from the Multiplex Yeast Toolkit",
    variable=use_myt_var,
    command=on_myt_checkbox
)
myt_checkbox.pack(pady=5)

# Accept button to close the window
accept_button = tk.Button(root, text="Accept", command=accept_files)
accept_button.pack(pady=20)

# Run the application
root.mainloop()