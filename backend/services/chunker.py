from collections import defaultdict
''' 
Split function code into smaller chunks based on byte size

Args:
    methods (dict): A dict mapping function names to their metadata
    max_bytes (int, optional): Max size in bytes for each chunk

Returns:
    list[dict]: A list of dict's containing code data
''' 
def chunk_code(methods:dict, max_bytes=15_000_000):
    chunks_with_meta = []
    for name, data in methods.items():
        code = data['code']
        func_type = data.get('type')
        current_chunk = []
        current_size = 0
        chunk_index = 0
        for line in code.splitlines(keepends=True):
            line_bytes = len(line.encode('utf-8'))
            if current_size + line_bytes > max_bytes:
                chunks_with_meta.append({
                    "function_name":name,
                    "chunk_index":chunk_index,
                    "type":func_type,
                    "code": "".join(current_chunk),
                    "file": data['file'],
                    "file_path":data['file_path']
                })
                current_chunk = [line]
                current_size = line_bytes
                chunk_index+=1
            else:
                current_chunk.append(line)
                current_size+=line_bytes
        if current_chunk:
            chunks_with_meta.append({
                    "function_name":name,
                    "chunk_index":chunk_index,
                    "type":func_type,
                    "code": "".join(current_chunk),
                    "file": data['file'],
                    "file_path":data['file_path']
                })
    return chunks_with_meta

'''
Chunks an entire file based on number of bytes

Args:
    file (dict): A dict containing the content of the file
    max_bytes (int,optional): The max number of bytes before chunking

Returns
    list[dict]: A list of dict's containing code data
'''
def chunk_file(file:dict, max_bytes=4_000_000):
    chunks_with_meta = []
    for name, data in file.items():
        code = data['code']
        current_chunk = []
        current_size = 0
        chunk_index = 0
        for line in code.splitlines(keepends=True):
            line_bytes = (len(line.encode('utf-8')))
            if current_size + line_bytes > max_bytes:
                chunks_with_meta.append({
                    "function_name":"N/A",
                    "chunk_index":chunk_index,
                    "type": "This is the entire file:{name}",
                    "code": "".join(current_chunk),
                    "file": name,
                    "file_path":data['file_path'],
                })
                current_chunk = [line]
                current_size = line_bytes
                chunk_index+=1
            else:
                current_chunk.append(line)
                current_size += line_bytes
        if current_chunk:
            chunks_with_meta.append({
                    "function_name":"N/A",
                    "chunk_index":chunk_index,
                    "type": "file",
                    "code": "".join(current_chunk),
                    "file": name,
                    "file_path":data['file_path'],
                })
    return chunks_with_meta