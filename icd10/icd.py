import json
import re
from dataclasses import dataclass
from typing import List

from icd10.chapter_block import chapter_block_list
from icd10.util import is_valid_byomei_id_or_code, normalize_icd_code, normalize_string


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
    code: str
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
        with open("data/byomei_id2disease.json") as f:
            self.byomei_id2disease = {k: Disease(**v) for k, v in json.load(f).items()}
        with open("data/icd_code2category.json") as f:
            self.icd_code2category = {k: Category(**v) for k, v in json.load(f).items()}
        with open("data/index_word2icd.json") as f:
            self.index_word2icd = json.load(f)
        with open("data/icd_code2byomei_ids_or_icd_codes.json") as f:
            self.icd_code2byomei_ids_or_icd_codes = json.load(f)

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

        if query_code in self.icd_code2category:
            return self.icd_code2category[query_code]
        else:
            raise ValueError(f"{query_code} is not valid ICD-10 Code")

    def get_disease_by_byomei_id(self, query_code: str) -> Category:
        """病名管理番号のコードから傷病を取得する

        Args:
            query_code (str): 病名管理番号の文字列

        Raises:
            ValueError: 与えられた病名管理番号が存在しなかった場合

        Returns:
            Category: 病名管理番号に対応する傷病
        """

        if query_code in self.byomei_id2disease:
            return self.byomei_id2disease[query_code]
        else:
            raise ValueError(f"{query_code} is not valid byomei_id Code")


    def find_categories_by_name(self, query_str: str) -> List[Category]:
        """検索文字列を、インデックスまたはカテゴリー名内から検索する

        Args:
            query_str (str): 検索文字列

        Returns:
            List[Category]: 該当するカテゴリーのリスト
        """
        if query_str == "":
            return []

        # indexを探索
        query_str_lower = normalize_string(query_str).lower()  # index_word2icd.jsonのkeyと合わせる
        if query_str_lower in self.index_word2icd:
            icd_codes = self.index_word2icd[query_str_lower]
            return [self.icd_code2category[icd_code] for icd_code in icd_codes]

        return []

    def get_diseases_by_code(self, query_code: str) -> List[Disease]:
        """ICD-10のコードの階層以下に含まれるすべての傷病を返す

        Args:
            query_code (str): ICD-10のコード文字列

        Returns:
            List[Disease]: 含まれる傷病のリスト
        """
        return self._get_by_code(query_code, include_category=False)

    def get_diseases_and_categories_by_code(self, query_code: str) -> List[Disease]:
        """ICD-10のコードの階層以下に含まれるすべての傷病とカテゴリーを返す

        Args:
            query_code (str): ICD-10のコード文字列

        Returns:
            List[Disease]: 含まれる傷病とカテゴリーのリスト
        """
        return self._get_by_code(query_code, include_category=True)

    def _get_by_code(self, query_code: str, include_category: bool = False) -> List[Disease]:
        """ICD-10のコードの階層以下に含まれるすべての要素を返す

        Args:
            query_code (str): ICD-10のコード文字列
            include_category (bool, optional): カテゴリーを取得するか. Defaults to False.

        Returns:
            List[Disease]: 取得された要素のリスト
        """
        if not is_valid_byomei_id_or_code(query_code):
            return []

        disease_list = []
        query_code = normalize_icd_code(query_code)

        def _get_categories_and_diseases(byomei_id_or_code):
            if re.match(r"^\d{8}$", byomei_id_or_code):
                disease_list.append(self.byomei_id2disease[byomei_id_or_code])
            else:
                if include_category:
                    disease_list.append(self.icd_code2category[normalize_icd_code(byomei_id_or_code)])
                for n in self.icd_code2byomei_ids_or_icd_codes.get(byomei_id_or_code, []):
                    _get_categories_and_diseases(n)

        _get_categories_and_diseases(query_code)
        return disease_list

    def __getitem__(self, name: str) -> Category:
        return self.get_category_by_code(name)


if __name__ == "__main__":
    icd = ICD()
    print(icd.get_category_by_code("A00.0"))
    # print(icd.find_categories_by_name("頭痛"))
