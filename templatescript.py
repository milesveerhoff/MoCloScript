import opentrons.execute # type: ignore
from opentrons import protocol_api # type: ignore
metadata = {{"apiLevel": "2.16", "description": '''{tube_placements}'''}}
# Fragments and constructs
inserts = {inserts}
constructs = {constructs}
# Tube rack locations of reagents
buffer = "{buffer}"
assembly_mix = "{assembly_mix}"
h2o = "{h2o}"
reagent_tubes = [buffer, assembly_mix, h2o] + list(inserts.values())
# Reaction Tube Locations
construct_tubes = {construct_tubes}
# Define volumes, in uL
vol_buffer = 1
vol_assembly_mix = 1
vol_h2o = {vol_h2o}
vol_per_insert = {vol_per_insert}
volumes = [vol_buffer, vol_assembly_mix] + [vol_per_insert] * len(inserts)
def run(protocol: protocol_api.ProtocolContext):
    # Define labware
    tips300 = protocol.load_labware("opentrons_96_tiprack_300ul", "9")
    tips20 = protocol.load_labware("opentrons_96_tiprack_20ul", "6")
    tube_rack = protocol.load_labware("opentrons_24_tuberack_nest_1.5ml_snapcap", "1")
    tc_mod = protocol.load_module(module_name="thermocyclerModuleV2")
    plate = tc_mod.load_labware(name="opentrons_96_wellplate_200ul_pcr_full_skirt")
    temp_mod = protocol.load_module(
    module_name="temperature module gen2", location="4"
    )
    temp_tubes = temp_mod.load_labware(
    "opentrons_24_aluminumblock_nest_1.5ml_screwcap"
    )

    # Initialize pipettes
    p300 = protocol.load_instrument("p300_single_gen2", "right", tip_racks=[tips300])
    p20 = protocol.load_instrument("p20_single_gen2", "left", tip_racks=[tips20])

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
        pipette_transfer(vol_h2o[index], tube_rack[h2o], tube_rack[construct_tube])
    # Distribute reagents to tubes based on the corresponding inserts from the constructs CSV file
    for index, construct_tube in enumerate(construct_tubes):
        construct_inserts = constructs[index]  # Get inserts for the current construct
        for insert in construct_inserts:
            insert_location = inserts[insert]  # Get the location of the insert
            pipette_transfer(vol_per_insert, tube_rack[insert_location], tube_rack[construct_tube])
    # Blink lights then pause
    for i in range(3):
        protocol.set_rail_lights(False)
        protocol.delay(seconds=0.5)
        protocol.set_rail_lights(True)
        protocol.delay(seconds=0.5)
    protocol.set_rail_lights(True)
    protocol.pause("test prompt")
    # Distribute buffer and assembly mix to tubes
    for index, construct_tube in enumerate(construct_tubes):
        pipette_transfer(vol_buffer, tube_rack[buffer], tube_rack[construct_tube])
        pipette_transfer(vol_assembly_mix, tube_rack[assembly_mix], tube_rack[construct_tube])