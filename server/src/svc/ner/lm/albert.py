import torch
from transformers import  AlbertForTokenClassification, AutoTokenizer, AlbertForQuestionAnswering, logging
from typing import List, Tuple

label_list = [
    'B-LOC', 
    'B-MISC', 
    'B-ORG', 
    'B-PER', 
    'I-LOC', 
    'I-MISC', 
    'I-ORG', 
    'I-PER', 
    'O'
]

logging.set_verbosity_error()

class AlbertQA:
    def __init__(self, model_name: str = "albert-base-v2", device: str = 'cpu'):
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AlbertForQuestionAnswering.from_pretrained(model_name)

        except Exception as e:
            raise RuntimeError(f"Error downloading model/tokenizer: {e}")

        self.model = self.model.eval()
        self.args = {}
        self.device = device
            


    def answer(self, question: str, context: str, **kwargs: dict) -> str:
        for key in kwargs:
            if key in self.args:
                self.args[key] = kwargs[key]

        inputs = self.tokenizer(question, context, return_tensors="pt", padding=True, truncation=True)
        inputs = {key: value.to(self.device) for key, value in inputs.items()}
        
        outputs = self.model(**inputs)

        answer_start_scores = outputs.start_logits
        answer_end_scores = outputs.end_logits

        answer_start = torch.argmax(answer_start_scores)
        answer_end = torch.argmax(answer_end_scores) + 1
        input_ids = inputs["input_ids"].tolist()[0]
        answer = self.tokenizer.convert_tokens_to_string(
            self.tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end])
        )

        answer = answer.replace("[CLS]", "").replace("[SEP]", " ").replace("<s>", "").replace("</s>", "").strip()
        return answer
 
class AlbertNER:
    def __init__(self, model_name: str = "albert-base-v2", device: str = "cpu"):
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AlbertForTokenClassification.from_pretrained(model_name, num_labels=9)
            self.model = self.model.eval()
        except Exception as e:
            raise e

    def extract(self, text: str, **kwargs: dict) -> List[Tuple[str, str]]:
        for key in kwargs:
    	    if key in self.args:
                self.args[key] = kwargs[key]

        tokens = self.tokenizer.tokenize(self.tokenizer.decode(self.tokenizer.encode(text)))
        inputs = self.tokenizer.encode(text, return_tensors="pt")

        outputs = self.model(inputs, **kwargs)[0]
        predictions = torch.argmax(outputs, dim=2)
        return [(token, label_list[prediction]) for token, prediction in zip(tokens, predictions[0].tolist())]
