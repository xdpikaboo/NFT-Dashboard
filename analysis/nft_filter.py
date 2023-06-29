from transformers import AutoModel, AutoTokenizer, AutoModelForSequenceClassification
from datasets import *
from transformers import TextClassificationPipeline
import re
from utils import logging
from transformers.pipelines.pt_utils import KeyDataset
import torch


class NFT_Filter:
    def __init__(self, tokenizer, model):
        self.device = 0 if torch.cuda.is_available() else -1
        self.tokenizer = tokenizer
        self.model = model
        self.pipe = TextClassificationPipeline(model=self.model, tokenizer=self.tokenizer, device=self.device)
        self.label_map = {'LABEL_0': 0, 'LABEL_1': 1}
        self.SEP = " </s> "

    def remove_emoji(self, data):
        data = str(data)
        emoj = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            u"\U00002500-\U00002BEF"  # chinese char
            u"\U00002702-\U000027B0"
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            u"\U0001f926-\U0001f937"
            u"\U00010000-\U0010ffff"
            u"\u2640-\u2642" 
            u"\u2600-\u2B55"
            u"\u200d"
            u"\u23cf"
            u"\u23e9"
            u"\u231a"
            u"\ufe0f"  # dingbats
            u"\u3030"
                        "]+", re.UNICODE)
        
        s = re.sub(emoj, '', data)
        s = re.sub(r"[\n\t]*", "", s)
        return s

    def remove_twitter(self, s):
        remove = "https://twitter.com/"
        return s.replace(remove, '')

    def remove_link_hash(self, text):
        new_text = []

        for t in text.split(" "):
            t = '@user' if t.startswith('@') and len(t) > 1 else t
            t = 'http' if t.startswith('http') else t
            new_text.append(t)
        return " ".join(new_text)

    def preprocess_string(self, string):
        string = self.remove_link_hash(string)
        string = self.remove_emoji(string)
        return string

    def preprocess_input(self, acc_list):
        input_string = []
        for acc in acc_list:
            name = self.preprocess_string(acc['name'])
            twitter = self.remove_twitter(acc['twitter'])
            desc = self.preprocess_string(acc['description'])
            
            text = name + self.SEP + twitter + self.SEP + desc
            input_string.append(text)
        return input_string

    def predict(self, acc_list):
        input_list = self.preprocess_input(acc_list)
        dataset = Dataset.from_dict({'text':input_list})
        results = self.pipe(KeyDataset(dataset, 'text'))
        preds = [self.label_map[result['label']] for result in results]
        return preds