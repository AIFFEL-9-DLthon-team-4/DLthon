import os, sys
sys.path.insert(1, "/".join(os.path.abspath('').split("/")[:-2]))

from src.data_processing import load
from src.training.config.model_case import tokenizer, model, get_bert_model
from transformers import TrainingArguments, Trainer, DataCollatorWithPadding

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
    # push_to_hub=True,
)

# trainer_01 = Trainer(
#     tokenizer=tokenizer["kogpt2-base-v2"],
#     model=model["DialogRPT-updown"],
#     model_init=None,
#     args=training_args,
#     train_dataset=load.df_1_train,
#     eval_dataset=load.df_1_test,
#     data_collator=DataCollatorWithPadding(tokenizer=tokenizer["kogpt2-base-v2"]),
#     compute_metrics=None,
# )

trainer_02 = Trainer(
    tokenizer=tokenizer["kcbert-base"],
    model=model["kcbert-base"],
    model_init=get_bert_model,
    args=training_args,
    train_dataset=load.df_tmp_split[0],
    eval_dataset=load.df_tmp_split[1],
    data_collator=DataCollatorWithPadding(tokenizer=tokenizer["kcbert-base"]),
    compute_metrics=None,
)

# print(load.df_1_train)
trainer_02.train()