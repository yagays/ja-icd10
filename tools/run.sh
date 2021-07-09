export PYTHONPATH="./:$PYTHONPATH"

mkdir -p icd10/data
# export all working files from byomei.zip
poetry run python tools/generate_data_from_byomei.py

# generate jsons
poetry run python tools/generate_byomei_id2disease.py
poetry run python tools/generate_icd_code2category.py
poetry run python tools/generate_icd_code2byomei_ids.py
poetry run python tools/generate_word2code.py
