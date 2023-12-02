import transformers
from src.check import check_valid_input

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


def mutatate_input_with_llm(user_input, num_gen):
    system_input = "You are a math expert assistant. Your mission is to help users generate various math equations. Do not include any other words. Do not generate same equations. You must make various variations from the given one. Generate %d equations (not same) like this: "%(min(10, num_gen))
    
    input_strings = set()
    while len(input_strings) != num_gen:
        response = generate_response(system_input, user_input)
        print(response)
        possible_strings = list(map(lambda x: x.strip(), response.split('\n')[1:]))
        print(possible_strings)
        for str_input in possible_strings:
            result = check_valid_input(str_input)
            if result == "Success":
                input_strings.add(str_input)
            
            if len(input_strings) == num_gen:
                break
    
    return list(input_strings)

if __name__ == "__main__":
    user_input = "((sqrt(-10) + -13) * sqrt(-13))"
    num_gen = 10
    print(mutatate_input_with_llm(user_input, num_gen))
