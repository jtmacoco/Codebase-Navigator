from transformers import AutoTokenizer, AutoModel
import torch

tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
model = AutoModel.from_pretrained("microsoft/codebert-base")

'''
- Description:
    - Embeds code chunks use codebert model
- Args:
    - code_chunk (String): A chunk of code (currently functions from codebase)
- Return:
    - list[float]: vector embeddings representing the code chunks
'''
def embed(code_chunks:str):
    inputs = tokenizer(code_chunks, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        output = model(**inputs)
        cls_embedding = output.last_hidden_state[:,0,:]
        return cls_embedding.squeeze()