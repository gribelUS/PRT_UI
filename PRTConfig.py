# Code ritten by Skyler Putney

TAG_TO_READ = 'SORTER_1_REQUEST'

STATUS_BIT = '.END'

TAG_TO_WRITE = 'SORTER_1_RESPONSE'

CAR_DEST_MAP = {
   
}
"""
READING
DATA_TYPE:
96 Bytes long
First member string - double int - 4 Bytes -- length of string (don't need to really worry about)
82 Bytes after are ASCII characters 
Int with scanner number - 2 Bytes
Int with transaction ID - 2 Bytes
End bit -- double integer - 4 Bytes

WRITING BACK
DESTINATION: 'SORTER_1_RESPONSE'
Send back transaction ID to ensure correct communication -- + the destination -- written into data type:
4 Bytes wide
3 members: 
1: transaction id 
2: destination (single int) 
3: end (single int, 1)

AFTER SORTING:
'SORTED_1_REPORT'
96 Bytes
Barcode -- same as sorted car
Tracking flags: Active, Lost, Good, Diverted: Inner data type w/ 4 Booleans (1 byte wide each)
End bit - double integer - 4 Bytes
Do with data what I want
This bardcode went to X destination and Y is the reason
Start logging like: packages lost, not diverted because motor is working or dest not available etc
"""

BARCODE_DESTINATION_MAP = {
    #Barcode: Destination,
    0: 0,
    1: 0,
    2: 2,
    3: 2,
    4: 2,
    5: 0,
    6: 0,
    7: 0,
    8: 0,
    9: 0,
    10: 0,
    11: 0,
    12: 0,
    13: 0,
    14: 0,
    15: 0,
    16: 0,
    17: 0,
    18: 0,
    19: 0,
    20: 0,
}
