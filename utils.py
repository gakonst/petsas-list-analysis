import pandas as pd
import tabula

def preprocess_data(fname, num_pages, end = 1232):
    df = pd.DataFrame([])
    for pageiter in range(num_pages):
        page = tabula.read_pdf(fname, pages=pageiter+1, guess=True)[0]

        # drop unnamed axis
        page = page.drop('Unnamed: 0', axis = 1)

        # rename columns (careful with utf-8)
        page = page.rename(columns = {
            "ΟΝΟΜΑ ΜΕΣΟΥ": 'name',
            'ΝΟΜΟΣ': 'district',
            'ΚΑΤΗΓΟΡΙΑ ΜΕΣΟΥ': 'category',
            'ΠΟΣΟ ΒΑΣΕΙ\rΕΝΤΟΛΩΝ': 'amount_instructed',
            'ΤΙΜΟΛΟΓΗΜΕΝΟ\rΠΟΣΟ (ΠΡΟ\rΚΡΑΤΗΣΕΩΝ)': 'pre_tax_billed_amount',
            'ΣΥΝΟΛΙΚΗ ΑΞΙΑ ΜΕ\rΦΠΑ': 'total_value_with_tax',
        })

        # gross
        for col in ['amount_instructed', 'pre_tax_billed_amount', 'total_value_with_tax']:
            page[col] = page[col].str.replace('.', '', regex = False).str.replace(',','.', regex = False).astype('float64')

        # rename text categories
        page = page.replace({
            'ΕΝΤΥΠΟ': 'newspaper',
            'ΙΣΤΟΣΕΛΙΔΑ': 'website',
            'ΡΑΔΙΟΦΩΝΟ': 'radio',
            'ΤΗΛΕΟΡΑΣΗ': 'tv',
        })

        df = df.append(page, sort = False, ignore_index = True)

    # trim the dataset to not include redundant info
    df = df[:end]
    return df
