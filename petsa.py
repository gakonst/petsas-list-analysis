import pandas as pd
# silence chain assignment warning
pd.options.mode.chained_assignment = None  # default='warn'
import os

from utils import preprocess_data
import matplotlib.pyplot as plt

PETSAS_LIST = "./lista_petsa.csv"

# https://www.protagon.gr/wp-content/uploads/2020/07/%CE%9A%CE%91%CE%A4%CE%91%CE%9B%CE%9F%CE%93%CE%9F%CE%A3-%CE%9C%CE%95%CE%A3%CE%A9%CE%9D-%CE%95%CE%9A%CE%A3%CE%A4%CE%A1%CE%91%CE%A4%CE%95%CE%99%CE%91-%CE%95%CE%9D%CE%97%CE%9C%CE%95%CE%A1%CE%A9%CE%A3%CE%97%CE%A3-COVID-19.pdf
FNAME = "./LISTA_PETSA_PROTAGON.pdf"
PAGES = 18
force = False

# load the cached file or re-generate it
df = pd.DataFrame()
if force or not os.path.exists(PETSAS_LIST):
    df = preprocess_data(FNAME, PAGES)
    # now that our data is pre-processed, let's throw it in a csv
    df.to_csv(PETSAS_LIST, index = False)
else:
    df = pd.read_csv(PETSAS_LIST)

# cleanup
media = pd.DataFrame({ "name" : df['name'], "amount" : df['total_value_with_tax']})
media = media[media['amount'] > 0]

# regex for rows that are under the same company group
# (both Greek and English unicode used)
groups = {
   'SKAI' : 'ΣΚΑΙ|SKAI',
   'ANT1' : 'ΑΝΤ1|ΑΝΤ 1|ΑΝΤΕΝΝΑ|ANT1|ANT 1|ANTENNA',
   'STAR' : '^STAR$|STAR.GR|STAR K.E.|STAR FM',
   'ALPHA': 'ΑΛΦΑ 94,7|ΑΛΦΑ',
   'OPEN' : 'OPEN',
   'MEGA' : '^MEGA$|MEGATV',
   'ERT' : 'ΕΡΤ|ERT.GR',
   'PROTO_THEMA': 'ΠΡΩΤΟ ΘΕΜΑ|PROTOTHEMA'
}

# Group them together
for name, expr in groups.items():
    # get the matching group
    medium = media[media['name'].str.contains(expr)]
    print("Grouping", ', '.join(list(medium['name'])))

    # remove the individual entries
    media = media[~media.name.isin(medium.name)]

    # add the sum
    grouped = { 'name': name, 'amount': sum(medium['amount']) }
    media = media.append(grouped, ignore_index = True)

# sort by amount
media = media.sort_values(by = 'amount', ascending = False).reset_index(drop = True)

# get percentages
total = sum(media['amount'])
media['percent_total'] = media['amount'] / total

# Get cumulative sums
for cumsum in [0.5, 0.75, 0.95]:
    media_until_cumsum = media.loc[media['percent_total'].cumsum() < cumsum]
    media_until_cumsum['cumulative_amount'] = media_until_cumsum['amount'].cumsum()
    media_until_cumsum.loc['cumulative_pct'] = media_until_cumsum['percent_total'].cumsum()
    # TODO: Weight this by listeners / audience?
    pct = len(media_until_cumsum) / len(media)
    print(f"{pct}% of media got {100 * cumsum}% of the funding")

# get the top 50 media and see the breakdown
media.head(50).set_index('name').plot.bar(y = 'amount')
plt.show()
