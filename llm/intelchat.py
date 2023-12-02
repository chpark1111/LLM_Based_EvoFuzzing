import transformers

model_name = 'Intel/neural-chat-7b-v3-1'
model = transformers.AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = transformers.AutoTokenizer.from_pretrained(model_name)

def generate_response(system_input, user_input):

    # Format the input using the provided template
    prompt = f"### System:\n{system_input}\n### User:\n{user_input}\n### Assistant:\n"

    # Tokenize and encode the prompt
    inputs = tokenizer.encode(prompt, return_tensors="pt", add_special_tokens=False)

    # Generate a response
    outputs = model.generate(inputs, max_length=1000, num_return_sequences=1)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Extract only the assistant's response
    return response.split("### Assistant:\n")[-1]


# Example usage
system_input = "You are a math expert assistant. Your mission is to help users generate various math equations. Generate 10 equations (not same) like this with a little bit of variation (do not include any other words): "
user_input = "((sqrt(-10) + -13) * sqrt(-13))"
response = generate_response(system_input, user_input)
possible_strings = list(map(lambda x: x[3:], response.split('\n')[1:]))
print(possible_strings)