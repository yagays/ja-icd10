import gzip
import json

with open("data/working/main.json") as f:
    byomei_list = json.load(f)

byomei_id2disease = {}
for byomei in byomei_list:
    if byomei["ＩＣＤ１０‐２０１３"]:
        icd_code = byomei["ＩＣＤ１０‐２０１３"]
    else:
        icd_code = ""

    icd_category = {
        "byomei_id": str(byomei["病名管理番号"]),
        "code": icd_code,
        "name": byomei["病名表記"],
        "name_kana": byomei["病名表記カナ"],
        "name_abbrev": byomei["傷病名省略名称"],
        "disease_exchange_id": byomei["病名交換用コード"],
    }
    byomei_id2disease[icd_category["byomei_id"]] = icd_category

with gzip.open("data/byomei_id2disease.json.gz", "wt", encoding="ascii") as zipfile:
    json.dump(byomei_id2disease, zipfile)
