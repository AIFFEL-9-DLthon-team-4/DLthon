import logging
from transformers import PreTrainedTokenizerFast, AutoTokenizer  # Tokenizer
from transformers import GPT2ForSequenceClassification  # 1. GPT model import & initialization
from transformers import BertForSequenceClassification  # 2. BERT model import & initialization

num_labels = 5

# TODO: make the pair as a class for better abstraction
# class TokenizerModelPair:
#     def __init__(self, tokenizer_src_method: PreTrainedTokenizerFast | AutoTokenizer, model_name: str, **kwargs):
#         self.tokenizer = tokenizer_src_method.from_pretrained(model_name,
#                                                               kwargs)

tokenizer = {
    "kogpt2-base-v2": PreTrainedTokenizerFast.from_pretrained("skt/kogpt2-base-v2",
                                                              bos_token='</s>',
                                                              eos_token='</s>',
                                                              unk_token='<unk>',
                                                              pad_token='<pad>',
                                                              mask_token='<mask>'),
    
    "kcbert-base": AutoTokenizer.from_pretrained("beomi/kcbert-base"),
}


model = {
    # "DialogRPT-updown": GPT2ForSequenceClassification.from_pretrained("microsoft/DialogRPT-updown",
    #                                                                   num_labels=num_labels,
    #                                                                   problem_type="multi_label_classification"),
    
    # "bert-base-uncased-yelp-polarity": BertForSequenceClassification.from_pretrained("textattack/bert-base-uncased-yelp-polarity",
    #                                                                                  num_labels=num_labels,
    #                                                                                  problem_type="multi_label_classification"),
    
    "kcbert-base": BertForSequenceClassification.from_pretrained("beomi/kcbert-base",
                                                                 num_labels=num_labels,
                                                                 ignore_mismatched_sizes=True,
                                                                 vocab_size = 30000),
}
    
    
def get_bert_model():
    return BertForSequenceClassification.from_pretrained("beomi/kcbert-base",
                                                         num_labels=num_labels,
                                                         ignore_mismatched_sizes=True,
                                                         vocab_size = 30000)


logging.info(get_bert_model())
