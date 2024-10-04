from model_case import tokenizer, model
from transformers import TrainingArguments, Trainer

training_args = TrainingArguments(
    output_dir="run",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=2,
    weight_decay=0.01,
    eval_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    push_to_hub=True,
)

trainer_01 = Trainer(
    tokenizer=tokenizer["kogpt2-base-v2"],
    model=model["DialogRPT-updown"],
    model_init=None,
    args=training_args,
    train_dataset=tokenized_imdb["train"],
    eval_dataset=tokenized_imdb["test"],
    data_collator=data_collator,
    compute_metrics=compute_metrics,
)

trainer_02 = Trainer(
    tokenizer=tokenizer["kcbert-base"],
    model=model["bert-base-uncased-yelp-polarity"],
    model_init=None,
    args=training_args,
    train_dataset=tokenized_imdb["train"],
    eval_dataset=tokenized_imdb["test"],
    data_collator=data_collator,
    compute_metrics=compute_metrics,
)