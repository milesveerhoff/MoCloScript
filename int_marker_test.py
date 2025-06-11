import opentrons.execute # type: ignore
from opentrons import protocol_api # type: ignore
metadata = {"apiLevel": "2.22", "description": '''[C7] (MYT Plate): pMYT031_nan_HIS3, 
[C8] (MYT Plate): pMYT032_nan_TRP1, 
[C12] (MYT Plate): pMYT036_nan_NatR, 
[D1] (MYT Plate): pMYT037_nan_HygR, 
[G9] (MYT Plate): pMYT081_nan_Int7_Vector, 
[G11] (MYT Plate): pMYT083_nan_Int9_Vector, 

[A1]: Master Mix (MM), 

Constructs will be built at the following locations in the thermocycler module:
[A1]: pMYT081_nan_Int7_Vector-pMYT031_nan_HIS3, 
[A2]: pMYT081_nan_Int7_Vector-pMYT032_nan_TRP1, 
[A3]: pMYT081_nan_Int7_Vector-pMYT036_nan_NatR, 
[A4]: pMYT081_nan_Int7_Vector-pMYT037_nan_HygR, 
[A5]: pMYT083_nan_Int9_Vector-pMYT031_nan_HIS3, 
[A6]: pMYT083_nan_Int9_Vector-pMYT032_nan_TRP1, 
[A7]: pMYT083_nan_Int9_Vector-pMYT036_nan_NatR, 
[A8]: pMYT083_nan_Int9_Vector-pMYT037_nan_HygR, '''}

# Fragments and constructs
inserts = {'pMYT031_nan_HIS3': ('myt_plate', 'C7'), 'pMYT032_nan_TRP1': ('myt_plate', 'C8'), 'pMYT036_nan_NatR': ('myt_plate', 'C12'), 'pMYT037_nan_HygR': ('myt_plate', 'D1'), 'pMYT081_nan_Int7_Vector': ('myt_plate', 'G9'), 'pMYT083_nan_Int9_Vector': ('myt_plate', 'G11')} # type: ignore
constructs = [['pMYT081_nan_Int7_Vector', 'pMYT031_nan_HIS3'], ['pMYT081_nan_Int7_Vector', 'pMYT032_nan_TRP1'], ['pMYT081_nan_Int7_Vector', 'pMYT036_nan_NatR'], ['pMYT081_nan_Int7_Vector', 'pMYT037_nan_HygR'], ['pMYT083_nan_Int9_Vector', 'pMYT031_nan_HIS3'], ['pMYT083_nan_Int9_Vector', 'pMYT032_nan_TRP1'], ['pMYT083_nan_Int9_Vector', 'pMYT036_nan_NatR'], ['pMYT083_nan_Int9_Vector', 'pMYT037_nan_HygR']] # type: ignore

# Tube rack locations of reagents
master_mix = 'A1' # type: ignore
reagent_tubes = [master_mix] + list(inserts.values())

# Construct Tube Locations
construct_tubes = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8'] # type: ignore

# Define volumes, in uL
vol_master_mix_per_reaction = [11] * len(construct_tubes)  # 11 uL master mix per well

# Insert volumes: dictionary mapping insert name to volume (uL)
vol_per_insert_dict = {
    'pMYT031_nan_HIS3': 3.68,
    'pMYT032_nan_TRP1': 4.21,
    'pMYT036_nan_NatR': 3.12,
    'pMYT037_nan_HygR': 5.57,
    'pMYT081_nan_Int7_Vector': 5.94,
    'pMYT083_nan_Int9_Vector': 6.89
} # type: ignore

# Thermocycler settings
reaction_temp = 37 # type: ignore
inactivation_temp = 65 # type: ignore
reaction_vol = 30 # Total volume of the reaction

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
    # tube_rack = protocol.load_labware("opentrons_24_tuberack_nest_1.5ml_snapcap", "1")
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
    tube_rack = temp_tubes
    # Load MYT plate if needed
    try:
        myt_plate = protocol.load_labware("nest_96_wellplate_200ul_flat", "2")
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
            f"Not enough tips: Need 16 x 20uL tips and 8 x 300uL tips, "
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

    # Distribute master mix to tubes using multi-dispense (one tip per batch)
    def distribute_master_mix(volumes, source, dest_wells, pipette):
        """
        volumes: list of volumes to dispense to each destination
        source: source well
        dest_wells: list of destination wells
        pipette: pipette object (p20 or p300)
        """
        pipette.pick_up_tip()
        for vol, dest in zip(volumes, dest_wells):
            pipette.aspirate(vol, source)
            pipette.dispense(vol, dest)
        pipette.drop_tip()

    # Decide which pipette to use for each batch based on volume
    # Group wells by pipette type (p20 for <20uL, p300 for >=20uL)
    wells_p20 = []
    vols_p20 = []
    wells_p300 = []
    vols_p300 = []
    for idx, vol in enumerate(vol_master_mix_per_reaction):
        if vol < 20:
            wells_p20.append(tc_plate[construct_tubes[idx]])
            vols_p20.append(vol)
        else:
            wells_p300.append(tc_plate[construct_tubes[idx]])
            vols_p300.append(vol)

    # Use the correct source for master mix
    if use_reservoir_for_mm:
        mm_source = master_mix_reservoir[master_mix] if not isinstance(master_mix, (tuple, list)) else master_mix_reservoir[master_mix[1]]
    else:
        if isinstance(master_mix, (tuple, list)):
            plate_type, well = master_mix
            if plate_type == "myt_plate" and myt_plate is not None:
                mm_source = myt_plate[well]
            else:
                mm_source = tube_rack[well]
        else:
            mm_source = tube_rack[master_mix]

    # Distribute 11 uL master mix to each well
    if wells_p20:
        distribute_master_mix(vols_p20, mm_source, wells_p20, p20)
    if wells_p300:
        distribute_master_mix(vols_p300, mm_source, wells_p300, p300)

    # First, add water to each well that needs it (after master mix, before inserts), using a single tip
    wells_needing_water = []
    water_vols = []
    for index, construct_tube in enumerate(construct_tubes):
        construct_inserts = constructs[index]
        total_insert_vol = sum(vol_per_insert_dict.get(insert, 4.5) for insert in construct_inserts)
        if total_insert_vol < 19:
            wells_needing_water.append(tc_plate[construct_tube])
            water_vols.append(19 - total_insert_vol)
    if wells_needing_water:
        p20.pick_up_tip()
        for vol, dest in zip(water_vols, wells_needing_water):
            p20.transfer(vol, tube_rack['A2'], dest, new_tip='never')
        p20.drop_tip()

    # Now add inserts to each well
    for index, construct_tube in enumerate(construct_tubes):
        construct_inserts = constructs[index]  # Get inserts for the current construct
        for insert in construct_inserts:
            insert_location = inserts[insert]
            insert_vol = vol_per_insert_dict.get(insert, 5)  # Default to 4.5 if not found
            # Decide which plate to use for each insert
            if isinstance(insert_location, tuple) or isinstance(insert_location, list):
                plate_type, well = insert_location
                if plate_type == "myt_plate" and myt_plate is not None:
                    pipette_transfer(insert_vol, myt_plate[well], tc_plate[construct_tube])
                else:
                    pipette_transfer(insert_vol, tube_rack[well], tc_plate[construct_tube])
            else:
                pipette_transfer(insert_vol, tube_rack[insert_location], tc_plate[construct_tube])

    # pause("Thermocycler protocol will begin after pipetting.")

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


