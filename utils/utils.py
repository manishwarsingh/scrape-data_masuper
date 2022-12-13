import pandas as pd
import time 
import os
from datetime import datetime



def create_csv(data, csvName, productType):
    """
    To create csv from collected dataframe
    """
    stamp = datetime.now().strftime("%d_%m_%Y_%H_%M")
    path = os.getcwd() + '/scraped_data/'+ productType + "/" + stamp
    try:
        if not os.path.isdir(path):
            os.makedirs(path)
    except OSError as e:
        print(e)
    df = pd.DataFrame.from_dict(data)
    df.to_csv(f'{path}/{csvName}.csv',index=False)
    #df.to_csv(f'{path}/{csvName}.csv', encoding='utf_8_sig')