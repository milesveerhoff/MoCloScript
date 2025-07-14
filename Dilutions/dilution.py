import opentrons.execute # type: ignore
from opentrons import protocol_api # type: ignore
metadata = {"apiLevel": "2.22", "description": ''}

vol_per_stock = {'A1': 300.0, 'A2': 297.0, 'A3': 294.0, 'A4': 0.0, 'A5': 288.0, 'A6': 285.0, 'A7': 282.0, 'A8': 279.0, 'A9': 276.0, 'A10': 273.0, 'A11': 0.0, 'A12': 267.0, 'B1': 0.0, 'B2': 0.0, 'B3': 0.0, 'B4': 0.0, 'B5': 0.0, 'B6': 0.0, 'B7': 0.0, 'B8': 0.0, 'B9': 0.0, 'B10': 0.0, 'B11': 0.0, 'B12': 0.0, 'C1': 228.0, 'C2': 225.0, 'C3': 222.0, 'C4': 0.0, 'C5': 216.0, 'C6': 213.0, 'C7': 210.0, 'C8': 207.0, 'C9': 204.0, 'C10': 201.0, 'C11': 0.0, 'C12': 195.0, 'D1': 192.0, 'D2': 189.0, 'D3': 186.0, 'D4': 0.0, 'D5': 180.0, 'D6': 177.0, 'D7': 174.0, 'D8': 171.0, 'D9': 168.0, 'D10': 165.0, 'D11': 0.0, 'D12': 159.0, 'E1': 156.0, 'E2': 153.0, 'E3': 150.0, 'E4': 0.0, 'E5': 144.0, 'E6': 141.0, 'E7': 138.0, 'E8': 135.0, 'E9': 132.0, 'E10': 129.0, 'E11': 0.0, 'E12': 123.0, 'F1': 120.0, 'F2': 117.0, 'F3': 114.0, 'F4': 0.0, 'F5': 108.0, 'F6': 105.0, 'F7': 102.0, 'F8': 99.0, 'F9': 96.0, 'F10': 93.0, 'F11': 0.0, 'F12': 87.0, 'G1': 84.0, 'G2': 81.0, 'G3': 78.0, 'G4': 0.0, 'G5': 72.0, 'G6': 69.0, 'G7': 66.0, 'G8': 63.0, 'G9': 60.0, 'G10': 57.0, 'G11': 0.0, 'G12': 51.0, 'H1': 48.0, 'H2': 45.0, 'H3': 42.0, 'H4': 0.0, 'H5': 36.0, 'H6': 33.0, 'H7': 30.0, 'H8': 27.0, 'H9': 24.0, 'H10': 21.0, 'H11': 0.0, 'H12': 15.0}  # type: ignore

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