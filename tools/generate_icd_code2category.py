import json
import re

import pandas as pd

from icd10.util import normalize_icd_code

icd_code2category = {}
items_df = pd.read_csv("data/raw/ClinicalCategories/ICDitems_20210701.txt", header=None)
for _, row in items_df.iterrows():
    byomei_id_or_code = row[0]
    normalized_byomei_id_or_code = normalize_icd_code(byomei_id_or_code)
    name = row[1]

    if re.match(r"^\d{8}$", byomei_id_or_code):
        # `20050004 １８常染色体異常` といった場合
        pass
    else:
        # `A00 コレラ` といった場合
        icd_code2category[normalized_byomei_id_or_code] = {"code": byomei_id_or_code, "name": name}

with open("data/icd_code2category.json", "w") as f:
    json.dump(icd_code2category, f, ensure_ascii=False, indent=4)
