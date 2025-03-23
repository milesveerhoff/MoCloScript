from opentrons import protocol_api # type: ignore

metadata = {"apiLevel": "2.16"}

#tube rack locations of inserts
inserts = ["A1", "A2", "A3"]

#tube rack locations of reagents
backbone = "B1"
buffer = "B2"
assembly_mix = "B3"
h2o = "B4"

reagent_tubes = [backbone, buffer, assembly_mix]
for loc in inserts:
    reagent_tubes.append(loc)

#tube rack construct location
construct = "D6"

#define volumes, in ul
vol_backbone = 1
vol_buffer = 2
vol_assembly_mix = 1
vol_h2o = 20 - backbone - buffer - assembly_mix - sum(1 for i in inserts)

volumes = [vol_backbone, vol_buffer, vol_assembly_mix]
for vol in inserts:
    reagent_tubes.append(1)

def run(protocol: protocol_api.ProtocolContext):
    #define labware
    tips = protocol.load_labware("opentrons_flex_96_tiprack_200ul", "9")
    tube_rack = protocol.load_labware("opentrons_24_tuberack_nest_1.5ml_snapcap", "1")

    #initialize pipette
    pipette = protocol.load_instrument("p300_single_gen2", "right", tip_racks=[tips])

    #distribute water to tubes
    pipette.transfer(vol_h2o, tube_rack[h2o], tube_rack[construct]) 
    pipette.drop_tip()

    #distribute reagents to tubes
    for i in reagent_tubes:
        pipette.pick_up_tip()

        pipette.transfer(volumes[i], tube_rack[reagent_tubes[i]], tube_rack[construct])

        pipette.drop_tip()
    


