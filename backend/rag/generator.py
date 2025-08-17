# Load model directly
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-4B-Instruct-2507")
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen3-4B-Instruct-2507")

messages = [
    {"role": "user", "content": "Who are you?"},
]
inputs = tokenizer.apply_chat_template(
	messages,
	add_generation_prompt=True,
    device_map="auto",
	tokenize=True,
	return_dict=True,
	return_tensors="pt",
).to(model.device)
#inputs = tokenizer(messages, return_tensors="pt").to(model.device)

with torch.inference_mode():
    outputs = model.generate(**inputs, max_new_tokens=40)
#response = tokenizer.decode(outputs[0], skip_special_tokens=True)
res = (tokenizsr.decode(outputs[0][inputs["input_ids"].shape[-1]:]))
print(res)