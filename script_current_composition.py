import sys
import os
import pandas as pd
from pathlib import Path
import datetime

CUR_DIR = Path(__file__).resolve().parent
sys.path.append(str(CUR_DIR.parent.parent))

B3_URL = "https://sistemaswebb3-listados.b3.com.br/indexPage/day/{index_code}?language=pt-br"
SLEEP_TIME = 2


class IBOVIndex():
    def __init__(self, index_name: str):
        self.index_name = index_name
        self._target_url = B3_URL.format(index_code="IBOV")
        self.today = datetime.date.today()
        self.quarter = str(pd.Timestamp(self.today).quarter)
        self.year = str(self.today.year)

    def get_first_added(self):
        path = str(CUR_DIR) + "/historic_composition/"
        df_latest_index = pd.read_csv(path + self.year + '_' + self.quarter + 'Q.csv')
        symbols = df_latest_index["symbol"].tolist()
        date_first_added = {}
        for file in os.listdir(path):
            if (file.split('.')[1] == 'csv' and 'date' not in file):
                df = pd.read_csv(path + file, encoding='utf8')
                for symbol in df["symbol"].tolist():
                    if symbol in symbols and symbol not in date_first_added:
                        date_first_added[symbol] = file.split(".")[0]

        df = pd.DataFrame.from_dict(date_first_added, orient='index', columns=['Date First Added'])
        df.reset_index(inplace=True)
        df.rename(columns={'index': 'symbol'}, inplace=True)
        df.to_csv(path + 'date_first_added_' + self.year + '_' + self.quarter + 'Q.csv')


if __name__ == "__main__":
    ibov = IBOVIndex(index_name='IBOV')
    ibov.get_first_added()
