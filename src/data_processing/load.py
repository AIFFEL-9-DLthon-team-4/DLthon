import os
import pandas as pd
import numpy as np
import torch
from datasets import Dataset
from sklearn.model_selection import train_test_split
from src.training.config.model_case import tokenizer

current_file_path = os.path.abspath(__file__)  # 이 파이썬 파일의 절대경로
base_path = "/".join(current_file_path.split("/")[:-3]) + "/data"


datset_path_dict = {
    "org": "/_original/",  # 원본 DKTC 데이터셋
    "01": "/ds_1/",        # 구두점 전처리 1
    "02": "/ds_2/",
    "03": "/ds_3/",
    "tmp": "/ds_tmp/",
}

df_1 = pd.read_csv(base_path + datset_path_dict["01"] + "train_processed.csv")
# df_2 = pd.read_csv(base_path + datset_path_dict["02"] + "train.csv")
# df_3 = pd.read_csv(base_path + datset_path_dict["03"] + "train.csv")
df_tmp = pd.read_csv(base_path + datset_path_dict["tmp"] + "train_tmp.csv")


# df_1_train, df_1_test = train_test_split(df_1, test_size=0.1)
# df_tmp_train, df_tmp_test = train_test_split(df_tmp, test_size=0.1)

def get_trainable_dataset(data, inputs, max_len, tokenizer):
    # making input dictionary
    data['input_ids'] = inputs

    # 0 padding
    data['input_ids'] = data['input_ids'].apply(lambda x: x[0] + [tokenizer.pad_token_id] * (max_len - len(x[0])))

    input_ids = torch.tensor(data['input_ids'])
    labels = torch.tensor(data['label'])
    attention_mask = [
        np.ones(len(encoded_seq)) + np.zeros(max_len - len(encoded_seq) + 1)
        for encoded_seq in inputs
    ]
    attention_mask = torch.tensor(attention_mask)
    token_type_ids = torch.tensor(np.zeros((len(input_ids),max_len)))

    data = {'input_ids':input_ids, 'attention_mask':attention_mask, 'labels':labels}
    data = Dataset.from_dict(data)

    # train test split
    train, test = data.train_test_split(test_size=0.1)['train'], data.train_test_split(test_size=0.1)['test']
    return (train, test)


max_len = 300


inputs = []
token_type_ids = []
for example in df_tmp['text']:
  if len(example) <= max_len:
    inputs.append(tokenizer["kcbert-base"](example, return_tensors='pt')['input_ids'].tolist())
  else:
    inputs.append(tokenizer["kcbert-base"](example[:max_len], return_tensors='pt')['input_ids'].tolist())

df_tmp_split = get_trainable_dataset(data=df_tmp,
                                     inputs=inputs,
                                     max_len=max_len,
                                     tokenizer=tokenizer["kcbert-base"])

# print(df_tmp_split[0])