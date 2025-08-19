from transformers import AutoTokenizer, AutoModel
import torch, gc
# Load model directly
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer = AutoTokenizer.from_pretrained("Salesforce/codet5p-110m-embedding",trust_remote_code=True, torch_dtype="auto")
model = AutoModel.from_pretrained("Salesforce/codet5p-110m-embedding",trust_remote_code=True, torch_dtype="auto").to(device)

model.eval()

@torch.inference_mode()
def embed(code_chunks: list, batch_size=32, use_fp16=True):
    all_embeddings = []
    for i in range(0,len(code_chunks),batch_size):
        batch = code_chunks[i:i+batch_size]

        inputs = tokenizer(batch,return_tensors="pt",truncation=True,padding=True,max_length=512)
        inputs = {k:v.to(device)for k,v in inputs.items()}

        if use_fp16 and device.type == "cuda":
            with torch.amp.autocast(device_type='cuda',dtype=torch.float16):
                outputs = model(**inputs)
        else:
            outputs = model(**inputs)

        cls_embeddings = outputs.to("cpu")
        all_embeddings.append(cls_embeddings)
    
    all_embeddings = torch.cat(all_embeddings,dim=0)
    return all_embeddings.tolist()