import gzip
import json
from collections import defaultdict

from icd10.util import normalize_string

with open("data/working/index.json") as f:
    index_json = json.load(f)

with open("data/working/main.json") as f:
    main_json = json.load(f)


# 病名交換用コードとICD-10は1対1対応している
exchange2icd = {}
for row in main_json:
    exchange2icd[row["病名交換用コード"]] = row["ＩＣＤ１０‐２０１３"]

index_word2icd = defaultdict(list)
for row in index_json:
    index_word = normalize_string(row["索引用語"]).lower()  # すべて小文字にする
    exchange_code = row["対応用語コード"]

    # 病名交換用コードにICD-10コードが振られていて、かつindex_word2icdに新規登録のみ
    if exchange_code in exchange2icd and exchange2icd[exchange_code] not in index_word2icd[index_word]:
        index_word2icd[index_word].append(exchange2icd[exchange_code])

with gzip.open("data/index_word2icd.json.gz", "wt", encoding="ascii") as zipfile:
    json.dump(index_word2icd, zipfile)
