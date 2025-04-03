import opentrons.execute # type: ignore
from opentrons import protocol_api # type: ignore
metadata = {"apiLevel": "2.16"}

rxn_vol = 50 # uL
reaction_temp = 37 # C
inactivation_temp = 65 # C

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

    # Initialize thermocycler
    tc_mod.open_lid()

    tc_mod.close_lid()

    '''
    BsaI test protocol
    ----------------------
    Lid: 75C
    Volume: 50uL
    1. 37C, 15min
    2. 37C, 1.5min
    3. 16C, 3min
    4. GOTO step 2, 25x
    5. 50C, 10min
    6. 65C, 10min
    7. 4C, hold
    '''
    tc_mod.set_lid_temperature(temperature=(inactivation_temp + 10))
    tc_mod.set_block_temperature(temperature=reaction_temp, hold_time_seconds=900, block_max_volume=rxn_vol) # 15 min
    for i in range(25):
        tc_mod.set_block_temperature(temperature=reaction_temp, hold_time_seconds=90, block_max_volume=rxn_vol) # 1.5 min
        tc_mod.set_block_temperature(temperature=16, hold_time_seconds=180, block_max_volume=rxn_vol) # 3 min
    tc_mod.set_block_temperature(temperature=50, hold_time_seconds=300, block_max_volume=rxn_vol) # 5 min
    tc_mod.set_block_temperature(temperature=inactivation_temp, hold_time_seconds=600, block_max_volume=rxn_vol) # 10 min
    tc_mod.set_block_temperature(temperature=4, hold_time_seconds=60) # 1 min
    tc_mod.deactivate_lid() # Deactivate lid to allow for pipetting
    protocol.delay(seconds=5) # Wait for lid to cool down
    tc_mod.open_lid() # Open lid for pipetting
