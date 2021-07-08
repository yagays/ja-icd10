from collections import defaultdict

import pandas as pd

from icd10.util import normalize_icd_code

relation = defaultdict(list)

relation_df = pd.read_csv("data/raw/ClinicalCategories/ICDrelation_20210701.txt", header=None, skiprows=[0])
for row in relation_df.itertuples():
    relation[normalize_icd_code(row[2])].append(normalize_icd_code(row[1]))
