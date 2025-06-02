import opentrons.execute # type: ignore
from opentrons import protocol_api # type: ignore
metadata = {{"apiLevel": "2.22", "description": '''{tube_placements}'''}}

# Fragments and constructs
inserts = {inserts} # type: ignore
constructs = {constructs} # type: ignore

# Tube rack locations of reagents
master_mix = {master_mix} # type: ignore
reagent_tubes = [master_mix] + list(inserts.values())

# Construct Tube Locations
construct_tubes = {construct_tubes} # type: ignore

# Define volumes, in uL
vol_master_mix_per_reaction = {vol_master_mix_per_reaction} # type: ignore
vol_per_insert = {vol_per_insert} # type: ignore

# Thermocycler settings
reaction_temp = {reaction_temp} # type: ignore
inactivation_temp = {inactivation_temp} # type: ignore
reaction_vol = 40 # Total volume of the reaction

def run(protocol: protocol_api.ProtocolContext):
    # --- TIP USAGE CHECK & TIPRACK LOADING ---
    num_master_mix_transfers = len(construct_tubes)
    num_insert_transfers = sum(len(construct) for construct in constructs)
    total_p20_tips = num_insert_transfers + sum(1 for v in vol_master_mix_per_reaction if v < 20)
    total_p300_tips = sum(1 for v in vol_master_mix_per_reaction if v >= 20)

    # Calculate how many tip racks are needed (each rack has 96 tips)
    num_p20_racks = (total_p20_tips - 1) // 96 + 1 if total_p20_tips > 0 else 1
    num_p300_racks = (total_p300_tips - 1) // 96 + 1 if total_p300_tips > 0 else 1

    # Assign deck slots for tip racks (avoid slots 1, 2, 4, 7 for labware/modules)
    available_slots = ["3", "5", "6", "8", "10", "11"]
    p20_slots = available_slots[:num_p20_racks]
    p300_slots = available_slots[num_p20_racks:num_p20_racks+num_p300_racks]

    # Load tip racks
    tips20_racks = [protocol.load_labware("opentrons_96_tiprack_20ul", slot) for slot in p20_slots]
    tips300_racks = [protocol.load_labware("opentrons_96_tiprack_300ul", slot) for slot in p300_slots]

    # Load other labware
    tube_rack = protocol.load_labware("opentrons_24_tuberack_nest_1.5ml_snapcap", "1")
    use_reservoir_for_mm = sum(vol_master_mix_per_reaction) > 1000
    if use_reservoir_for_mm:
        master_mix_reservoir = protocol.load_labware("nest_12_reservoir_15ml", "5")  # Use slot 5 for master mix
    tc_mod = protocol.load_module(module_name="thermocyclerModuleV2")
    tc_plate = tc_mod.load_labware(name="opentrons_96_wellplate_200ul_pcr_full_skirt")
    temp_mod = protocol.load_module(
        module_name="temperature module gen2", location="4"
    )
    temp_tubes = temp_mod.load_labware(
        "opentrons_24_aluminumblock_nest_1.5ml_screwcap"
    )
    # Load MYT plate if needed
    try:
        myt_plate = protocol.load_labware("opentrons_96_wellplate_200ul_pcr_full_skirt", "2")
    except Exception:
        myt_plate = None

    # Initialize pipettes with all loaded tip racks
    p300 = protocol.load_instrument("p300_single_gen2", "right", tip_racks=tips300_racks)
    p20 = protocol.load_instrument("p20_single_gen2", "left", tip_racks=tips20_racks)

    # --- TIP USAGE CHECK ---
    num_master_mix_transfers = len(construct_tubes)
    num_insert_transfers = sum(len(construct) for construct in constructs)
    total_p20_tips = num_insert_transfers + sum(1 for v in vol_master_mix_per_reaction if v < 20)
    total_p300_tips = sum(1 for v in vol_master_mix_per_reaction if v >= 20)
    if total_p20_tips > 96 or total_p300_tips > 96:
        raise Exception(
            f"Not enough tips: Need {total_p20_tips} x 20uL tips and {total_p300_tips} x 300uL tips, "
            "but only 96 of each are loaded. Please add more tip racks or reduce the number of reactions."
        )

    # Initialize thermocycler
    tc_mod.open_lid()

    # Pipette transfer function to handle both pipettes
    def pipette_transfer(vol, source, dest, pipette=None):
        if pipette is not None:
            pipette.transfer(vol, source, dest)
        else:
            if vol < 20:
                p20.transfer(vol, source, dest)
            else:
                p300.transfer(vol, source, dest)

    # Blink and pause function
    def pause(message):
        for i in range(3):
            protocol.set_rail_lights(False)
            protocol.delay(seconds=0.3)
            protocol.set_rail_lights(True)
            protocol.delay(seconds=0.3)
        protocol.set_rail_lights(True)
        protocol.pause(message)

    # Distribute master mix to tubes
    for index, construct_tube in enumerate(construct_tubes):
        # Use reservoir for MM if total MM volume > 1000 uL, else use tube_rack as before
        if use_reservoir_for_mm:
            if isinstance(master_mix, (tuple, list)):
                _, well = master_mix
                pipette_transfer(vol_master_mix_per_reaction[index], master_mix_reservoir[well], tc_plate[construct_tube])
            else:
                pipette_transfer(vol_master_mix_per_reaction[index], master_mix_reservoir[master_mix], tc_plate[construct_tube])
        else:
            if isinstance(master_mix, (tuple, list)):
                plate_type, well = master_mix
                if plate_type == "myt_plate" and myt_plate is not None:
                    pipette_transfer(vol_master_mix_per_reaction[index], myt_plate[well], tc_plate[construct_tube])
                else:
                    pipette_transfer(vol_master_mix_per_reaction[index], tube_rack[well], tc_plate[construct_tube])
            else:
                pipette_transfer(vol_master_mix_per_reaction[index], tube_rack[master_mix], tc_plate[construct_tube])

    # Distribute inserts to tubes based on the corresponding inserts from the constructs CSV file
    for index, construct_tube in enumerate(construct_tubes):
        construct_inserts = constructs[index]  # Get inserts for the current construct
        for insert in construct_inserts:
            insert_location = inserts[insert]
            # Decide which plate to use for each insert
            if isinstance(insert_location, tuple) or isinstance(insert_location, list):
                # If insert_location is a tuple/list: (plate_type, well)
                plate_type, well = insert_location
                if plate_type == "myt_plate" and myt_plate is not None:
                    pipette_transfer(vol_per_insert, myt_plate[well], tc_plate[construct_tube])
                else:
                    pipette_transfer(vol_per_insert, tube_rack[well], tc_plate[construct_tube])
            else:
                # Default: use tube rack
                pipette_transfer(vol_per_insert, tube_rack[insert_location], tc_plate[construct_tube])

    pause(f"Place Master Mix in [{{tube_rack[master_mix]}}] and press continue. Thermocycler protocol will begin after pipetting.")

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
    7. 4C, 1 hour, open lid
    '''    
    tc_mod.set_lid_temperature(temperature=(inactivation_temp + 10))
    tc_mod.set_block_temperature(temperature=reaction_temp, hold_time_seconds=900, block_max_volume=reaction_vol) # 15 min
    for i in range(25):
        tc_mod.set_block_temperature(temperature=reaction_temp, hold_time_seconds=90, block_max_volume=reaction_vol) # 1.5 min
        tc_mod.set_block_temperature(temperature=16, hold_time_seconds=180, block_max_volume=reaction_vol) # 3 min
    tc_mod.set_block_temperature(temperature=50, hold_time_seconds=300, block_max_volume=reaction_vol) # 10 min
    tc_mod.set_block_temperature(temperature=inactivation_temp, hold_time_seconds=600, block_max_volume=reaction_vol) # 10 min
    tc_mod.set_block_temperature(temperature=4, hold_time_seconds=3600) # 1 hour
    tc_mod.deactivate_lid() # Deactivate lid to allow for pipetting
    protocol.delay(seconds=5) # Wait for lid to cool down

    pause("Thermocycler protocol complete. Press continue to open thermocycler lid.")
    tc_mod.open_lid() # Open lid for pipetting


