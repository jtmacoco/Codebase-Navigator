from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from rag.stoppingCriteria import StoppingCriteriaSub
from transformers import StoppingCriteriaList
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
class Generator:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct")
        self.model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct",
        device_map="auto",
        torch_dtype=torch.float16,
        )

    '''
    Generates a response based on the user query and adds context using 
    data chunks for context

    Args:
        user_query: The user query string to respond too
        data_chunks_fine: The fine-grained data chunks retrieved
        data_chunks_medium: The medium-grained data chunsk retrieved
    
    Returns:
        str: The model-generated reponse to the query
    '''
    def generate_response(self,user_query:str,data_chunks_fine:list,data_chunks_medium:list):
        self.model.eval()
        messages = [
            {"role": "system", "content":"You are a codebase assistant helping explain any code or file in this repository. Here are code snippets as context for what the user asked"}
        ]
        for data in data_chunks_fine:
            messages.append({"role":"assistant",
            "content":f"file_path:{data['file_path']}\n\nfile_name:{data['file']}\n\n method type: {data['type']}\n\n code:{data['code']}"
            })
        for data in data_chunks_medium:
            messages.append({"role":"assistant",
            "content":f"file_path:{data['file_path']}\n\nfile_name:{data['file']}\n\n method type: {data['type']}\n\n code:{data['code']}"
            })
        messages.append({"role":"user","content":user_query})
        inputs = self.tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt",
        ).to(self.model.device)
        stopping = StoppingCriteriaList([StoppingCriteriaSub(self.tokenizer.eos_token_id)])
        with torch.inference_mode():
            outputs = self.model.generate(**inputs, max_new_tokens=512,use_cache=True,stopping_criteria=stopping)
        response = (self.tokenizer.decode(outputs[0][inputs["input_ids"].shape[-1]:]))
        return response[:-10]
        

