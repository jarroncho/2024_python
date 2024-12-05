import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import Trainer, TrainingArguments
from datasets import Dataset

# Load the tokenizer and model
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-1B")
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-1B")
vocab_size = tokenizer.vocab_size
print("Vocabulary size:", vocab_size)

# Example dataset
data = {
    "train": [
        {"input": "What is AI?", "output": "AI stands for Artificial Intelligence."},
        {"input": "What is Python?", "output": "Python is a programming language."}
    ],
    "validation": [
        {"input": "What is ML?", "output": "ML stands for Machine Learning."}
    ]
}

# Load datasets
train_dataset = Dataset.from_list(data["train"])
eval_dataset = Dataset.from_list(data["validation"])

def encode(examples):
    # Tokenize the input and output pairs
    model_inputs = tokenizer(
        examples["input"],
        text_pair=examples["output"],
        truncation=True,
        max_length=512,
        return_tensors='pt',
        add_special_tokens=False
    )

    # Set up labels: shift input_ids for causal language modeling
    labels = model_inputs['input_ids'].clone()
    
    # Set padding token if needed (optional, depending on your tokenizer configuration)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # Prepare model inputs
    model_inputs['labels'] = labels  # Add labels to model inputs
    return model_inputs

# Tokenize datasets
tokenized_train_dataset = train_dataset.map(encode, batched=True)
tokenized_eval_dataset = eval_dataset.map(encode, batched=True)

# Define training arguments
training_args = TrainingArguments(
    output_dir="./results",    
    num_train_epochs=3,
    learning_rate=2e-5,
    per_device_train_batch_size=2,
    logging_dir='./logs',
    evaluation_strategy="epoch",  # Optional: Track evaluation at the end of each epoch
)

# Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train_dataset,
    eval_dataset=tokenized_eval_dataset,
)

# Start training
trainer.train()

# Evaluate the model
trainer.evaluate()
