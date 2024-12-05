from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_name = "gpt2"  # or any other model you choose
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
input_text = "Please introduce Microsoft Windows 10. "

input_ids = tokenizer.encode(input_text, return_tensors="pt")
attention_mask = torch.ones(input_ids.shape, dtype=torch.long)



with torch.no_grad():  # Disable gradient calculation for inference    
    output = model.generate(input_ids, 
                            attention_mask=attention_mask, 
                            max_length=100,                             
                            num_return_sequences=1,
                            pad_token_id=tokenizer.eos_token_id,                            
                            top_k=50 ,        # Consider top 50 tokens
                            do_sample=True,                  
                            )

print("\n\nInput text:", input_text)

generated_text = tokenizer.decode(output[0],skip_special_tokens=True)
# Print the generated response
print("\ndecode output[0]: ",generated_text)


