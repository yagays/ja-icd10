import re
import unicodedata


def normalize_icd_code(code: str) -> str:
    return code.replace(".", "")


def is_valid_byomei_id_or_code(byomei_id_or_code: str) -> bool:
    if re.match(r"^\d{8}$", byomei_id_or_code):
        # e.g. 20050004
        return True
    if re.match(r"^[A-Z]\d{2}[\d\.\-abcd]{,3}$", byomei_id_or_code):
        # e.g. A00.0, F15.-a
        return True
    if re.match(r"^[A-Z]\d{2}-[A-Z]\d{2}$", byomei_id_or_code):
        # e.g. A00-A09
        return True
    return False


def normalize_string(s: str) -> str:
    s = unicodedata.normalize("NFKC", s)
    s = re.sub("[˗֊‐‑‒–⁃⁻₋−]+", "-", s)  # normalize hyphens
    s = re.sub("[﹣－ｰ—―─━ー]+", "ー", s)  # normalize choonpus
    return s
