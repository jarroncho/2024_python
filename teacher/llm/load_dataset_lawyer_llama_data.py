from transformers import AutoTokenizer, AutoModelForCausalLM
from datasets import load_dataset
import time

# Load the tokenizer and model
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-1B")
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-1B")

vocab_size = tokenizer.vocab_size
print("Vocabulary size:", vocab_size)

# Load the lawyer_llama_data dataset
dataset = load_dataset("Skepsun/lawyer_llama_data", split='train')
#dataset = load_dataset("tim9510019/llama2_QA_Economics_230915", split='train')
dataset = dataset.select(range(5))

def preprocess_function(examples):
    print(examples)   
    #time.sleep(30)
    inputs = [example for example in examples.data['instruction']]
    #inputs = [example for example in examples.data['input']]
    #print(inputs)
    outputs = [example for example in examples.data['output']]
    #outputs = [example for example in examples.data['Answer']]
    #tokenizer.add_special_tokens({'pad_token': '[PAD]'})
    
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model_inputs = tokenizer(inputs, text_pair=outputs, truncation=True, padding="max_length", max_length=512,add_special_tokens=False)
    print("Tokens:", model_inputs)
    # Check for token IDs exceeding vocab size

    for input_ids in model_inputs["input_ids"]:
        if max(input_ids) >= tokenizer.vocab_size:
            print("Token ID exceeds vocabulary size:", max(input_ids))
    return model_inputs            
        

tokenized_dataset = dataset.map(preprocess_function, batched=True)


# Display the dataset content
print(dataset)
print(dataset[0])



