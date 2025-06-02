import opentrons.execute # type: ignore
from opentrons import protocol_api # type: ignore
metadata = {"apiLevel": "2.22", "description": '''[G3] (MYT Plate): pMYT075_nan_Int1_Vector, 
[G5] (MYT Plate): pMYT077_nan_Int3_Vector, 
[G6] (MYT Plate): pMYT078_nan_Int4_Vector, 
[G7] (MYT Plate): pMYT079_nan_Int5_Vector, 
[G8] (MYT Plate): pMYT080_nan_Int6_Vector, 
[G9] (MYT Plate): pMYT081_nan_Int7_Vector, 
[G10] (MYT Plate): pMYT082_nan_Int8_Vector, 
[G11] (MYT Plate): pMYT083_nan_Int9_Vector, 
[G12] (MYT Plate): pMYT084_nan_Int10_Vector, 
[C5] (MYT Plate): pMYT029_nan_URA3, 
[C6] (MYT Plate): pMYT030_nan_LEU2, 
[C7] (MYT Plate): pMYT031_nan_HIS3, 
[C8] (MYT Plate): pMYT032_nan_TRP1, 
[C9] (MYT Plate): pMYT033_nan_MET17, 
[C10] (MYT Plate): pMYT034_nan_LYS2, 
[C11] (MYT Plate): pMYT035_nan_KanR, 
[C12] (MYT Plate): pMYT036_nan_NatR, 
[D1] (MYT Plate): pMYT037_nan_HygR, 
[D2] (MYT Plate): pMYT038_nan_ZeoR, 

[A1]: Master Mix (MM), 

Constructs will be built at the following locations in the thermocycler module:
[A1]: pMYT075_nan_Int1_Vector-pMYT029_nan_URA3, 
[A2]: pMYT075_nan_Int1_Vector-pMYT030_nan_LEU2, 
[A3]: pMYT075_nan_Int1_Vector-pMYT031_nan_HIS3, 
[A4]: pMYT075_nan_Int1_Vector-pMYT032_nan_TRP1, 
[A5]: pMYT075_nan_Int1_Vector-pMYT033_nan_MET17, 
[A6]: pMYT075_nan_Int1_Vector-pMYT034_nan_LYS2, 
[A7]: pMYT075_nan_Int1_Vector-pMYT035_nan_KanR, 
[A8]: pMYT075_nan_Int1_Vector-pMYT036_nan_NatR, 
[A9]: pMYT075_nan_Int1_Vector-pMYT037_nan_HygR, 
[A10]: pMYT075_nan_Int1_Vector-pMYT038_nan_ZeoR, 
[A11]: pMYT077_nan_Int3_Vector-pMYT029_nan_URA3, 
[A12]: pMYT077_nan_Int3_Vector-pMYT030_nan_LEU2, 
[B1]: pMYT077_nan_Int3_Vector-pMYT031_nan_HIS3, 
[B2]: pMYT077_nan_Int3_Vector-pMYT032_nan_TRP1, 
[B3]: pMYT077_nan_Int3_Vector-pMYT033_nan_MET17, 
[B4]: pMYT077_nan_Int3_Vector-pMYT034_nan_LYS2, 
[B5]: pMYT077_nan_Int3_Vector-pMYT035_nan_KanR, 
[B6]: pMYT077_nan_Int3_Vector-pMYT036_nan_NatR, 
[B7]: pMYT077_nan_Int3_Vector-pMYT037_nan_HygR, 
[B8]: pMYT077_nan_Int3_Vector-pMYT038_nan_ZeoR, 
[B9]: pMYT078_nan_Int4_Vector-pMYT029_nan_URA3, 
[B10]: pMYT078_nan_Int4_Vector-pMYT030_nan_LEU2, 
[B11]: pMYT078_nan_Int4_Vector-pMYT031_nan_HIS3, 
[B12]: pMYT078_nan_Int4_Vector-pMYT032_nan_TRP1, 
[C1]: pMYT078_nan_Int4_Vector-pMYT033_nan_MET17, 
[C2]: pMYT078_nan_Int4_Vector-pMYT034_nan_LYS2, 
[C3]: pMYT078_nan_Int4_Vector-pMYT035_nan_KanR, 
[C4]: pMYT078_nan_Int4_Vector-pMYT036_nan_NatR, 
[C5]: pMYT078_nan_Int4_Vector-pMYT037_nan_HygR, 
[C6]: pMYT078_nan_Int4_Vector-pMYT038_nan_ZeoR, 
[C7]: pMYT079_nan_Int5_Vector-pMYT029_nan_URA3, 
[C8]: pMYT079_nan_Int5_Vector-pMYT030_nan_LEU2, 
[C9]: pMYT079_nan_Int5_Vector-pMYT031_nan_HIS3, 
[C10]: pMYT079_nan_Int5_Vector-pMYT032_nan_TRP1, 
[C11]: pMYT079_nan_Int5_Vector-pMYT033_nan_MET17, 
[C12]: pMYT079_nan_Int5_Vector-pMYT034_nan_LYS2, 
[D1]: pMYT079_nan_Int5_Vector-pMYT035_nan_KanR, 
[D2]: pMYT079_nan_Int5_Vector-pMYT036_nan_NatR, 
[D3]: pMYT079_nan_Int5_Vector-pMYT037_nan_HygR, 
[D4]: pMYT079_nan_Int5_Vector-pMYT038_nan_ZeoR, 
[D5]: pMYT080_nan_Int6_Vector-pMYT029_nan_URA3, 
[D6]: pMYT080_nan_Int6_Vector-pMYT030_nan_LEU2, 
[D7]: pMYT080_nan_Int6_Vector-pMYT031_nan_HIS3, 
[D8]: pMYT080_nan_Int6_Vector-pMYT032_nan_TRP1, 
[D9]: pMYT080_nan_Int6_Vector-pMYT033_nan_MET17, 
[D10]: pMYT080_nan_Int6_Vector-pMYT034_nan_LYS2, 
[D11]: pMYT080_nan_Int6_Vector-pMYT035_nan_KanR, 
[D12]: pMYT080_nan_Int6_Vector-pMYT036_nan_NatR, 
[E1]: pMYT080_nan_Int6_Vector-pMYT037_nan_HygR, 
[E2]: pMYT080_nan_Int6_Vector-pMYT038_nan_ZeoR, 
[E3]: pMYT081_nan_Int7_Vector-pMYT029_nan_URA3, 
[E4]: pMYT081_nan_Int7_Vector-pMYT030_nan_LEU2, 
[E5]: pMYT081_nan_Int7_Vector-pMYT031_nan_HIS3, 
[E6]: pMYT081_nan_Int7_Vector-pMYT032_nan_TRP1, 
[E7]: pMYT081_nan_Int7_Vector-pMYT033_nan_MET17, 
[E8]: pMYT081_nan_Int7_Vector-pMYT034_nan_LYS2, 
[E9]: pMYT081_nan_Int7_Vector-pMYT035_nan_KanR, 
[E10]: pMYT081_nan_Int7_Vector-pMYT036_nan_NatR, 
[E11]: pMYT081_nan_Int7_Vector-pMYT037_nan_HygR, 
[E12]: pMYT081_nan_Int7_Vector-pMYT038_nan_ZeoR, 
[F1]: pMYT082_nan_Int8_Vector-pMYT029_nan_URA3, 
[F2]: pMYT082_nan_Int8_Vector-pMYT030_nan_LEU2, 
[F3]: pMYT082_nan_Int8_Vector-pMYT031_nan_HIS3, 
[F4]: pMYT082_nan_Int8_Vector-pMYT032_nan_TRP1, 
[F5]: pMYT082_nan_Int8_Vector-pMYT033_nan_MET17, 
[F6]: pMYT082_nan_Int8_Vector-pMYT034_nan_LYS2, 
[F7]: pMYT082_nan_Int8_Vector-pMYT035_nan_KanR, 
[F8]: pMYT082_nan_Int8_Vector-pMYT036_nan_NatR, 
[F9]: pMYT082_nan_Int8_Vector-pMYT037_nan_HygR, 
[F10]: pMYT082_nan_Int8_Vector-pMYT038_nan_ZeoR, 
[F11]: pMYT083_nan_Int9_Vector-pMYT029_nan_URA3, 
[F12]: pMYT083_nan_Int9_Vector-pMYT030_nan_LEU2, 
[G1]: pMYT083_nan_Int9_Vector-pMYT031_nan_HIS3, 
[G2]: pMYT083_nan_Int9_Vector-pMYT032_nan_TRP1, 
[G3]: pMYT083_nan_Int9_Vector-pMYT033_nan_MET17, 
[G4]: pMYT083_nan_Int9_Vector-pMYT034_nan_LYS2, 
[G5]: pMYT083_nan_Int9_Vector-pMYT035_nan_KanR, 
[G6]: pMYT083_nan_Int9_Vector-pMYT036_nan_NatR, 
[G7]: pMYT083_nan_Int9_Vector-pMYT037_nan_HygR, 
[G8]: pMYT083_nan_Int9_Vector-pMYT038_nan_ZeoR, 
[G9]: pMYT084_nan_Int10_Vector-pMYT029_nan_URA3, 
[G10]: pMYT084_nan_Int10_Vector-pMYT030_nan_LEU2, 
[G11]: pMYT084_nan_Int10_Vector-pMYT031_nan_HIS3, 
[G12]: pMYT084_nan_Int10_Vector-pMYT032_nan_TRP1, 
[H1]: pMYT084_nan_Int10_Vector-pMYT033_nan_MET17, 
[H2]: pMYT084_nan_Int10_Vector-pMYT034_nan_LYS2, 
[H3]: pMYT084_nan_Int10_Vector-pMYT035_nan_KanR, 
[H4]: pMYT084_nan_Int10_Vector-pMYT036_nan_NatR, 
[H5]: pMYT084_nan_Int10_Vector-pMYT037_nan_HygR, 
[H6]: pMYT084_nan_Int10_Vector-pMYT038_nan_ZeoR, '''}

# Fragments and constructs
inserts = {'pMYT075_nan_Int1_Vector': ('myt_plate', 'G3'), 'pMYT077_nan_Int3_Vector': ('myt_plate', 'G5'), 'pMYT078_nan_Int4_Vector': ('myt_plate', 'G6'), 'pMYT079_nan_Int5_Vector': ('myt_plate', 'G7'), 'pMYT080_nan_Int6_Vector': ('myt_plate', 'G8'), 'pMYT081_nan_Int7_Vector': ('myt_plate', 'G9'), 'pMYT082_nan_Int8_Vector': ('myt_plate', 'G10'), 'pMYT083_nan_Int9_Vector': ('myt_plate', 'G11'), 'pMYT084_nan_Int10_Vector': ('myt_plate', 'G12'), 'pMYT029_nan_URA3': ('myt_plate', 'C5'), 'pMYT030_nan_LEU2': ('myt_plate', 'C6'), 'pMYT031_nan_HIS3': ('myt_plate', 'C7'), 'pMYT032_nan_TRP1': ('myt_plate', 'C8'), 'pMYT033_nan_MET17': ('myt_plate', 'C9'), 'pMYT034_nan_LYS2': ('myt_plate', 'C10'), 'pMYT035_nan_KanR': ('myt_plate', 'C11'), 'pMYT036_nan_NatR': ('myt_plate', 'C12'), 'pMYT037_nan_HygR': ('myt_plate', 'D1'), 'pMYT038_nan_ZeoR': ('myt_plate', 'D2')} # type: ignore
constructs = [['pMYT075_nan_Int1_Vector', 'pMYT029_nan_URA3'], ['pMYT075_nan_Int1_Vector', 'pMYT030_nan_LEU2'], ['pMYT075_nan_Int1_Vector', 'pMYT031_nan_HIS3'], ['pMYT075_nan_Int1_Vector', 'pMYT032_nan_TRP1'], ['pMYT075_nan_Int1_Vector', 'pMYT033_nan_MET17'], ['pMYT075_nan_Int1_Vector', 'pMYT034_nan_LYS2'], ['pMYT075_nan_Int1_Vector', 'pMYT035_nan_KanR'], ['pMYT075_nan_Int1_Vector', 'pMYT036_nan_NatR'], ['pMYT075_nan_Int1_Vector', 'pMYT037_nan_HygR'], ['pMYT075_nan_Int1_Vector', 'pMYT038_nan_ZeoR'], ['pMYT077_nan_Int3_Vector', 'pMYT029_nan_URA3'], ['pMYT077_nan_Int3_Vector', 'pMYT030_nan_LEU2'], ['pMYT077_nan_Int3_Vector', 'pMYT031_nan_HIS3'], ['pMYT077_nan_Int3_Vector', 'pMYT032_nan_TRP1'], ['pMYT077_nan_Int3_Vector', 'pMYT033_nan_MET17'], ['pMYT077_nan_Int3_Vector', 'pMYT034_nan_LYS2'], ['pMYT077_nan_Int3_Vector', 'pMYT035_nan_KanR'], ['pMYT077_nan_Int3_Vector', 'pMYT036_nan_NatR'], ['pMYT077_nan_Int3_Vector', 'pMYT037_nan_HygR'], ['pMYT077_nan_Int3_Vector', 'pMYT038_nan_ZeoR'], ['pMYT078_nan_Int4_Vector', 'pMYT029_nan_URA3'], ['pMYT078_nan_Int4_Vector', 'pMYT030_nan_LEU2'], ['pMYT078_nan_Int4_Vector', 'pMYT031_nan_HIS3'], ['pMYT078_nan_Int4_Vector', 'pMYT032_nan_TRP1'], ['pMYT078_nan_Int4_Vector', 'pMYT033_nan_MET17'], ['pMYT078_nan_Int4_Vector', 'pMYT034_nan_LYS2'], ['pMYT078_nan_Int4_Vector', 'pMYT035_nan_KanR'], ['pMYT078_nan_Int4_Vector', 'pMYT036_nan_NatR'], ['pMYT078_nan_Int4_Vector', 'pMYT037_nan_HygR'], ['pMYT078_nan_Int4_Vector', 'pMYT038_nan_ZeoR'], ['pMYT079_nan_Int5_Vector', 'pMYT029_nan_URA3'], ['pMYT079_nan_Int5_Vector', 'pMYT030_nan_LEU2'], ['pMYT079_nan_Int5_Vector', 'pMYT031_nan_HIS3'], ['pMYT079_nan_Int5_Vector', 'pMYT032_nan_TRP1'], ['pMYT079_nan_Int5_Vector', 'pMYT033_nan_MET17'], ['pMYT079_nan_Int5_Vector', 'pMYT034_nan_LYS2'], ['pMYT079_nan_Int5_Vector', 'pMYT035_nan_KanR'], ['pMYT079_nan_Int5_Vector', 'pMYT036_nan_NatR'], ['pMYT079_nan_Int5_Vector', 'pMYT037_nan_HygR'], ['pMYT079_nan_Int5_Vector', 'pMYT038_nan_ZeoR'], ['pMYT080_nan_Int6_Vector', 'pMYT029_nan_URA3'], ['pMYT080_nan_Int6_Vector', 'pMYT030_nan_LEU2'], ['pMYT080_nan_Int6_Vector', 'pMYT031_nan_HIS3'], ['pMYT080_nan_Int6_Vector', 'pMYT032_nan_TRP1'], ['pMYT080_nan_Int6_Vector', 'pMYT033_nan_MET17'], ['pMYT080_nan_Int6_Vector', 'pMYT034_nan_LYS2'], ['pMYT080_nan_Int6_Vector', 'pMYT035_nan_KanR'], ['pMYT080_nan_Int6_Vector', 'pMYT036_nan_NatR'], ['pMYT080_nan_Int6_Vector', 'pMYT037_nan_HygR'], ['pMYT080_nan_Int6_Vector', 'pMYT038_nan_ZeoR'], ['pMYT081_nan_Int7_Vector', 'pMYT029_nan_URA3'], ['pMYT081_nan_Int7_Vector', 'pMYT030_nan_LEU2'], ['pMYT081_nan_Int7_Vector', 'pMYT031_nan_HIS3'], ['pMYT081_nan_Int7_Vector', 'pMYT032_nan_TRP1'], ['pMYT081_nan_Int7_Vector', 'pMYT033_nan_MET17'], ['pMYT081_nan_Int7_Vector', 'pMYT034_nan_LYS2'], ['pMYT081_nan_Int7_Vector', 'pMYT035_nan_KanR'], ['pMYT081_nan_Int7_Vector', 'pMYT036_nan_NatR'], ['pMYT081_nan_Int7_Vector', 'pMYT037_nan_HygR'], ['pMYT081_nan_Int7_Vector', 'pMYT038_nan_ZeoR'], ['pMYT082_nan_Int8_Vector', 'pMYT029_nan_URA3'], ['pMYT082_nan_Int8_Vector', 'pMYT030_nan_LEU2'], ['pMYT082_nan_Int8_Vector', 'pMYT031_nan_HIS3'], ['pMYT082_nan_Int8_Vector', 'pMYT032_nan_TRP1'], ['pMYT082_nan_Int8_Vector', 'pMYT033_nan_MET17'], ['pMYT082_nan_Int8_Vector', 'pMYT034_nan_LYS2'], ['pMYT082_nan_Int8_Vector', 'pMYT035_nan_KanR'], ['pMYT082_nan_Int8_Vector', 'pMYT036_nan_NatR'], ['pMYT082_nan_Int8_Vector', 'pMYT037_nan_HygR'], ['pMYT082_nan_Int8_Vector', 'pMYT038_nan_ZeoR'], ['pMYT083_nan_Int9_Vector', 'pMYT029_nan_URA3'], ['pMYT083_nan_Int9_Vector', 'pMYT030_nan_LEU2'], ['pMYT083_nan_Int9_Vector', 'pMYT031_nan_HIS3'], ['pMYT083_nan_Int9_Vector', 'pMYT032_nan_TRP1'], ['pMYT083_nan_Int9_Vector', 'pMYT033_nan_MET17'], ['pMYT083_nan_Int9_Vector', 'pMYT034_nan_LYS2'], ['pMYT083_nan_Int9_Vector', 'pMYT035_nan_KanR'], ['pMYT083_nan_Int9_Vector', 'pMYT036_nan_NatR'], ['pMYT083_nan_Int9_Vector', 'pMYT037_nan_HygR'], ['pMYT083_nan_Int9_Vector', 'pMYT038_nan_ZeoR'], ['pMYT084_nan_Int10_Vector', 'pMYT029_nan_URA3'], ['pMYT084_nan_Int10_Vector', 'pMYT030_nan_LEU2'], ['pMYT084_nan_Int10_Vector', 'pMYT031_nan_HIS3'], ['pMYT084_nan_Int10_Vector', 'pMYT032_nan_TRP1'], ['pMYT084_nan_Int10_Vector', 'pMYT033_nan_MET17'], ['pMYT084_nan_Int10_Vector', 'pMYT034_nan_LYS2'], ['pMYT084_nan_Int10_Vector', 'pMYT035_nan_KanR'], ['pMYT084_nan_Int10_Vector', 'pMYT036_nan_NatR'], ['pMYT084_nan_Int10_Vector', 'pMYT037_nan_HygR'], ['pMYT084_nan_Int10_Vector', 'pMYT038_nan_ZeoR']] # type: ignore

# Tube rack locations of reagents
master_mix = A1 # type: ignore
reagent_tubes = [master_mix] + list(inserts.values())

# Construct Tube Locations
construct_tubes = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10', 'E11', 'E12', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6'] # type: ignore

# Define volumes, in uL
vol_master_mix_per_reaction = [48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48] # type: ignore
vol_per_insert = 1 # type: ignore

# Thermocycler settings
reaction_temp = 37 # type: ignore
inactivation_temp = 65 # type: ignore
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
            f"Not enough tips: Need 180 x 20uL tips and 90 x 300uL tips, "
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

    pause(f"Place Master Mix in [{tube_rack[master_mix]}] and press continue. Thermocycler protocol will begin after pipetting.")

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


