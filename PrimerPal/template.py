import opentrons.execute # type: ignore
from opentrons import protocol_api # type: ignore
metadata = {"apiLevel": "2.22", "description": '''Primer Pal oligo dilution!'''}

vol_per_oligo = {oligo_values}  # type: ignore

def run(ctx: protocol_api.ProtocolContext):
    # Load labware
    tips300= ctx.load_labware("opentrons_96_tiprack_300ul", "4")
    tips20 = ctx.load_labware("opentrons_96_tiprack_20ul", "5")
    oligo_tubes = ctx.load_labware("opentrons_24_tuberack_generic_2ml_screwcap", "1")
    working_tubes = ctx.load_labware("opentrons_24_tuberack_nest_1.5ml_snapcap", "2")
    water_res = ctx.load_labware("opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical", "3")

    # Load pipettes
    p300 = ctx.load_instrument("p300_single_gen2", "right", tip_racks=[tips300])
    p20 = ctx.load_instrument("p20_single_gen2", "left", tip_racks=[tips20])

    working_tubes_loc = [loc for loc in vol_per_oligo]

    # Transfer water to working tubes
    p300.pick_up_tip()
    p300.distribute(45, water_res['A1'], [working_tubes[loc] for loc in working_tubes_loc], new_tip='never')
    p300.drop_tip()

    for oligo, vol in vol_per_oligo.items():
        # Transfer water to oligo tubes
        p300.pick_up_tip()
        p300.transfer(vol, water_res['A1'], oligo_tubes[oligo], new_tip='never', drop_tip=False)
        custom_mix(p300, oligo_tubes[oligo], mixreps=3, vol=(vol * 0.75), z_asp=1, z_disp_source_mix=8, z_disp_destination=8)
        p300.drop_tip()

    for oligo in vol_per_oligo:
        # Transfer oligo to working tubes
        p20.pick_up_tip()
        p20.transfer(5, oligo_tubes[oligo], working_tubes[working_tubes_loc[0]], new_tip='never', drop_tip=False)
        custom_mix(p20, working_tubes[working_tubes_loc[0]], mixreps=3, vol=15, z_asp=1, z_disp_source_mix=8, z_disp_destination=8)
        p20.drop_tip()
    
def custom_mix(pipette, well, mixreps=3, vol=20, z_asp=1, z_disp_source_mix=8, z_disp_destination=8):
    # Save original flow rates
    orig_asp = pipette.flow_rate.aspirate
    orig_disp = pipette.flow_rate.dispense
    # Increase flow rates for mixing
    pipette.flow_rate.aspirate *= 4
    pipette.flow_rate.dispense *= 6
    for _ in range(mixreps):
        pipette.aspirate(vol, well.bottom(z_asp))
        pipette.dispense(vol, well.bottom(z_disp_source_mix))
    # Restore original flow rates BEFORE blow out
    pipette.flow_rate.aspirate = orig_asp
    pipette.flow_rate.dispense = orig_disp
    # Blow out just above the bottom to help droplet detach
    pipette.blow_out(well.bottom(z_disp_destination + 2))
    # Touch tip to the well wall to remove any droplet
    pipette.touch_tip(well)

