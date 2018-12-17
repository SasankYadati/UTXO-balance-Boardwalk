# Team 3
from base64 import b64encode
import json
import pandas as pd
import numpy as np
import datetime
import requests

class UTXO:

    url = "http://pa.boardwalktech.com/BW_PES_Assignment_Group1/rest/v1/grid/2000001?importTid=-1&mode=1&baselineId=-1&view=LATEST"

    def __init__(self, email, username='root', password='0'):
        self.email = email
        self.username = username
        self.password = password    
    
    def __getAuthorizationString__(self):
        self.base_string = self.email+":"+self.password+":"+self.username
        print(self.base_string)
        self.base_string = bytes(self.base_string, 'utf-8')
        self.base_string = b64encode(self.base_string)
        self.base_string = self.base_string.decode()
        return self.base_string

    def __getBalance__(self):
        self.headers = { "Authorization" : self.__getAuthorizationString__()}
        self.response = requests.get(self.url, headers=self.headers)
        self.data = self.response.json()
        # print(self.data)
    
    def displayBalance(self):
        self.__getBalance__()
        columns = self.data["columnArray"]
        index = self.data["rowArray"]
        df_ = pd.DataFrame(index=index, columns=columns)
        row_wise = {}

        for cell in self.data['cells']:
            row, col  = cell["rowId"], cell["colId"]
            if row not in row_wise:
                row_wise[row] = {}
            row_wise[row][col] = cell["cellValue"]
        
        for row in row_wise:
            df_.loc[row] = row_wise[row]        
        
        active_id = -1
        amount_id = -1
        
        for col in self.data["columns"]:
            if col["name"] == "AMOUNT":
                amount_id = col['id']
            if col["name"] == "ACTIVE":
                active_id = col['id']

        active_cells = df_[active_id] == 'YES'

        df = df_[active_cells]

        print(df)

        self.total_balance = df[1001].apply(lambda x: float (x)).sum()

        return self.total_balance

if __name__ == '__main__':
    utxo_1 = UTXO(email='gavrish14@gmail.com')
    utxo_1.displayBalance()

    utxo_2 = UTXO(email='salampes2015@gmail.com')
    utxo_2.displayBalance()

    utxo_3 = UTXO(email='sharnam.khurana2@gmail.com')
    utxo_3.displayBalance()

    utxo_4 = UTXO(email='tvarita1297@gmail.com')
    utxo_4.displayBalance()