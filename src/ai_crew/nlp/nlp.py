from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
import torch
from datasets import load_dataset

def fine_tune_model():
    # Load a pre-trained model and tokenizer
    model_name = "microsoft/DialoGPT-medium"
    model = AutoModelForCausalLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Load and preprocess the dataset
    dataset = load_dataset("emotion", split="train")
    def preprocess_function(examples):
        return tokenizer(examples["text"], truncation=True, padding="max_length", max_length=128)
    tokenized_dataset = dataset.map(preprocess_function, batched=True)

    # Define training arguments
    training_args = TrainingArguments(
        output_dir="./results",
        evaluation_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        num_train_epochs=3,
        weight_decay=0.01,
    )

    # Initialize the Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
        eval_dataset=tokenized_dataset,
    )

    # Fine-tune the model
    trainer.train()

    # Save the fine-tuned model
    model.save_pretrained("./fine_tuned_model")
    tokenizer.save_pretrained("./fine_tuned_model")

if __name__ == "__main__":
    fine_tune_model()