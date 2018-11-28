# Definitions for Machine.Status
MACHINE_STATUS_BROKEN = 0
MACHINE_STATUS_ALIVE = 1

# The "prebaked" downage categories
PREBAKED_DOWNAGE_CATEGORY_TEXTS = [
    'Software Problem',
    'Hardware Problem',
    'Machine Problem'
]

# TODO: remove this and actually query locations after basic demo
# x should be within [0-3] and y should be within [0-8]
STUB_LOCATION_DICT = {
    '1': {
        'x': 1,
        'y': 2
     },
    '2': {
        'x': 0,
        'y': 3
     },
    '3': {
        'x': 0,
        'y': 4
     },
    '4': {
        'x': 0,
        'y': 5
     },
    '5': {
        'x': 1,
        'y': 6 
     },
    '6': {
        'x': 3,
        'y': 6
     },
    '7': {
        'x': 3,
        'y': 5
     },
    '8': {
        'x': 3,
        'y': 4
     },
    '9': {
        'x': 3,
        'y': 3
     },
    '10': {
        'x': 3,
        'y': 2
     },
}
