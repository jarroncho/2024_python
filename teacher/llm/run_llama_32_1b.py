
# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import pipeline
import torch


pipe=False
input_text = "Please introduce Microsoft Windows 10. "
# Use a pipeline as a high-level helper
if pipe:
  
    pipe = pipeline("text-generation", model="meta-llama/Llama-3.2-1B")

    
    # Generate a response
    responses = pipe(input_text, truncation=True, max_length=100, num_return_sequences=1)

    print("Pipe output: ",responses)
    # Print the generated response
    for response in responses:
        print(response['generated_text'])


# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-1B")
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-1B")

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

#print(f"pad_token_id={tokenizer.pad_token_id}")    
#print("Pad token:", tokenizer.pad_token)
#print("Unknown token:", tokenizer.unk_token)
#print("End of sequence token:", tokenizer.eos_token)  


# Encode the input text
input_ids = tokenizer.encode(input_text, return_tensors='pt')  # Convert to tensor

# Create attention mask (optional here since there's no padding, but good practice)
attention_mask = torch.ones(input_ids.shape, dtype=torch.long)

# Generate a response
# You can tweak max_length and num_return_sequences as needed
with torch.no_grad():  # Disable gradient calculation for inference    
    output = model.generate(input_ids, 
                            attention_mask=attention_mask, 
                            max_length=100,                             
                            num_return_sequences=1,
                            pad_token_id=tokenizer.eos_token_id,
                            temperature=0.7,  # Adjust to control randomness
                            top_k=50,         # Consider top 50 tokens
                            top_p=0.95 
                            )

#print("output: ",output)
# Decode the generated output back to text
generated_text = tokenizer.decode(output[0],skip_special_tokens=True)

# Print the generated response
print("decode output[0]: ",generated_text)



