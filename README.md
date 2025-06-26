# OpentronsGoldenGate

**OpentronsGoldenGate** is a graphical tool and protocol generator for automating Golden Gate/MoClo DNA assembly workflows using benchling.com and the Opentrons OT-2 liquid handling robot. It is designed to streamline the process of preparing and running complex DNA assembly reactions, including support for the Multiplex Yeast Toolkit (MYT).

---

## Features

- **Graphical User Interface (GUI):**  
  Easily select input files, review and adjust reaction parameters, and generate protocols with a user-friendly interface built in Tkinter.

- **Flexible Input:**  
  Accepts CSV files describing DNA fragments and construct designs exported directly from benchling.  
  Optionally integrates with the Multiplex Yeast Toolkit (MYT) for automated well assignment.

- **Automated Labware Assignment:**  
  Assigns reagents and constructs to deck positions and modules (thermocycler, temperature module) automatically.

- **Customizable Reaction Parameters:**  
  Set per-insert volumes, master mix volumes, reaction volumes, excess percentages, and thermocycler settings (digestion temp, ligation temp, inactivation temp, number of cycles).

- **Protocol Generation:**  
  Outputs a ready-to-run Python protocol script for the Opentrons OT-2, including all pipetting steps and thermocycler programming.

---

## How to Use

1. **Prepare Input Files:**
   - **Fragments CSV:** List of DNA fragments, with columns for name, volume, etc. I.e. "Fragments" table in benchling.
   - **Constructs CSV:** List of constructs, each row specifying the fragments to combine. I.e. "Constructs" table in benchling.

2. **Launch the Application:**
   - Run `assembly_main.py` with Python 3 (requires `pandas` and `tkinter`).

3. **Select Input Files:**
   - Use the GUI to select your fragments and constructs CSV files.
   - Optionally, check the "Use Multiplex Yeast Toolkit (MYT)" box to use MYT well assignments.

4. **Review and Edit Settings:**
   - Confirm reagent locations and construct assignments.
   - Adjust per-insert volumes, master mix, reaction volume, and excess as needed.
   - Set thermocycler parameters (digestion temp, ligation temp, inactivation temp, cycles).

5. **Generate Protocol:**
   - Enter a filename and click "Confirm" to generate your Opentrons protocol script.

6. **Run on OT-2:**
   - Upload the generated protocol (e.g., `saved_protocol.py`) to your Opentrons app and run as usual.

---

## Requirements

- Python 3.7+
- `pandas`
- `tkinter` (usually included with Python)

## License

This repository is provided for research and educational use.  
See `LICENSE` for details.

---

## Acknowledgments

- Inspired by [AsssemblyTron](https://github.com/PlantSynBioLab/AssemblyTron)
- Incorporates the Modular Cloning (MoClo) and Golden Gate assembly standards.
- MYT support based on the Multiplex Yeast Toolkit.
- Thermocycler protocol based on the [Bennett Lab](https://wiki.rice.edu/confluence/display/BIODESIGN/Golden+Gate+Assembly)

