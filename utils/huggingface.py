from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os

hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
MODEL_NAME = "tiiuae/falcon-7b-instruct"

tokenizer = None
model = None

if hf_token:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, token=hf_token)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        token=hf_token,
        torch_dtype=torch.float16,
        trust_remote_code=True,
        device_map="auto"
    )

def send_to_huggingface(prompt, model, tokenizer):
    if not tokenizer or not model:
        return "Error: HuggingFace no está configurado."
    inputs = tokenizer(prompt, return_tensors="pt")
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=100, do_sample=True)
    response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    if "Asistente:" in response_text:
        response_text = response_text.split("Asistente:")[-1].strip()
    return response_text


