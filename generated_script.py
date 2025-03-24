
from opentrons import protocol_api # type: ignore
metadata = {"apiLevel": "2.16"}
# Fragments and constructs
inserts = {'Lvl 1 GFP Dropout L2RE': 'A1', 'pYTK014': 'A2', 'pYTK017': 'A3', 'pYTK027': 'A4', 'pYSD021': 'A5', "HFB1 Fragment Sequence, GenBank KU173825 + moclo ends for 3b' part, no stop codon": 'A6', 'pYSD085': 'B1', 'pYTK065': 'B2'}
constructs = [['Lvl 1 GFP Dropout L2RE', 'pYTK014', 'pYSD021', "HFB1 Fragment Sequence, GenBank KU173825 + moclo ends for 3b' part, no stop codon", 'pYSD085', 'pYTK065'], ['Lvl 1 GFP Dropout L2RE', 'pYTK017', 'pYSD021', "HFB1 Fragment Sequence, GenBank KU173825 + moclo ends for 3b' part, no stop codon", 'pYSD085', 'pYTK065'], ['Lvl 1 GFP Dropout L2RE', 'pYTK027', 'pYSD021', "HFB1 Fragment Sequence, GenBank KU173825 + moclo ends for 3b' part, no stop codon", 'pYSD085', 'pYTK065']]
# Tube rack locations of reagents
buffer = "B3"
assembly_mix = "B4"
h2o = "B5"
reagent_tubes = [buffer, assembly_mix, h2o] + list(inserts.values())
# Reaction Tube Locations
construct_tubes = ['B6', 'C1', 'C2']
# Define volumes, in uL
vol_buffer = 1
vol_assembly_mix = 1
vol_h2o = [44.0, 44.0, 44.0]
vol_per_insert = 0.5
volumes = [vol_buffer, vol_assembly_mix] + [vol_per_insert] * len(inserts)
def run(protocol: protocol_api.ProtocolContext):
    # Define labware
    tips = protocol.load_labware("opentrons_96_tiprack_300ul", "9")
    tube_rack = protocol.load_labware("opentrons_24_tuberack_nest_1.5ml_snapcap", "1")
    # Initialize pipette
    pipette = protocol.load_instrument("p300_single_gen2", "right", tip_racks=[tips])
    # Distribute water to tubes
    for index, construct_tube in enumerate(construct_tubes):
        pipette.transfer(vol_h2o[index], tube_rack[h2o], tube_rack[construct_tube])
    # Distribute reagents to tubes based on the corresponding inserts from the constructs CSV file
    for index, construct_tube in enumerate(construct_tubes):
        construct_inserts = constructs[index]  # Get inserts for the current construct
        for insert in construct_inserts:
            insert_location = inserts[insert]  # Get the location of the insert
            pipette.transfer(vol_per_insert, tube_rack[insert_location], tube_rack[construct_tube])
        pipette.transfer(vol_buffer, tube_rack[buffer], tube_rack[construct_tube])
        pipette.transfer(vol_assembly_mix, tube_rack[assembly_mix], tube_rack[construct_tube])
