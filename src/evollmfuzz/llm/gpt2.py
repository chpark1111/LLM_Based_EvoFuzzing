import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load pre-trained GPT-2 model and tokenizer
model_name = "gpt2-large"  # You can also use other variations like "gpt2-medium", "gpt2-large", etc.
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Set the device (CPU or GPU)
device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)

# Set the model to evaluation mode
model.eval()

# Generate text
prompt = """Generate similar (not same) equations like this with python (do not include any imports, prints and other words. Just equations in python): (tan(-2) + sqrt(-3))"""
input_ids = tokenizer.encode(prompt, return_tensors="pt").to(device)
output_ids = model.generate(input_ids, max_length=500, num_beams=5, no_repeat_ngram_size=2, top_k=50, top_p=0.95)

generated_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
print("Generated text:", generated_text)