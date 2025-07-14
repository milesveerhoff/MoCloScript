import opentrons.execute # type: ignore
from opentrons import protocol_api # type: ignore
metadata = {"apiLevel": "2.22", "description": ''}

vol_per_stock = {'A1': 1.0, 'A2': 2.0, 'A3': 3.0, 'A4': 4.0, 'A5': 5.0, 'A6': 6.0, 'A7': 7.0, 'A8': 8.0, 'A9': 9.0, 'A10': 10.0, 'A11': 11.0, 'A12': 12.0, 'B1': 13.0, 'B2': 14.0, 'B3': 15.0, 'B4': 16.0, 'B5': 17.0, 'B6': 18.0, 'B7': 19.0, 'B8': 20.0, 'B9': 21.0, 'B10': 22.0, 'B11': 23.0, 'B12': 24.0, 'C1': 1.0, 'C2': 2.0, 'C3': 3.0, 'C4': 4.0, 'C5': 5.0, 'C6': 6.0, 'C7': 7.0, 'C8': 8.0, 'C9': 9.0, 'C10': 10.0, 'C11': 11.0, 'C12': 12.0, 'D1': 13.0, 'D2': 14.0, 'D3': 15.0, 'D4': 16.0, 'D5': 17.0, 'D6': 18.0, 'D7': 19.0, 'D8': 20.0, 'D9': 21.0, 'D10': 22.0, 'D11': 23.0, 'D12': 24.0, 'E1': 1.0, 'E2': 2.0, 'E3': 3.0, 'E4': 4.0, 'E5': 5.0, 'E6': 6.0, 'E7': 7.0, 'E8': 8.0, 'E9': 9.0, 'E10': 10.0, 'E11': 11.0, 'E12': 12.0, 'F1': 13.0, 'F2': 14.0, 'F3': 15.0, 'F4': 16.0, 'F5': 17.0, 'F6': 18.0, 'F7': 19.0, 'F8': 20.0, 'F9': 21.0, 'F10': 22.0, 'F11': 23.0, 'F12': 24.0, 'G1': 1.0, 'G2': 2.0, 'G3': 3.0, 'G4': 4.0, 'G5': 5.0, 'G6': 6.0, 'G7': 7.0, 'G8': 8.0, 'G9': 9.0, 'G10': 0.0, 'G11': 0.0, 'G12': 0.0, 'H1': 13.0, 'H2': 14.0, 'H3': 15.0, 'H4': 16.0, 'H5': 17.0, 'H6': 18.0, 'H7': 19.0, 'H8': 20.0, 'H9': 21.0, 'H10': 0.0, 'H11': 0.0, 'H12': 0.0}  # type: ignore

def run(ctx: protocol_api.ProtocolContext):
    # Load labware
    tips300= ctx.load_labware("opentrons_96_tiprack_300ul", "4")
    tips20 = ctx.load_labware("opentrons_96_tiprack_20ul", "5")
    stock_tubes = ctx.load_labware("nest_96_wellplate_100ul_pcr_full_skirt", "1")
    dilute_tubes = ctx.load_labware("nest_96_wellplate_100ul_pcr_full_skirt", "2")

    # Load pipettes
    p300 = ctx.load_instrument("p300_single_gen2", "right", tip_racks=[tips300])
    p20 = ctx.load_instrument("p20_single_gen2", "left", tip_racks=[tips20])

    def pipette_transfer(vol, source, dest, pipette=None):
        if pipette is not None:
            pipette.transfer(vol, source, dest, new_tip='always')
        else:
            if vol < 20:
                p20.transfer(vol, source, dest, new_tip='always')
            else:
                p300.transfer(vol, source, dest, new_tip='always')
                
    for stock, vol in vol_per_stock.items():
        # Transfer stock to dilute tubes
        if vol <= 0.0:
            continue
        else:
            pipette_transfer(vol, stock_tubes[stock], dilute_tubes[stock])
        # custom_mix(p20, dilute_tubes[stock], mixreps=5, vol=15, z_asp=1, z_disp_source_mix=4, z_disp_destination=4)
    
def custom_mix(pipette, well, mixreps=10, vol=20, z_asp=1, z_disp_source_mix=8, z_disp_destination=8):
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