import pandas as pd
import requests
import time
from io import StringIO
import numpy as np
from tqdm import tqdm

class PvgisAPI:
    def __init__(self, reference_lat_lon):
        self.df_reference = pd.read_csv('reference.csv').drop()

    def set_url(self, url_base, data_dic):
        url = url_base
        for key in data_dic.keys():
            url += str(key)+'='+str(data_dic[key]) + '&'
        url = url[:-1]
        return url

    def get_dataframe_from_text(self, text):
        s=text
        substring_data = s[s.find('Month'):s.find('\r\n\tAOI loss')]
        substring_data = substring_data.replace('\t\t',',')
        substring_data = substring_data.replace('\r','')
        TESTDATA = StringIO(substring_data)
        df = pd.read_csv(TESTDATA, sep=",")
        return df

    def set_df_pvgis_format(self, df_in, coluna_selecionada):
        values = df_in.loc[:,[coluna_selecionada]].values
        a = values.copy()
        a = np.delete(a, -1)
        a = np.insert(a, 0, values[-1])
        return a