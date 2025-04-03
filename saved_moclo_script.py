import opentrons.execute # type: ignore
from opentrons import protocol_api # type: ignore
metadata = {"apiLevel": "2.16", "description": '''[A1]: Lvl 1 GFP Dropout L2RE, 
[A2]: pYTK014, 
[A3]: pYTK017, 
[A4]: pYTK027, 
[A5]: pYSD021, 
[A6]: HFB1 Fragment Sequence, GenBank KU173825 + moclo ends for 3b' part, no stop codon, 
[B1]: pYSD085, 
[B2]: pYTK065, 

[B3]: Buffer, 
[B4]: Assembly Mix, 
[B5]: Sterile DI Water, 

Constructs will be built at the following locations in the thermocycler module:
[A1]: OLD pWL-591 Lvl 1 GFP Dropout L2RE-pYTK014-pYSD021-HFB1:KU173825, 3b' part, no stop-pYSD085-pYTK065, 
[A2]: OLD pWL-590 Lvl 1 GFP Dropout L2RE-pYTK017-pYSD021-HFB1:KU173825, 3b' part, no stop-pYSD085-pYTK065, 
[A3]: OLD pWL-589 Lvl 1 GFP Dropout L2RE-pYTK027-pYSD021-HFB1:KU173825, 3b' part, no stop-pYSD085-pYTK065, '''}

# Fragments and constructs
inserts = {'Lvl 1 GFP Dropout L2RE': 'A1', 'pYTK014': 'A2', 'pYTK017': 'A3', 'pYTK027': 'A4', 'pYSD021': 'A5', "HFB1 Fragment Sequence, GenBank KU173825 + moclo ends for 3b' part, no stop codon": 'A6', 'pYSD085': 'B1', 'pYTK065': 'B2'} # type: ignore
constructs = [['Lvl 1 GFP Dropout L2RE', 'pYTK014', 'pYSD021', "HFB1 Fragment Sequence, GenBank KU173825 + moclo ends for 3b' part, no stop codon", 'pYSD085', 'pYTK065'], ['Lvl 1 GFP Dropout L2RE', 'pYTK017', 'pYSD021', "HFB1 Fragment Sequence, GenBank KU173825 + moclo ends for 3b' part, no stop codon", 'pYSD085', 'pYTK065'], ['Lvl 1 GFP Dropout L2RE', 'pYTK027', 'pYSD021', "HFB1 Fragment Sequence, GenBank KU173825 + moclo ends for 3b' part, no stop codon", 'pYSD085', 'pYTK065']] # type: ignore

# Tube rack locations of reagents
buffer = "B3"
assembly_mix = "B4"
h2o = "B5"
reagent_tubes = [buffer, assembly_mix, h2o] + list(inserts.values())

# Reaction Tube Locations
construct_tubes = ['A1', 'A2', 'A3'] # type: ignore

# Define volumes, in uL
vol_buffer = 1
vol_assembly_mix = 1
vol_h2o = [34.0, 34.0, 34.0] # type: ignore
vol_per_insert = 1 # type: ignore
volumes = [vol_buffer, vol_assembly_mix] + [vol_per_insert] * len(inserts)

# Thermocycler settings
reaction_temp = 37 # type: ignore
inactivation_temp = 65 # type: ignore
reaction_vol = 40 # Total volume of the reaction

def run(protocol: protocol_api.ProtocolContext):
    # Define labware
    tips300 = protocol.load_labware("opentrons_96_tiprack_300ul", "9")
    tips20 = protocol.load_labware("opentrons_96_tiprack_20ul", "6")
    tube_rack = protocol.load_labware("opentrons_24_tuberack_nest_1.5ml_snapcap", "1")
    tc_mod = protocol.load_module(module_name="thermocyclerModuleV2")
    tc_plate = tc_mod.load_labware(name="opentrons_96_wellplate_200ul_pcr_full_skirt")
    temp_mod = protocol.load_module(
    module_name="temperature module gen2", location="4"
    )
    temp_tubes = temp_mod.load_labware(
    "opentrons_24_aluminumblock_nest_1.5ml_screwcap"
    )

    # Blink and pause function
    def pause(message):
        for i in range(3):
            protocol.set_rail_lights(False)
            protocol.delay(seconds=0.3)
            protocol.set_rail_lights(True)
            protocol.delay(seconds=0.3)
        protocol.set_rail_lights(True)
        protocol.pause(message)

    # Initialize pipettes
    p300 = protocol.load_instrument("p300_single_gen2", "right", tip_racks=[tips300])
    p20 = protocol.load_instrument("p20_single_gen2", "left", tip_racks=[tips20])

    # Initialize thermocycler
    tc_mod.open_lid()

    def pipette_transfer(vol, source, dest, pipette=None):
        if pipette is not None:
            pipette.transfer(vol, source, dest)
        else:
            if vol < 20:
                p20.transfer(vol, source, dest)
            else:
                p300.transfer(vol, source, dest)
    
    # Distribute water to tubes
    for index, construct_tube in enumerate(construct_tubes):
        pipette_transfer(vol_h2o[index], tube_rack[h2o], tc_plate[construct_tube])

    # Distribute reagents to tubes based on the corresponding inserts from the constructs CSV file
    for index, construct_tube in enumerate(construct_tubes):
        construct_inserts = constructs[index]  # Get inserts for the current construct
        for insert in construct_inserts:
            insert_location = inserts[insert]  # Get the location of the insert
            pipette_transfer(vol_per_insert, tube_rack[insert_location], tc_plate[construct_tube])
    
    pause(f"Place Assembly Mix in [{tube_rack[assembly_mix]}] and Buffer in [{tube_rack[buffer]}] and press RESUME.")

    # Distribute buffer and assembly mix to thermocycler tubes
    for index, construct_tube in enumerate(construct_tubes):
        pipette_transfer(vol_buffer, tube_rack[buffer], tc_plate[construct_tube])
        pipette_transfer(vol_assembly_mix, tube_rack[assembly_mix], tc_plate[construct_tube])

    tc_mod.close_lid()

    '''
    Thermocycler protocol based on BsaI test protocol, variables passed from script generation
    ----------------------
    Lid: inactivation_temp + 10C
    Volume: reaction_vol
    1. reaction_temp, 15min
    2. reaction_temp, 1.5min
    3. 16C, 3min
    4. GOTO step 2, 25x
    5. 50C, 10min
    6. inactivation_temp, 10min
    7. 4C, 1min, open lid
    '''    
    tc_mod.set_lid_temperature(temperature=(inactivation_temp + 10))
    tc_mod.set_block_temperature(temperature=reaction_temp, hold_time_seconds=900, block_max_volume=reaction_vol) # 15 min
    for i in range(25):
        tc_mod.set_block_temperature(temperature=reaction_temp, hold_time_seconds=90, block_max_volume=reaction_vol) # 1.5 min
        tc_mod.set_block_temperature(temperature=16, hold_time_seconds=180, block_max_volume=reaction_vol) # 3 min
    tc_mod.set_block_temperature(temperature=50, hold_time_seconds=300, block_max_volume=reaction_vol) # 10 min
    tc_mod.set_block_temperature(temperature=inactivation_temp, hold_time_seconds=600, block_max_volume=reaction_vol) # 10 min
    tc_mod.set_block_temperature(temperature=4, hold_time_seconds=60) # 1 min
    tc_mod.deactivate_lid() # Deactivate lid to allow for pipetting
    protocol.delay(seconds=5) # Wait for lid to cool down
    tc_mod.open_lid() # Open lid for pipetting

    
