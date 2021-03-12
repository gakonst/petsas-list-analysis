import pandas as pd
import os
from utils import preprocess_data

PETSAS_LIST = "./lista_petsa.csv"

# https://www.protagon.gr/wp-content/uploads/2020/07/%CE%9A%CE%91%CE%A4%CE%91%CE%9B%CE%9F%CE%93%CE%9F%CE%A3-%CE%9C%CE%95%CE%A3%CE%A9%CE%9D-%CE%95%CE%9A%CE%A3%CE%A4%CE%A1%CE%91%CE%A4%CE%95%CE%99%CE%91-%CE%95%CE%9D%CE%97%CE%9C%CE%95%CE%A1%CE%A9%CE%A3%CE%97%CE%A3-COVID-19.pdf
FNAME = "./ΚΑΤΑΛΟΓΟΣ-ΜΕΣΩΝ-ΕΚΣΤΡΑΤΕΙΑ-ΕΝΗΜΕΡΩΣΗΣ-COVID-19.pdf"
PAGES = 18

# load the cached file or re-generate it
if not os.path.exists(PETSAS_LIST):
    df = preprocess_data(FNAME, PAGES)
    # now that our data is pre-processed, let's throw it in a csv
    df.to_csv(PETSAS_LIST, index = False)
else:
    df = pd.read_csv(PETSAS_LIST)

print(df)
