import pytest

from icd10.icd import ICD


@pytest.fixture(scope="module")
def icd():
    return ICD()


def test_get_category_by_code(icd):
    category = icd["A000"]
    assert category.name == "コレラ菌によるコレラ"
    assert category.code == "A00.0"
    assert category.is_block is False
    assert category.is_chapter is False


def test_get_category_by_code_5_digit(icd):
    category = icd["F150a"]
    assert category.name == "カフェインによる精神及び行動の障害，急性中毒"
    assert category.code == "F15.0a"
    assert category.normalized_code == "F150a"
    assert category.is_block is False
    assert category.is_chapter is False


def test_get_category_by_code_point_dash(icd):
    category = icd["F15.-a"]
    assert category.name == "カフェインによる精神及び行動の障害"
    assert category.code == "F15.-a"
    assert category.is_block is False
    assert category.is_chapter is False


def test_get_category_by_code_blocks(icd):
    # 3桁はblocks of categories
    category = icd["A00"]
    assert category.name == "コレラ"
    assert category.code == "A00"
    assert category.is_block is True
    assert category.is_chapter is False


def test_get_category_by_code_has_point(icd):
    assert icd["A00.0"].name == "コレラ菌によるコレラ"


def test_get_category_by_code_blocks_range(icd):
    # block (chapterではない)
    category = icd["A00-A09"]
    assert category.name == "腸管感染症"
    assert category.is_block is True
    assert category.is_chapter is False


def test_get_category_by_code_chapter(icd):
    # chapter
    category = icd["A00-B99"]
    assert category.name == "感染症及び寄生虫症"
    assert category.is_block is True
    assert category.is_chapter is True


def test_icd10_by_code_invalid(icd):
    with pytest.raises(ValueError):
        icd[""]
    with pytest.raises(ValueError):
        icd["A0000"]


def test_get_disease_by_byomei_id(icd):
    disease = icd.get_disease_by_byomei_id("20100524")
    assert disease.byomei_id == "20100524"
    assert disease.code == "E250"
    assert disease.name == "１１β−水酸化酵素欠損症"


def test_get_disease_by_byomei_id_invalid(icd):
    with pytest.raises(ValueError):
        icd.get_disease_by_byomei_id("")
    with pytest.raises(ValueError):
        icd.get_disease_by_byomei_id("99999999")


def test_get_diseases_by_code(icd):
    # http://www.byomei.org/Scripts/ICD10Categories/default2_ICD.asp?CategoryID=A00.0
    assert len(icd.get_diseases_by_code("A000")) == 2
    assert len(icd.get_diseases_by_code("A00.0")) == 2

    # http://www.byomei.org/Scripts/ICD10Categories/default2_ICD.asp?CategoryID=A00
    assert len(icd.get_diseases_by_code("A00")) == 5

    # http://www.byomei.org/Scripts/ICD10Categories/default2_ICD.asp?CategoryID=A02
    # その他の明示されたサルモネラ感染症 には傷病は無し
    assert len(icd.get_diseases_by_code("A02.8")) == 0


def test_get_diseases_by_code_point_dash(icd):
    # http://www.byomei.org/Scripts/ICD10Categories/default2_ICD.asp?CategoryID=F15.-a
    # F15.2a にある 20051469:カフェイン依存 のみ
    assert len(icd.get_diseases_by_code("F15.-a")) == 1


def test_get_disease_by_code_invalid(icd):
    # 正しいICDコードでは無い場合
    assert icd.get_diseases_by_code("") == []
    assert icd.get_diseases_by_code("invalid_code") == []


def test_get_diseases_and_categories_by_code(icd):
    # A00.0と、それに含まれる傷病の合計3つ
    assert len(icd.get_diseases_and_categories_by_code("A000")) == 3
    assert len(icd.get_diseases_and_categories_by_code("A00.0")) == 3


def test_get_diseases_and_categories_by_code_invalid(icd):
    # 正しいICD-10コードでは無い場合
    assert icd.get_diseases_and_categories_by_code("") == []
    assert icd.get_diseases_and_categories_by_code("invalid_code") == []


def test_find_categories_by_name(icd):
    assert icd.find_categories_by_name("") == []

    assert len(icd.find_categories_by_name("腸管病原性大腸菌感染症")) == 1


def test_find_categories_by_name_partial_match(icd):
    assert len(icd.find_categories_by_name("頭痛")) == 1
    assert len(icd.find_categories_by_name("頭痛", partial_match=True)) == 18


def test_find_categories_by_name_normalize_string(icd):
    # NFKC normalizeのあとにlowerで統一している

    # 数字
    assert len(icd.find_categories_by_name("13トリソミー")) == 1  # 小文字
    assert len(icd.find_categories_by_name("１３トリソミー")) == 1

    # 英字
    assert len(icd.find_categories_by_name("AADC欠損症")) == 1
    assert len(icd.find_categories_by_name("aadc欠損症")) == 1
    assert len(icd.find_categories_by_name("ＡＡＤＣ欠損症")) == 1

    # 記号
    assert len(icd.find_categories_by_name("鳥インフルエンザ（Ｈ７Ｎ９）")) == 1
    assert len(icd.find_categories_by_name("２２ｑ１１．２欠失症候群")) == 1
    assert len(icd.find_categories_by_name("ＣＡＤ／ＣＡＭ冠破損")) == 1
    assert len(icd.find_categories_by_name("体表面積１０−１９％の熱傷")) == 1  # MINUS SIGN
    assert len(icd.find_categories_by_name("体表面積10-19%の熱傷")) == 1  # HYPHEN-MINUS

    # ローマ数字
    assert len(icd.find_categories_by_name("ムコ多糖症ＩＩＩ型")) == 1

    # ギリシャ文字
    assert len(icd.find_categories_by_name("原発性皮膚γδT細胞リンパ腫")) == 1


def test_find_categories_by_name_not_found_by_exchange_code(icd):
    # (外総診) に対応する "対応用語コード":"1BFG" は、ICD-10には無い
    assert len(icd.find_categories_by_name("(外総診)")) == 0
