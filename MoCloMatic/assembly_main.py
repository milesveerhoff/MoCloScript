import pandas as pd
import tkinter as tk
from tkinter import filedialog
import re
import tkinter.font as tkfont

def safe_float(entry, default=1.0):
    try:
        val = entry.get()
        return float(val) if val.strip() != "" else default
    except Exception:
        return default

# Template script with placeholders
template = open("template.py").read()

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
    global constructs_df, num_inserts, insert_locations, master_mix, construct_tubes, constructs, vol_per_insert_dict, toolkit_plate_wells, water_loc

    # Load volume data from CSV files
    fragments = pd.read_csv(path_fragments)
    constructs_df = pd.read_csv(path_constructs)

    # Extract Bin values for each insert (assumes columns: [Name, ..., Bin, ...])
    bin_dict = dict(zip(fragments.iloc[:, 0], fragments["Bin"]))

    # --- Check for toolkit fragments in fragment names ---
    fragment_names = fragments.iloc[:, 0].astype(str)

    toolkit_locations = {}  # {toolkit_name: {plasmid_name: position}}
    toolkit_plate_wells = {}  # {fragment_name: (plate, position)}
    toolkit_keys = set()
    if use_myt_var.get():
        toolkit_df = pd.read_csv("toolkit_data.csv")
        # Build a mapping: {plasmid_name: (plate, position)}
        for _, row in toolkit_df.iterrows():
            toolkit = str(row["Plate"])
            toolkit_keys.add(toolkit)
            if toolkit not in toolkit_locations:
                toolkit_locations[toolkit] = {}
            toolkit_locations[toolkit][row["Name"]] = row["Position"]

        # For each fragment, if its name contains a toolkit key, and matches a toolkit entry, assign it
        for frag_name in fragment_names:
            found = False
            for toolkit in toolkit_keys:
                if toolkit in frag_name:
                    # Try to find a matching toolkit entry for this fragment
                    for plasmid_name, position in toolkit_locations[toolkit].items():
                        if plasmid_name in frag_name:
                            toolkit_plate_wells[frag_name] = (toolkit, position)
                            found = True
                            break
                if found:
                    break

    # Remove unnecessary columns
    constructs_df.drop(columns=[col for col in constructs_df.columns if "Overhang" in col], inplace=True, errors='ignore')
    constructs_df.drop(columns=["Status"], inplace=True, errors='ignore')

    # Calculate the number of inserts
    num_inserts = len(fragments)

    # Define locations for non-toolkit fragments
    locations = [f"{chr(65 + i // 6)}{i % 6 + 1}" for i in range(24)]
    inserts = []
    insert_plate_map = {}  # Map fragment name to (plate, well)

    non_toolkit_idx = 0
    for i, frag_name in enumerate(fragment_names):
        # Check if fragment is in any toolkit
        if use_myt_var.get() and frag_name in toolkit_plate_wells:
            toolkit_plate, toolkit_position = toolkit_plate_wells[frag_name]
            insert_plate_map[frag_name] = (toolkit_plate, toolkit_position)
            inserts.append((toolkit_plate, toolkit_position))
        else:
            insert_plate_map[frag_name] = ("tube_rack", locations[non_toolkit_idx])
            inserts.append(("tube_rack", locations[non_toolkit_idx]))
            non_toolkit_idx += 1

    remaining_locations = locations[non_toolkit_idx:]
    master_mix = remaining_locations[0]  # Use first remaining location for MM
    water_loc = remaining_locations[1]

    # Assign locations in thermocycler to constructs
    construct_tubes = [f"{chr(65 + i // 12)}{i % 12 + 1}" for i in range(len(constructs_df))]

    # Create a dictionary mapping insert names to their locations (well only, for script compatibility)
    insert_locations = {fragments.iloc[i, 0]: inserts[i] for i in range(num_inserts)}

    # Extract constructs as a list of lists and get construct names if available
    constructs = [row[1:].tolist() for _, row in constructs_df.iterrows()]
    
    if 'Name' in constructs_df.columns:
        construct_names = constructs_df['Name'].tolist()
    else:
        construct_names = [f"Construct {i+1}" for i in range(len(constructs))]

    # --- NEW: Get per-insert volumes from CSV if available, else default to 1 ---
    if "Volume" in fragments.columns:
        vol_per_insert_dict = dict(zip(fragments.iloc[:, 0], fragments["Volume"]))
    else:
        vol_per_insert_dict = {name: 1 for name in fragments.iloc[:, 0]}

    # Display the confirmation window, passing MM info and toolkit info
    display_confirmation_window(
        constructs_df, num_inserts, insert_locations, construct_tubes, construct_names,
        insert_plate_map, vol_per_insert_dict, bin_dict
    )

def display_confirmation_window(
    constructs_df, num_inserts, insert_locations, construct_tubes, construct_names,
    insert_plate_map, vol_per_insert_dict, bin_dict
):
    global confirmation_window, file_name_entry, excess_entry
    confirmation_window = tk.Tk()
    confirmation_window.title("Confirm Settings")
    confirmation_window.configure(padx=20, pady=20)
    confirmation_window.geometry("1000x600")  # Set a default size

    # Create a canvas and scrollbar for scrollable content
    canvas = tk.Canvas(confirmation_window)
    scrollbar = tk.Scrollbar(confirmation_window, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Tube placements info
    global tube_placements
    tube_placements = ""

    # --- Identify all toolkit plates and assign deck slots ---
    toolkit_plate_slots = {}
    # Use the same available slots as the rest of the script (for tip racks and toolkit plates)
    available_slots = ["1", "2", "3", "5", "6", "9"]

    # Calculate number of tips needed as in template.py
    num_master_mix_transfers = len(construct_tubes)
    num_insert_transfers = sum(len(construct) for construct in constructs)
    total_p20_tips = num_insert_transfers + num_master_mix_transfers  # assuming all MM and inserts use p20
    total_p300_tips = 0  # not used if all volumes < 20

    num_p20_racks = (total_p20_tips - 1) // 96 + 1 if total_p20_tips > 0 else 0
    num_p300_racks = (total_p300_tips - 1) // 96 + 1 if total_p300_tips > 0 else 0

    p20_slots = available_slots[:num_p20_racks]
    p300_slots = available_slots[num_p20_racks:num_p20_racks+num_p300_racks]
    toolkit_slots = available_slots[num_p20_racks+num_p300_racks:]

    used_toolkits = set()
    for insert, (plate, well) in insert_plate_map.items():
        if plate not in ("tube_rack", "temp_module", "myt_plate"):
            used_toolkits.add(plate)
    for idx, toolkit in enumerate(sorted(used_toolkits)):
        if idx < len(toolkit_slots):
            toolkit_plate_slots[toolkit] = toolkit_slots[idx]
        else:
            toolkit_plate_slots[toolkit] = "extra"

    # --- Build tube placements string with plate and slot info ---
    for insert, (plate, well) in insert_plate_map.items():
        if plate in toolkit_plate_slots:
            slot = toolkit_plate_slots[plate]
            tube_placements += f"[{well}] ({plate} Plate, Slot {slot}): {insert}, \n"
        elif plate == "myt_plate":
            tube_placements += f"[{well}] (MYT Plate): {insert}, \n"
        else:
            tube_placements += f"[{well}] (Temp Module): {insert}, \n"

    tube_placements += f"\n[{master_mix}] (Temp Module): Master Mix,"
    tube_placements += f"\n[{water_loc}] (Temp Module): Molecular Grade Water, \n"
    tube_placements += "\nConstructs will be built in the thermocycler module:\n\n"
    tube_placements += "\n".join([f"[{location}]: {construct_names[i]}, " for i, location in enumerate(construct_tubes)])

    # Add plate/slot summary for user clarity
    if used_toolkits:
        tube_placements += "\n\nToolkit plate locations on deck:\n"
        for toolkit, slot in toolkit_plate_slots.items():
            tube_placements += f"  {toolkit} Plate: Slot {slot}\n"

    # Confirmation message
    confirmation_message = (
        f"Loaded {num_inserts} fragments using {path_fragments} and\n"
        f"{len(constructs_df)} constructs using {path_constructs}.\n\n"
        "Reagents will be pulled from these locations:\n\n"
        f"{tube_placements}\n"
    )
    label_confirmation = tk.Label(
        scrollable_frame,
        text=confirmation_message,
        justify="left",
        wraplength=900,
        anchor="w",
        padx=10
    )
    label_confirmation.pack(pady=10, fill="x", anchor="w")

    # --- Per-insert volume input section (FIRST) ---
    tk.Label(
        scrollable_frame,
        text="Volumes need to be manually calculated for 25/50 fmol of each fragment, should be between >1µL:",
        anchor="w", justify="left"
    ).pack(pady=5, fill="x", anchor="w")
    insert_volume_entries = {}
    for insert_name in vol_per_insert_dict:
        frame = tk.Frame(scrollable_frame)
        frame.pack(fill="x", pady=2, anchor="w")
        bin_val = bin_dict.get(insert_name, "")
        label_text = f"({bin_val}) {insert_name}" if bin_val != "" else insert_name
        tk.Label(frame, text=label_text, width=40, anchor="w", justify="left").pack(side="left", padx=(0, 5))
        entry = tk.Entry(frame, width=10, justify="left")
        entry.insert(0, str(vol_per_insert_dict[insert_name]))
        entry.pack(side="left", padx=(0, 5))
        insert_volume_entries[insert_name] = entry

    # --- Master mix per reaction input section (SECOND) ---
    mm_per_reaction_frame = tk.Frame(scrollable_frame)
    mm_per_reaction_frame.pack(fill="x", pady=2, anchor="w")
    mm_per_reaction_label = tk.Label(mm_per_reaction_frame, text="Master Mix volume per reaction (µL):", anchor="w", justify="left", width=40)
    mm_per_reaction_label.pack(side="left", padx=(0, 5))
    mm_per_reaction_entry = tk.Entry(mm_per_reaction_frame, width=10, justify="left")
    mm_per_reaction_entry.insert(0, "6")
    mm_per_reaction_entry.pack(side="left", padx=(0, 5))

    # Input box for total reaction volume
    reaction_vol_frame = tk.Frame(scrollable_frame)
    reaction_vol_frame.pack(fill="x", pady=2, anchor="w")
    reaction_vol_label = tk.Label(reaction_vol_frame, text="Total reaction volume per construct (µL):", anchor="w", justify="left", width=40)
    reaction_vol_label.pack(side="left", padx=(0, 5))
    reaction_vol_entry = tk.Entry(reaction_vol_frame, width=10, justify="left")
    reaction_vol_entry.insert(0, "15")
    reaction_vol_entry.pack(side="left", padx=(0, 5))

    # --- Excess percentage input and live update ---
    excess_frame = tk.Frame(scrollable_frame)
    excess_frame.pack(fill="x", pady=2, anchor="w")
    excess_label = tk.Label(excess_frame, text="Excess percentage for master mix (e.g., 5 for 5%):", anchor="w", justify="left", width=40)
    excess_label.pack(side="left", padx=(0, 5))
    excess_entry = tk.Entry(excess_frame, width=10, justify="left")
    excess_entry.insert(0, "0")
    excess_entry.pack(side="left", padx=(0, 5))

    # Info label for water and master mix, to be updated live
    mm_info_var = tk.StringVar()
    def update_mm_info(*args):
        try:
            excess_percent = float(excess_entry.get())
        except Exception:
            excess_percent = 0.0
        try:
            reaction_vol = float(reaction_vol_entry.get())
        except Exception:
            reaction_vol = 15.0
        try:
            mm_per_reaction = float(mm_per_reaction_entry.get())
        except Exception:
            mm_per_reaction = 6.0
        n_reactions = len(constructs)
        water_per_reaction = []
        for construct in constructs:
            total_insert_vol = sum(safe_float(insert_volume_entries[insert]) for insert in construct)
            water_vol = reaction_vol - (mm_per_reaction + total_insert_vol)
            water_per_reaction.append(round(water_vol,2))
        total_mm = mm_per_reaction * n_reactions
        total_mm_with_excess = int(total_mm * (1 + excess_percent / 100) + 0.5)
        mm_info_var.set(
            f"Total master mix (with {excess_percent:.1f}% excess): {total_mm_with_excess} uL\n"
            f"Water per reaction (should all be positive): {water_per_reaction} uL\n"
            f"Total water needed: {round(sum(water_per_reaction),2)} uL"
        )
    excess_entry.bind("<KeyRelease>", update_mm_info)
    reaction_vol_entry.bind("<KeyRelease>", update_mm_info)
    mm_per_reaction_entry.bind("<KeyRelease>", update_mm_info)
    for entry in insert_volume_entries.values():
        entry.bind("<KeyRelease>", update_mm_info)
    update_mm_info()  # Initialize with default

    mm_info_label = tk.Label(
        scrollable_frame,
        textvariable=mm_info_var,
        justify="left",
        anchor="w",
        wraplength=500,
        pady=5
    )
    mm_info_label.pack(pady=(10, 10), fill="x", anchor="w")

    # --- Thermocycler settings section (grouped, with consistent padding and style) ---
    tc_settings_frame = tk.Frame(scrollable_frame)
    tc_settings_frame.pack(fill="x", pady=(10, 10), anchor="w")

    tc_settings_label = tk.Label(
        tc_settings_frame,
        text="Enter settings for thermocycler protocol:",
        anchor="w",
        justify="left",
        pady=2
    )
    tc_settings_label.pack(side="top", anchor="w", fill="x", pady=(0, 8))

    # Digestion Temp
    digestion_frame = tk.Frame(tc_settings_frame)
    digestion_frame.pack(fill="x", pady=2, anchor="w")
    tc_temp_label = tk.Label(digestion_frame, text="Digestion Temp (°C):", anchor="w", justify="left", width=40)
    tc_temp_label.pack(side="left", padx=(0, 5))
    tc_temp_activation = tk.Entry(digestion_frame, width=10, justify="left")
    tc_temp_activation.insert(0, "37")
    tc_temp_activation.pack(side="left", padx=(0, 5))

    # Ligation Temp
    ligation_frame = tk.Frame(tc_settings_frame)
    ligation_frame.pack(fill="x", pady=2, anchor="w")
    tc_temp_label_lig = tk.Label(ligation_frame, text="Ligation Temp (°C):", anchor="w", justify="left", width=40)
    tc_temp_label_lig.pack(side="left", padx=(0, 5))
    tc_temp_ligation = tk.Entry(ligation_frame, width=10, justify="left")
    tc_temp_ligation.insert(0, "16")
    tc_temp_ligation.pack(side="left", padx=(0, 5))

    # Final Inactivation Temp
    inact_frame = tk.Frame(tc_settings_frame)
    inact_frame.pack(fill="x", pady=2, anchor="w")
    tc_temp_label2 = tk.Label(inact_frame, text="Final Inactivation Temp (°C):", anchor="w", justify="left", width=40)
    tc_temp_label2.pack(side="left", padx=(0, 5))
    tc_temp_inactivation = tk.Entry(inact_frame, width=10, justify="left")
    tc_temp_inactivation.insert(0, "65")
    tc_temp_inactivation.pack(side="left", padx=(0, 5))

    # Number of cycles
    cycles_frame = tk.Frame(tc_settings_frame)
    cycles_frame.pack(fill="x", pady=2, anchor="w")
    cycles_label = tk.Label(cycles_frame, text="Number of cycles (for digestion/ligation):", anchor="w", justify="left", width=40)
    cycles_label.pack(side="left", padx=(0, 5))
    cycles_entry = tk.Entry(cycles_frame, width=10, justify="left")
    cycles_entry.insert(0, "25")
    cycles_entry.pack(side="left", padx=(0, 5))

    # --- File name section (grouped, with clear separation) ---
    file_name_frame = tk.Frame(scrollable_frame)
    file_name_frame.pack(fill="x", pady=(15, 5), anchor="w")
    file_name_label = tk.Label(
        file_name_frame,
        text="File will be saved in the same directory as this script, and overwrite files with the same name.\nSave as:",
        anchor="w",
        justify="left"
    )
    file_name_label.pack(side="top", anchor="w", fill="x", pady=(0, 2))
    file_name_entry = tk.Entry(file_name_frame, width=30, justify="left")
    file_name_entry.insert(0, "saved_protocol.py")
    file_name_entry.pack(side="top", anchor="w", padx=(0, 0), pady=(0, 2))

    # Confirm button to generate the script (extra space above)
    confirm_button = tk.Button(
        scrollable_frame,
        text="Confirm",
        anchor="w",
        command=lambda: generate_script(
            file_name_entry, tc_temp_activation, tc_temp_inactivation,
            excess_entry, reaction_vol_entry, insert_volume_entries, mm_per_reaction_entry,
            tc_temp_ligation, cycles_entry
        )
    )
    confirm_button.pack(pady=(20, 10), anchor="w")

def generate_script(
    file_name_entry, tc_temp_activation, tc_temp_inactivation, excess_entry,
    reaction_vol_entry, insert_volume_entries, mm_per_reaction_entry,
    tc_temp_ligation, cycles_entry
):
    file_name = file_name_entry.get()
    try:
        excess_percent = float(excess_entry.get())
    except Exception:
        excess_percent = 0.0  # Default to 0% excess
    try:
        reaction_vol = float(reaction_vol_entry.get())
    except Exception:
        reaction_vol = 15.0  # Default to 15 µL
    try:
        mm_per_reaction = float(mm_per_reaction_entry.get())
    except Exception:
        mm_per_reaction = 6.0  # Default to 6 µL
    try:
        ligation_temp = float(tc_temp_ligation.get())
    except Exception:
        ligation_temp = 16.0  # Default to 16 °C
    try:
        num_cycles = int(cycles_entry.get())
    except Exception:
        num_cycles = 25  # Default to 25 cycles

    # Use per-insert volumes for each construct
    vol_per_insert_dict = {}
    for insert_name, entry in insert_volume_entries.items():
        try:
            vol_per_insert_dict[insert_name] = float(entry.get())
        except Exception:
            vol_per_insert_dict[insert_name] = 1.0  # fallback default

    # Calculate water needed for each well
    water_per_reaction = []
    for construct in constructs:
        total_insert_vol = sum(float(vol_per_insert_dict.get(insert, 1)) for insert in construct)
        water_vol = reaction_vol - (mm_per_reaction + total_insert_vol)
        water_per_reaction.append(round(water_vol, 2))  # Round to 2

    # Calculate number of tips needed as in template.py
    num_master_mix_transfers = len(construct_tubes)
    num_insert_transfers = sum(len(construct) for construct in constructs)
    total_p20_tips = num_insert_transfers + num_master_mix_transfers  # assuming all MM and inserts use p20
    total_p300_tips = 0  # not used if all volumes < 20

    num_p20_racks = (total_p20_tips - 1) // 96 + 1 if total_p20_tips > 0 else 0
    num_p300_racks = (total_p300_tips - 1) // 96 + 1 if total_p300_tips > 0 else 0

    script = template.format(
        tube_placements=tube_placements,
        inserts=insert_locations,
        master_mix=master_mix,
        construct_tubes=construct_tubes,
        mm_per_reaction=mm_per_reaction,
        vol_per_insert=vol_per_insert_dict,
        water_per_reaction=water_per_reaction,
        reaction_temp=tc_temp_activation.get(),
        ligation_temp=ligation_temp,
        inactivation_temp=tc_temp_inactivation.get(),
        constructs=constructs,
        total_p20_tips=total_p20_tips,
        total_p300_tips=total_p300_tips,
        reaction_vol=reaction_vol,
        vol_master_mix_per_reaction=[mm_per_reaction] * len(constructs),
        num_cycles=num_cycles
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
root.title("Golden Gate Assembly - Select Benchling Files")
root.configure(padx=20, pady=20)  # Add horizontal (and vertical) padding
root.geometry("500x220")  # Set a default size

# Add a variable to track the checkbox state
use_myt_var = tk.BooleanVar(value=False)

def on_myt_checkbox():
    if use_myt_var.get():
        handle_myt_toolkit_selected()
    else:
        handle_myt_toolkit_unselected()

def handle_myt_toolkit_selected():
    print("Toolkit option selected.")

def handle_myt_toolkit_unselected():
    print("Toolkit option unselected.")

# --- Add file selection buttons ---
def check_accept_ready():
    if path_fragments and path_constructs:
        accept_button.config(state="normal")
    else:
        accept_button.config(state="disabled")

def select_file_1():
    global path_fragments
    path_fragments = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if path_fragments:
        select_button_1.config(text=f"Selected: {path_fragments}")
    check_accept_ready()

def select_file_2():
    global path_constructs
    path_constructs = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if path_constructs:
        select_button_2.config(text=f"Selected: {path_constructs}")
    check_accept_ready()

select_button_1 = tk.Button(root, text="Select Fragments CSV", command=select_file_1)
select_button_1.pack(pady=5)

select_button_2 = tk.Button(root, text="Select Constructs CSV", command=select_file_2)
select_button_2.pack(pady=5)

myt_checkbox = tk.Checkbutton(root, text="Pull fragments from toolkit plates (MYT, YTK, YSD)", variable=use_myt_var, command=on_myt_checkbox)
myt_checkbox.pack(pady=5)

accept_button = tk.Button(root, text="Confirm", command=accept_files, state="disabled")
accept_button.pack(pady=20)

# Run the application
root.mainloop()