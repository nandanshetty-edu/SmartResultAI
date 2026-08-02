import re


SUBJECT_FIX = {

    "1BMATS20\n1": "1BMATS201",

    "1BPHYS20\n2": "1BPHYS202",

    "1BCEDS20\n3": "1BCEDS203",

    "1BPOPL20\n7": "1BPOPL207",

    "1BESC204\nC": "1BESC204C",

}


def normalize_subject(code):

    code = str(code).strip()

    code = code.replace("\r", "")

    if code in SUBJECT_FIX:

        return SUBJECT_FIX[code]

    return code


def clean(value):

    if value is None:

        return ""

    return re.sub(r"\s+", " ", str(value)).strip()