import json
import re

from dataclasses import dataclass
from typing import Dict, List, Optional

import pandas as pd


from icd10.chapter_block import chapter_block_list
from icd10.relation import relation
from icd10.util import normalize_icd_code, is_valid_byomei_id_or_code

with open("data/main.json") as f:
    byomei_list = json.load(f)


@dataclass
class Disease:
    """
    傷病
    """

    byomei_id: str  # 病名管理番号
    code: str
    name: str
    name_kana: str
    name_abbrev: str
    disease_exchange_id: str  # 病名交換用コード

    @property
    def dot_code(self) -> str:
        return self.code[:3] + "." + self.code[3:]

    def __repr__(self) -> str:
        return f"<Disease:[{self.dot_code}][{self.byomei_id}] {self.name}>"


@dataclass
class Category:
    byomei_id: Optional[str]
    code: Optional[str]
    name: str

    @property
    def normalized_code(self) -> str:
        return normalize_icd_code(self.code)

    @property
    def is_block(self) -> bool:
        if self.code:
            re_block = re.match(r"^[A-Z]\d{2}$", self.code)
            re_block_range = re.match(r"^[A-Z]\d{2}-[A-Z]\d{2}$", self.code)
            if any([re_block, re_block_range]):
                return True
        return False

    def __repr__(self) -> str:
        return f"<ICD Category:[{self.code}] {self.name}>"

    @property
    def is_chapter(self) -> bool:
        return self.code in chapter_block_list


class ICD:
    def __init__(self) -> None:
        self.version = "20210701"
        self.byomei_id2disease: Dict = {}
        self.code2category: Dict = {}

        self._initialize()

    def _initialize(self):
        for byomei in byomei_list:
            icd_category = Disease(
                byomei_id=str(byomei["病名管理番号"]),
                code=byomei["ＩＣＤ１０‐２０１３"],
                name=byomei["病名表記"],
                name_kana=byomei["病名表記カナ"],
                name_abbrev=byomei["傷病名省略名称"],
                disease_exchange_id=byomei["病名交換用コード"],
            )
            self.byomei_id2disease[icd_category.byomei_id] = icd_category

        self.byomei_id2disease[icd_category.byomei_id] = icd_category

        items_df = pd.read_csv("data/raw/ClinicalCategories/ICDitems_20210701.txt", header=None)
        for _, row in items_df.iterrows():
            byomei_id_or_code = row[0]
            normalized_byomei_id_or_code = normalize_icd_code(byomei_id_or_code)
            name = row[1]

            if re.match(r"^\d{8}$", byomei_id_or_code):
                # `20050004 １８常染色体異常` といった場合
                # self.code2category[normalized_byomei_id_or_code] = Category(
                #     byomei_id=byomei_id_or_code, code=None, name=name
                # )
                pass
            else:
                # `A00 コレラ` といった場合
                self.code2category[normalized_byomei_id_or_code] = Category(
                    byomei_id=None, code=byomei_id_or_code, name=name
                )

    def get_category_by_code(self, query_code: str) -> Category:
        """ICD-10のコードからカテゴリーを取得する

        Args:
            query_code (str): ICD-10のコード文字列

        Raises:
            ValueError: 与えられたコード文字列が存在しなかった場合

        Returns:
            Category: コードに対応するカテゴリー
        """
        query_code = normalize_icd_code(query_code)

        if query_code in self.code2category:
            return self.code2category[query_code]
        else:
            raise ValueError(f"{query_code} is not valid ICD-10 Code")

    def find_categories_by_name(self, query_str: str) -> List[Category]:
        """検索文字列を含むカテゴリー名を検索する

        Args:
            query_str (str): 検索文字列

        Returns:
            List[Category]: 検索文字列を含むカテゴリーのリスト
        """
        if query_str == "":
            return []

        results = []
        for _, category in self.code2category.items():
            if query_str in category.name:
                results.append(category)

        return results

    def get_diseases_by_code(self, query_code: str) -> List[Disease]:
        """ICD-10のコードの階層以下に含まれるすべての傷病を返す

        Args:
            query_code (str): ICD-10のコード文字列

        Returns:
            List[Disease]: 含まれる傷病のリスト
        """

        if not is_valid_byomei_id_or_code(query_code):
            return []

        disease_list = []
        query_code = normalize_icd_code(query_code)

        def _get_leaf_nodes(byomei_id_or_code):
            if re.match(r"^\d{8}$", byomei_id_or_code):
                disease_list.append(self.byomei_id2disease[byomei_id_or_code])
            else:
                for n in relation[byomei_id_or_code]:
                    _get_leaf_nodes(n)

        _get_leaf_nodes(query_code)
        return disease_list

    def get_diseases_and_categories_by_code(self, query_code: str) -> List[Disease]:
        if not is_valid_byomei_id_or_code(query_code):
            return []

        disease_list = []
        query_code = normalize_icd_code(query_code)

        def _get_leaf_nodes(byomei_id_or_code):
            if re.match(r"^\d{8}$", byomei_id_or_code):
                disease_list.append(self.byomei_id2disease[byomei_id_or_code])
            else:
                disease_list.append(self.code2category[normalize_icd_code(byomei_id_or_code)])
                for n in relation[byomei_id_or_code]:
                    _get_leaf_nodes(n)

        _get_leaf_nodes(query_code)
        return disease_list

    def __getitem__(self, name: str) -> Category:
        return self.get_category_by_code(name)


if __name__ == "__main__":
    icd = ICD()
    print(icd.get_category_by_code("A00.0"))
    # print(icd.find_categories_by_name("頭痛"))

