import pandas as pd


def get_header_from_ttl(file_path):
    ttl_df = pd.read_csv(file_path, encoding="shift-jis")
    return ttl_df.columns.tolist()


main_df = pd.read_csv("data/raw/byomei507/main/nmain507.txt", encoding="shift-jis", header=None)
main_df.columns = get_header_from_ttl("data/raw/byomei507/option/ttl_main.txt")
main_df.to_json("data/main.json", orient="records", force_ascii=False, indent=4)

modify_df = pd.read_csv("data/raw/byomei507/main/mdfy507.txt", encoding="shift-jis", header=None)
modify_df.columns = get_header_from_ttl("data/raw/byomei507/option/ttl_mdfy.txt")
modify_df.to_json("data/modify.json", orient="records", force_ascii=False, indent=4)

index_df = pd.read_csv("data/raw/byomei507/main/index507.txt", encoding="shift-jis", header=None)
index_df.columns = get_header_from_ttl("data/raw/byomei507/option/ttl_idx.txt")
index_df.to_json("data/working/index.json", orient="records", force_ascii=False, indent=4)
