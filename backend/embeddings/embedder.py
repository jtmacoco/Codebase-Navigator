from transformers import AutoTokenizer, AutoModel
import torch, gc

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
model = AutoModel.from_pretrained("microsoft/codebert-base").to(device)
model.eval()
'''
Use to compare parallel to non-parallel
- Description:
    - Embeds code chunks use codebert model
- Args:
    - code_chunk (String): A chunk of code (currently functions from codebase)
- Return:
    - list[float]: vector embeddings representing the code chunks
def embed(code_chunks: list):
    inputs = tokenizer(code_chunks, return_tensors="pt", truncation=True, padding=True, max_length=512)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        output = model(**inputs)
        cls_embedding = output.last_hidden_state[:,0,:].detach().cpu()
    del inputs, output
    torch.cuda.empty_cache()
    gc.collect()
    return cls_embedding
'''

'''
Embed code chunks in batches

Supports mixed-precision (FP16) for faster GPU inference

Args:
     code_chunks(list): list of code chunks
     batch_size(int, optional): size of batch
     use_fp16(bool, optional): Whether to use FP16 percision always set to True

 Return:
    - list[lieft[float]]: A list of embeddings, one per code chunk
'''
@torch.inference_mode()
def embed(code_chunks: list, batch_size=64, use_fp16=True):
    all_embeddings = []
    for i in range(0,len(code_chunks),batch_size):
        batch = code_chunks[i:i+batch_size]

        inputs = tokenizer(batch,return_tensors="pt",truncation=True,padding=True,max_length=512)
        inputs = {k:v.to(device)for k,v in inputs.items()}
        if use_fp16:
            with torch.amp.autocast(device_type='cuda',dtype=torch.float16):
                outputs = model(**inputs)
        else:
            outputs = model(**inputs)

        cls_embeddings = outputs.last_hidden_state[:,0,:].cpu()
        all_embeddings.append(cls_embeddings)
    
    all_embeddings = torch.cat(all_embeddings,dim=0)
    return all_embeddings.tolist()