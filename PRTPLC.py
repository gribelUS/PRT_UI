# Code ritten by Skyler Putney

from Communication.PLC import PLC
from Communication.PLCConfig import PRT_PLC_IP_ADDRESS

class PRTPLC(PLC):
    """
    Represents the PRT PLC
    """
    def __init__(self):
        super().__init__(PRT_PLC_IP_ADDRESS)
        self.connect()

    def read_sorter_request(self, sorter_num: int):
        data = self.read_tag(f'SORTER_{sorter_num}_REQUEST')
        if data is None:
            return None
        if data['END'] == 1:
            return data['BARCODE'], data['TRANSACTION_ID']

    def send_sorter_response(self, sorter_num: int, transaction_id: int, destination: int):
        #Clear original tag
        self.write_tag(f'SORTER_{sorter_num}_REQUEST.END', 0)
        #Write response tags
        self.write_tag(f'SORTER_{sorter_num}_RESPONSE.TRANSACTION_ID', transaction_id)
        self.write_tag(f'SORTER_{sorter_num}_RESPONSE.DESTINATION', destination)
        self.write_tag(f'SORTER_{sorter_num}_RESPONSE.END', 1)

    def read_sorted_report(self, sorter_num: int):
        data = self.read_tag(f'SORTED_{sorter_num}_REPORT')
        if data is None:
            return None
        if data['END'] == 1:
            return data['BARCODE'], data['ACTIVE'], data['LOST'], data['GOOD'], data['DIVERTED']

