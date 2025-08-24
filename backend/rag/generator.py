from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from constants.languages import LANGUAGES
from constants.methods import METHODS
from . import filterQuery
import torch
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

#to help speed up 
quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb4bit_use_double_quant=True
)
class Generator:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct")
        self.model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct",
        device_map="auto",
        torch_dtype=torch.float16,
        quantization_config=quant_config
        )
    
    '''
    Informs if a user query is about anything code related

    Args:
        query (str): The user's question or message
    
    Returns:
        bool: Returns true if any code is in the query else it's False
    
    '''
    def is_code_related(self,query:str):
        code_keywords = [
            "code", "function", "class", "method", "file", "repository",
            "python", "javascript", "java", "programming", "debug", "error",
            "script", "module", "import", "variable", "syntax"
        ]
        if len(filterQuery.filter_query(query)) > 0:
            return True
        q_lower = query.lower()
        for k, v in LANGUAGES.items():
            if q_lower == k or q_lower == v:
                return True
        return any(keyword in q_lower for keyword in code_keywords)

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
            {"role": "system", "content": "You are a versatile assistant capable of answering both code-related and general questions.\
                - For code-related queries (e.g. about repositories, files, functions, or programming), use the code context to ground your response. Only use the provided code context and avoid making up detaisl not present in the data.\
                - For non-code related queires, discard the code context and provide a concise, accurate answer based on general knowledge. \
                - If a query is ambiguous, ask for clarification to ensure accuracy. \
            "}
        ]
        if self.is_code_related(user_query):
            for data in data_chunks_fine:
                messages.append({"role":"assistant",
                "content":f"file_path:{data['file_path']}\n\nfile_name:{data['file']}\n\n method type: {data['type']}\n\n code:{data['code']}"
                })
            for data in data_chunks_medium:
                messages.append({"role":"assistant",
                "content":f"file_path:{data['file_path']}\n\nfile_name:{data['file']}\n\n method type: {data['type']}\n\n code:{data['code']}"
                })
        else:
            messages.append({"role":"assistant","content":" This is a non-code related query. I will answer based on general knowledge."})

        messages.append({"role":"user","content":user_query})
        inputs = self.tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt",
        ).to(self.model.device)
        with torch.inference_mode():
            outputs = self.model.generate(**inputs, max_new_tokens=512,use_cache=True,eos_token_id=self.tokenizer.eos_token_id)
        response = (self.tokenizer.decode(outputs[0][inputs["input_ids"].shape[-1]:],skip_special_tokens=True))
        return response.strip()
        

