from tree_sitter import Language, Parser
from pathlib import Path
from tree_sitter_language_pack import get_language, get_parser
from constants.languages import LANGUAGES
from constants.methods import ALL_METHODS, FILTER_METHODS
from constants.ignore import should_ignore
'''
Filters methods if total number of methods is greater thanmax_size

Args:
    all_methods (dict): A dict mapping methods names to their data
                        where each value is a dict with "type" and "code" keys
    max_size (optional): Max number of methods to keep before filtering, defaults to 5,000

Returns:
    dict[str,dict]: A dict mapping method names to their code only, excluding unwanted methods
'''
def filter_methods(all_methods:dict,max_size=100_000):
    if len(all_methods)>max_size:
        allowed_types = FILTER_METHODS
        all_methods = {
            name: data 
            for name, data in all_methods.items()
            if data["type"] in allowed_types
        }
    return all_methods
    #return{name:data["code"] for name,data in all_methods.items()}

'''
Extracts the source code methods from a github repo, using Tree-sitter parser

Args:
    source_code (str): The source code for that file
    parser (Parser): The specific parser needed to parse the file (using tree-sitter)

Returns:
    list[dict]: A list of dictionaries each containing:
        "node": the Tree-sitter node of the method
        "name": the name of the method as a string
'''
def get_code_methods(source_code:str,parser:Parser):
    tree = parser.parse(bytes(source_code,'utf8'))
    root = tree.root_node
    target_type = ALL_METHODS

    def find_name(node):
        name_node = node.child_by_field_name("name")
        if name_node:
            return source_code[name_node.start_byte:name_node.end_byte]
        for child in node.children:
            if child.type == 'identifier':
                return source_code[child.start_byte:child.end_byte]
            found = find_name(child)
            if found:
                return found
        return ""
    def recurse(node):
        if node.type in target_type:
            func_name=find_name(node)
            if not func_name:
                #print("function name not found")
                func_name= node.type
            yield {"node":node,"name":func_name}
        for child in node.children:
            yield from recurse(child)
    return list(recurse(root))
'''
Extract all the methods from a file

This function recursivley scans a file and parses the file using a language-specific
parsers (Tree-sitter) and collects all the methods

Args:
    file_path (str): Path to the file to scan

Returns:
    dict[str,dict]: A dict mapping method names to their code 
'''
def get_all_methods(file_path:str):
    path = Path(file_path)
    parsers = {}
    all_methods= {}
    for ext,lang_name in LANGUAGES.items():
        lang = get_language(lang_name)
        parser = Parser(lang)
        parsers[ext] = parser
    for file_path in path.rglob("*"):
        if file_path.is_file() and file_path.suffix in LANGUAGES.keys():
            parser = parsers[file_path.suffix]
            try:
                with open(file_path,'r',encoding='utf-8') as f:
                    content = f.read()
                methods = get_code_methods(content,parser)
                for method_node in methods:
                    method_code = content.encode('utf-8')[method_node["node"].start_byte:method_node["node"].end_byte].decode('utf-8')
                    method_name = str(method_node["name"])
                    #all_methods[method_name] = str(method_code)
                    all_methods[method_name] = {
                        "code":method_code,
                        "type":method_node["node"].type,
                        "file":file_path.name
                    }
                tree = parser.parse(bytes(content,'utf8'))
            except Exception as e:
                print(f"ERROR READING {file_path}:{e}")
    all_methods=filter_methods(all_methods)
    return all_methods

def get_all_code(file_path:str):
    path = Path(file_path)
    file_code = {}
    for file_path in path.rglob("*"):
        if file_path.is_file():
            if should_ignore(file_path):
                continue
            try:
                rel_path = file_path.relative_to(path)
                with open(file_path,'r',encoding='utf-8') as f:
                    content = f.read()
                    file_code[str(file_path.name)]=str(content)
            except UnicodeDecodeError:
                pass
            except Exception as e:
                print(f"ERROR READING {file_path}:{e}")
    return  file_code