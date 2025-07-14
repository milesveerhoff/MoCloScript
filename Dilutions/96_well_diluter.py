import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
import csv

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "template.py")

def load_template():
    with open(TEMPLATE_PATH, "r") as f:
        return f.read()

# --- GUI logic ---
# Store entry widgets for later access
oligo_entry_widgets = []

def select_all(event):
    event.widget.select_range(0, tk.END)
    event.widget.icursor(tk.END)
    return 'break'

def update_oligo_entries(*args):
    global oligo_entry_widgets
    oligo_entry_widgets = []
    for widget in oligo_entries_frame.winfo_children():
        widget.destroy()
    # Add a single label at the top
    tk.Label(
        oligo_entries_frame,
        text="Enter the volume to pull from each well (0 to skip):",
        anchor="center",
        justify="center"
    ).pack(pady=(0, 8), fill="x")
    try:
        count = int(oligos_entry.get())
        if count < 1:
            count = 1
        elif count > 96:
            count = 96
    except ValueError:
        count = 1
    # Generate well names A1-H12
    wells = [f"{chr(65 + row)}{col+1}" for row in range(8) for col in range(12)]
    for i in range(count):
        slot = wells[i]
        row = tk.Frame(oligo_entries_frame)
        row.pack(fill="x", pady=(0, 6))
        label = tk.Label(row, text=slot, width=6, anchor="e", justify="right")
        label.pack(side="left")
        entry = tk.Entry(row, justify="center", width=20)
        entry.insert(0, "---")
        entry.pack(side="left", padx=(6, 0))
        entry.bind("<KeyRelease>", lambda e: update_total_water())
        entry.bind("<FocusIn>", select_all)  # Highlight text on focus
        oligo_entry_widgets.append((slot, entry))
    update_total_water()
    scrollable_frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

def update_total_water():
    return  # This function is not used in the current context
    # total_oligo_volume = 0.0
    # for slot, entry in oligo_entry_widgets:
    #     try:
    #         value = float(entry.get())
    #     except ValueError:
    #         value = 0.0
    #     total_oligo_volume += value
    # num_oligos = len(oligo_entry_widgets)
    # total_water = total_oligo_volume + (45 * num_oligos)
    # total_water_ml = total_water / 1000
    # total_water_label.config(
    #     text=f"Minimum volume molecular grade water needed: {total_water:.2f} µL ({total_water_ml:.3f} mL)\n\nNote: water in falcon tube should not exceed 20 mL to avoid contamination.",
    # )

def generate_script():
    # Collect oligo values into a dictionary
    oligo_values = {}
    total_oligo_volume = 0.0
    for slot, entry in oligo_entry_widgets:
        try:
            value = float(entry.get())
        except ValueError:
            value = 0.0
        oligo_values[slot] = value
        total_oligo_volume += value

    num_oligos = len(oligo_entry_widgets)
    total_water = total_oligo_volume + (45 * num_oligos)

    # Load template from file
    template = load_template()
    script = template.replace("{oligo_values}", repr(oligo_values))

    output_path = os.path.join(os.path.dirname(__file__), "oligo_dilution.py")
    with open(output_path, "w") as f:
        f.write(script)
    status_label.config(
        text=f"Script saved as oligo_dilution.py\n"
    )

def save_script():
    # Open file dialog to choose save location
    initialfile = filename_entry.get().strip() or "oligo_dilution.py"
    file_path = filedialog.asksaveasfilename(
        defaultextension=".py",
        filetypes=[("Python files", "*.py"), ("All files", "*.*")],
        initialfile=initialfile,
        initialdir=os.path.dirname(__file__),
        title="Save Protocol As"
    )
    if not file_path:
        return  # User cancelled

    # Collect oligo values into a dictionary
    oligo_values = {}
    total_oligo_volume = 0.0
    for slot, entry in oligo_entry_widgets:
        try:
            value = float(entry.get())
        except ValueError:
            value = 0.0
        oligo_values[slot] = value
        total_oligo_volume += value

    num_oligos = len(oligo_entry_widgets)
    total_water = total_oligo_volume + (45 * num_oligos)

    # Load template from file
    template = load_template()
    script = template.replace("{stock_values}", repr(oligo_values))

    with open(file_path, "w") as f:
        f.write(script)
    status_label.config(
        text=f"Script saved as {os.path.basename(file_path)}\n"
    )

def load_csv():
    file_path = filedialog.askopenfilename(
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        title="Select CSV File"
    )
    if not file_path:
        return
    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            # Create a mapping from Position to Volume
            volume_map = {}
            wells_in_csv = []
            for row in reader:
                pos = row.get("Position", "").strip()
                vol = row.get("Volume", "").strip()
                if pos:
                    wells_in_csv.append(pos)
                    try:
                        volume_map[pos] = float(vol) if vol else 0.0
                    except ValueError:
                        volume_map[pos] = 0.0
            # Set the number of wells in the entry and update widgets
            oligos_entry.delete(0, tk.END)
            oligos_entry.insert(0, str(len(wells_in_csv)))
            update_oligo_entries()
            # Update entry widgets with CSV values
            for slot, entry in oligo_entry_widgets:
                entry.delete(0, tk.END)
                entry.insert(0, str(volume_map.get(slot, 0.0)))
        status_label.config(text=f"Loaded volumes from {os.path.basename(file_path)}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load CSV: {e}")

# --- Main window ---
root = tk.Tk()
root.title("Dilution Script Generator")
root.geometry("450x450")

# --- Scrollable Frame Setup ---
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True, padx=(20,0))

canvas = tk.Canvas(main_frame)
canvas.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)

# Properly update scrollregion when widgets are added/removed
def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

scrollable_frame = tk.Frame(canvas)
scrollable_frame.bind("<Configure>", on_frame_configure)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# --- Widgets in scrollable frame ---
tk.Label(
    scrollable_frame,
    text="Number of items to dilute (96 max):",
    anchor="center",
    justify="center"
).pack(pady=(10, 0), fill="x")

oligos_entry = tk.Entry(scrollable_frame, justify="center")
oligos_entry.insert(0, "--")  
oligos_entry.pack(pady=5)
oligos_entry.configure(width=20)

# tk.Label(
#     scrollable_frame,
#     text="Protocol will use one p300 and one p20 tip for each oligo.",
#     anchor="center",
#     justify="center"
# ).pack(pady=(10, 0), fill="x")

oligo_entries_frame = tk.Frame(scrollable_frame)
oligo_entries_frame.pack(pady=5)

oligos_entry.bind("<KeyRelease>", update_oligo_entries)
oligos_entry.bind("<FocusIn>", select_all)  # Highlight text on focus

# total_water_label = tk.Label(
#     scrollable_frame,
#     text="Minimum volume molecular grade water needed: 0 µL (0.000 mL)\n\nNote: water in falcon tube should not exceed 20 mL to avoid contamination.",
#     fg="blue",
#     anchor="center",
#     justify="center"
# )
# total_water_label.pack(pady=5, fill="x")

# File name entry and Save As button side by side (centered)
file_frame = tk.Frame(scrollable_frame)
file_frame.pack(pady=5)

tk.Label(
    file_frame,
    text="Output:",
    anchor="center",
    justify="center"
).pack(side="left", padx=(0, 5))

filename_entry = tk.Entry(file_frame, justify="center", width=22)
filename_entry.insert(0, "dilution.py")
filename_entry.pack(side="left", padx=(0, 5))
filename_entry.bind("<FocusIn>", select_all)  # Highlight text on focus

save_button = tk.Button(
    file_frame,
    text="Save As",
    command=save_script
)
save_button.pack(side="left", padx=(5, 0))

# Add a button to load CSV above the file name entry
csv_button = tk.Button(
    scrollable_frame,
    text="Load Volumes from CSV",
    command=load_csv
)
csv_button.pack(pady=5)

status_label = tk.Label(
    scrollable_frame,
    text="",
    anchor="center",
    justify="center"
)
status_label.pack(pady=5, fill="x")

# Make mousewheel scroll the canvas (Windows/Mac/Linux compatible)
def _on_mousewheel(event):
    if event.delta:
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    elif event.num == 5:
        canvas.yview_scroll(1, "units")
    elif event.num == 4:
        canvas.yview_scroll(-1, "units")

canvas.bind_all("<MouseWheel>", _on_mousewheel)      # Windows/Mac
canvas.bind_all("<Button-4>", _on_mousewheel)        # Linux scroll up
canvas.bind_all("<Button-5>", _on_mousewheel)        # Linux scroll down

root.mainloop()
