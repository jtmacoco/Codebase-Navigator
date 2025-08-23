from constants.languages import LANGUAGES
from constants.methods import METHODS
import re
def filter_query(user_query:str):
    filter_dict = {}
    keyword_to_methods = {
        "function":"functions",
        "class":"types",
        "variable":"variables",
        "import":"import_exports",
        "export":"import_exports"
    }
    for key_word, method in keyword_to_methods.items():
        try:
            if re.search(rf"\b{key_word}\b",user_query,re.IGNORECASE):
                filter_dict["type"]= {"$in": list(METHODS[method]) }
                break
        except Exception as e:
            print(e)
    extension_patter = "|".join(re.escape(ext) for ext in LANGUAGES.keys())
    file_match = re.search(rf"\b[\w\-.]+(?:{extension_patter})\b",user_query)
    if file_match:
        filter_dict["file"] = {"$eq":file_match.group(0)}
    return filter_dict