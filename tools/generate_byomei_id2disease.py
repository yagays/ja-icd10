import json

with open("data/working/main.json") as f:
    byomei_list = json.load(f)

byomei_id2disease = {}
for byomei in byomei_list:
    icd_category = {
        "byomei_id": str(byomei["病名管理番号"]),
        "code": byomei["ＩＣＤ１０‐２０１３"],
        "name": byomei["病名表記"],
        "name_kana": byomei["病名表記カナ"],
        "name_abbrev": byomei["傷病名省略名称"],
        "disease_exchange_id": byomei["病名交換用コード"],
    }
    byomei_id2disease[icd_category["byomei_id"]] = icd_category

with open("data/byomei_id2disease.json", "w") as f:
    json.dump(byomei_id2disease, f, ensure_ascii=False, indent=4)
