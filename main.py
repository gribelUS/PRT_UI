# Code ritten by Skyler Putney
# Copyright (c) 2023, PRT
# All rights reserved.

from time import time, sleep
from Communication.PLC import PLC
from DataCollection.DataLogger import DataLogger
from PRTConfig import TAG_TO_READ, STATUS_BIT, TAG_TO_WRITE
from Communication.PLCConfig import PRT_PLC_IP_ADDRESS
from PRTPLC import PRTPLC
from PRTConfig import BARCODE_DESTINATION_MAP

# Data Logger
logger = DataLogger('datalogs', 'dataplots')
# Data save interval (seconds), last save time
SAVE_INTERVAL = 60

def get_destination(barcode: int):
    return BARCODE_DESTINATION_MAP.get(barcode)


def run_system():
    print(f"PRT_PLC: Connecting to PLC: {PRT_PLC_IP_ADDRESS}...")
    prt = PRTPLC()
    LAST_SAVE_TIME = time()

    while (True):
        sorter_1_request = prt.read_sorter_request(1)
        if sorter_1_request is not None:
            barcode, transaction_id = sorter_1_request
            barcode = int(barcode)
            logger.log_data(SORTER=1, TYPE="REQUEST", TRANSACTION_ID=transaction_id, BARCODE=barcode)
            destination = get_destination(barcode)
            prt.send_sorter_response(1, transaction_id, destination)
            logger.log_data(SORTER=1, TYPE="RESPONSE", TRANSACTION_ID=transaction_id, DESTINATION=destination)
        sorted_1_report = prt.read_sorted_report(1)
        if sorted_1_report is not None:
            barcode, active, lost, good, diverted = sorted_1_report
            barcode = int(barcode)
            logger.log_data(SORTER=1, TYPE="REPORT", BARCODE=barcode, ACTIVE=active, LOST=lost, GOOD=good, DIVERTED=diverted)

        current_time = time()
        if current_time - LAST_SAVE_TIME >= SAVE_INTERVAL:
            logger.save_log("PRT")
            LAST_SAVE_TIME = current_time

def test_system():
    print(f"PLCPrt: Connecting to PLC: {PRT_PLC_IP_ADDRESS}...")
    prt_plc = PLC(PRT_PLC_IP_ADDRESS)
    prt_plc.connect()
    print(f"PLCPrt: Successfully connected to PLC: {PRT_PLC_IP_ADDRESS}...")
    while (True):
        end_bit = prt_plc.read_tag(TAG_TO_READ + STATUS_BIT)
        print(f"End bit: {end_bit}")
        if end_bit == 1:
            data = prt_plc.read_tag(TAG_TO_READ)
            print(f"Data: {data}")
            prt_plc.write_tag(TAG_TO_READ + STATUS_BIT, 0)
            prt_plc.write_tag(TAG_TO_WRITE + '.TRANSACTION_ID', data['TRANSACTION_ID'])
            prt_plc.write_tag(TAG_TO_WRITE + '.DESTINATION', 2)
            prt_plc.write_tag(TAG_TO_WRITE + '.END', 1)
            
        
def main():
    run_system()
    #test_system()

if __name__ == "__main__":
    main()