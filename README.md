# MoCloMatic

**MoCloMatic** is a graphical tool and protocol generator for automating Golden Gate/MoClo DNA assembly workflows using [benchling.com](https://benchling.com) and the Opentrons OT-2 liquid handling robot. It streamlines the process of preparing and running complex DNA assembly reactions, including support for multiple toolkits (e.g., Multiplex Yeast Toolkit (MYT), Yeast Toolkit (YTK), and others).

---

## Features

- **Graphical User Interface (GUI):**  
  Easily select input files, review and adjust reaction parameters, and generate protocols with a user-friendly interface built in Tkinter.

- **Flexible Input:**  
  Accepts CSV files describing DNA fragments and construct designs exported directly from Benchling.  
  Supports multiple toolkits for automated well assignment.

- **Automated Labware Assignment:**  
  Assigns reagents and constructs to deck positions and modules (thermocycler, temperature module, and multiple toolkit plates) automatically.  
  Toolkit plates are assigned to deck slots after tip racks, with the slot assignment clearly displayed in the GUI and protocol.

- **Customizable Reaction Parameters:**  
  Set per-insert volumes, master mix volumes, reaction volumes, excess percentages, and thermocycler settings (digestion temp, ligation temp, inactivation temp, number of cycles).

- **Live Calculation:**  
  Displays calculated master mix and water requirements as you adjust parameters.

- **Protocol Generation:**  
  Outputs a ready-to-run Python protocol script for the Opentrons OT-2, including all pipetting steps and thermocycler programming.  
  Supports multiple toolkit plates, each loaded into a specific deck slot.

---

## How to Use

1. **Prepare Input Files (Export From Benchling):**
   - **Fragments CSV:** List of DNA fragments, from the "Fragments" table in Benchling.
   - **Constructs CSV:** List of constructs, each row specifying the fragments to combine, from the "Constructs" table in Benchling.
   - Exported files will default to "table.csv" so rename or keep track of each file.

2. **Launch the Application:**
   - Run `assembly_main.py` with Python 3 (requires `pandas` and `tkinter`).

3. **Select Input Files:**
   - Use the GUI to select your fragments and constructs CSV files.
   - Optionally, check the "Use Toolkit CSV" box to use toolkit well assignments.

4. **Review and Edit Settings:**
   - Confirm reagent locations and construct assignments.
   - Adjust per-insert volumes, master mix, reaction volume, and excess as needed.
   - Set thermocycler parameters (digestion temp, ligation temp, inactivation temp, cycles).

5. **Generate Protocol:**
   - Enter a filename and click "Confirm" to generate your Opentrons protocol script.

6. **Run on OT-2:**
   - Import the generated protocol (e.g., `saved_protocol.py`) directly to the Opentrons app and run as usual.

---

## Toolkit Support & Naming Scheme

**To use toolkit-based well assignment:**

- A toolkit CSV is provided (e.g., `toolkit_data.csv`) with columns:  
  `Name,Position,Plate`
  - `Name`: The exact name of the plasmid/part as it appears in your fragments CSV.
  - `Position`: The well position on the plate (e.g., `A1`, `B2`).
  - `Plate`: The name of the toolkit plate (e.g., `MYT`, `YTK`, `YSD`).
  - To add support for additional toolkits, simply update this csv via the same scheme.

**Naming Requirements:**
- The `Name` in your toolkit CSV must match (or be contained in) the fragment name in your fragments CSV for automatic assignment.
- The `Plate` value is used to group fragments onto the same physical plate and assign it to a deck slot.
- Each unique `Plate` will be loaded as a separate 96-well plate on the OT-2 deck.

**Example fragment name in fragments CSV:**  
If your fragment is named `pMYT001_nan_HIS3`, and your toolkit CSV has `pMYT001` as a `Name`, the script will assign it to the MYT plate at position A1.

---

## Requirements

- Python 3.7+
- `pandas`
- `tkinter` (usually included with Python)

---

## License

This repository is provided for research and educational use.

---

## Acknowledgments

- Inspired by [AssemblyTron](https://github.com/PlantSynBioLab/AssemblyTron)
- Golden Gate protocols based on the [Bennett Lab](https://wiki.rice.edu/confluence/display/BIODESIGN/Golden+Gate+Assembly)

