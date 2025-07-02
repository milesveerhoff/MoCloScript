import tkinter as tk
from tkinter import filedialog
import shutil
import os

# --- Use template.py as the template file ---
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "template.py")

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
        text="Enter the volume of molecular grade water needed for each oligo:",
        anchor="center",
        justify="center"
    ).pack(pady=(0, 8), fill="x")
    try:
        count = int(oligos_entry.get())
        if count < 1:
            count = 1
        elif count > 24:
            count = 24
    except ValueError:
        count = 1
    for i in range(count):
        slot = f"{chr(65 + i // 6)}{i % 6 + 1}"
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
    total_oligo_volume = 0.0
    for slot, entry in oligo_entry_widgets:
        try:
            value = float(entry.get())
        except ValueError:
            value = 0.0
        total_oligo_volume += value
    num_oligos = len(oligo_entry_widgets)
    total_water = total_oligo_volume + (45 * num_oligos)
    total_water_ml = total_water / 1000
    total_water_label.config(
        text=f"Minimum molecular grade water needed: {total_water:.2f} µL ({total_water_ml:.3f} mL)\n\nNote: water in falcon tube should not exceed 20 mL to avoid contamination.",
    )

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

    # Read template.py, replace {oligo_values} with the dictionary
    with open(TEMPLATE_PATH, "r") as f:
        template_code = f.read()
    script = template_code.replace("{oligo_values}", repr(oligo_values))

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

    # Read template.py, replace {oligo_values} with the dictionary
    with open(TEMPLATE_PATH, "r") as f:
        template_code = f.read()
    script = template_code.replace("{oligo_values}", repr(oligo_values))

    with open(file_path, "w") as f:
        f.write(script)
    status_label.config(
        text=f"Script saved as {os.path.basename(file_path)}\n"
    )

# --- Main window ---
root = tk.Tk()
root.title("Primer Pal Oligo Dilution Script Generator")
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
    text="Number of oligos to dilute (24 max):",
    anchor="center",
    justify="center"
).pack(pady=(10, 0), fill="x")

oligos_entry = tk.Entry(scrollable_frame, justify="center")
oligos_entry.insert(0, "-")  
oligos_entry.pack(pady=5)
oligos_entry.configure(width=20)

tk.Label(
    scrollable_frame,
    text="Protocol will use one p300 and one p20 tip for each oligo.",
    anchor="center",
    justify="center"
).pack(pady=(10, 0), fill="x")

oligo_entries_frame = tk.Frame(scrollable_frame)
oligo_entries_frame.pack(pady=5)

oligos_entry.bind("<KeyRelease>", update_oligo_entries)
oligos_entry.bind("<FocusIn>", select_all)  # Highlight text on focus

total_water_label = tk.Label(
    scrollable_frame,
    text="Minimum molecular grade water needed: 0 µL (0.000 mL)\n\nNote: water in falcon tube should not exceed 20 mL to avoid contamination.",
    fg="blue",
    anchor="center",
    justify="center"
)
total_water_label.pack(pady=5, fill="x")

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
filename_entry.insert(0, "oligo_dilution.py")
filename_entry.pack(side="left", padx=(0, 5))
filename_entry.bind("<FocusIn>", select_all)  # Highlight text on focus

save_button = tk.Button(
    file_frame,
    text="Save As",
    command=save_script
)
save_button.pack(side="left", padx=(5, 0))

generate_button = tk.Button(
    scrollable_frame,
    text="Generate Script",
    command=generate_script
)
generate_button.pack(pady=(10, 0))

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
