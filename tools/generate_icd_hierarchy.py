import json
from collections import defaultdict

import pandas as pd

relation = defaultdict(list)

relation_df = pd.read_csv("data/raw/ClinicalCategories/ICDrelation_20210701.txt", header=None, skiprows=[0])
for row in relation_df.itertuples():
    relation[row[2]].append(row[1])

# utfに変換が必要
# $ nkf -w --overwrite data/raw/ClinicalCategories/ICDitems_20210701.txt
items_df = pd.read_csv("data/raw/ClinicalCategories/ICDitems_20210701.txt", header=None)
id2name = dict(zip(items_df[0], items_df[1]))


def recursive_expand(icd10_id):
    if relation[icd10_id]:
        result = []
        for child in relation[icd10_id]:
            children = recursive_expand(child)
            if children:
                result.append({"id": child, "name": f"{child} {id2name[child]}", "children": children})
            else:
                result.append({"id": child, "name": f"{child} {id2name[child]}"})
        return result
    else:
        return ""


result = recursive_expand("1")

with open("data/icd_hierarchy.json", "w") as f:
    json.dump(result, f, ensure_ascii=False, indent=4)
