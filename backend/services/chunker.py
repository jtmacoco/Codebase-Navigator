from collections import defaultdict
''' 
Split function code into smaller chunks based on byte size

Args:
    functions (dict): A dictionary containing the function names to their code
    max_bytes (int, optional): Max size in bytes for each chunk. Default value 30,000

Returns:
    dict[str,list[str]]: Dic mapping functions names to list of code chunks
''' 
def chunk_code(functions:dict,max_bytes=30_000):
    chunks = defaultdict(list)
    for name, code in functions.items():
        current_chunk = []
        current_size = 0
        chunk_id = 0
        for line in code.splitlines(keepends=True):
            line_bytes = (len(line.encode('utf-8')))
            if current_size + line_bytes > max_bytes:
                chunks[name].append("".join(current_chunk))
                current_chunk = [line]
                current_size = line_bytes
            else:
                current_chunk.append(line)
                current_size += line_bytes
        if current_chunk:
            chunks[name].append("".join(current_chunk))
    return chunks