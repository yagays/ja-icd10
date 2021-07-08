import json

import pandas as pd

from icd10.util import normalize_icd_code

icd_code2byomei_ids = {}

relation_df = pd.read_csv("data/raw/ClinicalCategories/ICDrelation_20210701.txt", header=None, skiprows=[0])
for row in relation_df.itertuples():
    byomei_id_or_icd_code = normalize_icd_code(row[1])
    icd_code = normalize_icd_code(row[2])

    if icd_code not in icd_code2byomei_ids:
        icd_code2byomei_ids[icd_code] = [byomei_id_or_icd_code]
    else:
        icd_code2byomei_ids[icd_code].append(byomei_id_or_icd_code)


with open("data/icd_code2byomei_ids_or_icd_codes.json", "w") as f:
    json.dump(icd_code2byomei_ids, f, ensure_ascii=False, indent=4)
