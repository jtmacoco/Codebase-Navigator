# A mapping of code entity categories corresponding to node type names
# Basedon Tree-sitter grammars). Used for filtering parsed code entities
METHODS = {
    "functions": {
        "function_definition",
        "method_definition",
        "function_declaration",
        "constructor",
        "arrow_function",
        "lambda_expression"
    },
    "types": {
        "class_definition",
        "class_declaration",
        "struct_specifier",
        "interface_declaration",
        "trait_definition",
        "enum_declaration",
        "enum_specifier"
    },
    "variables": {
        "variable_declaration",
        "lexical_declaration",
        "const_declaration",
        "field_definition",
        "property_signature"
    },
    "modules": {
        "module_definition",
        "namespace_definition",
        "package_declaration"
    },
    "imports_exports": {
        "import_statement",
        "import_declaration",
        "export_statement",
        "export_clause"
    }
}
# Set containing all node type names from every categor
ALL_METHODS = set().union(*METHODS.values())

#Node types to keep when filtering larger codebases (i.e. greater than 5,000)
FILTER_METHODS = METHODS["functions"].union(METHODS['types'])