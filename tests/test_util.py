from icd10.util import is_valid_byomei_id_or_code, normalize_icd_code


def test_normalize_icd_code():
    assert normalize_icd_code("A000") == "A000"
    assert normalize_icd_code("A00.0") == "A000"


def test_is_valid_byomei_id_or_code():
    assert is_valid_byomei_id_or_code("20050004") is True
    assert is_valid_byomei_id_or_code("A00") is True
    assert is_valid_byomei_id_or_code("A00.0") is True
    assert is_valid_byomei_id_or_code("A000") is True
    assert is_valid_byomei_id_or_code("F15.1a") is True
    assert is_valid_byomei_id_or_code("F15.-a") is True
    assert is_valid_byomei_id_or_code("F60.3d") is True
    assert is_valid_byomei_id_or_code("A00-A09") is True

    assert is_valid_byomei_id_or_code("") is False
    assert is_valid_byomei_id_or_code("invalid") is False
