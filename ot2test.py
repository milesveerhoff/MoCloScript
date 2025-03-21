# imports
from opentrons import containers, instruments

# containers
plate = containers.load('96-flat', 'B1')
tiprack = containers.load('tiprack-200ul', 'A1')

# pipettes
pipette = instruments.Pipette(axis='b', max_volume=200, tip_racks=[tiprack])

# commands
pipette.transfer(100, plate.wells('A1'), plate.wells('B1'))