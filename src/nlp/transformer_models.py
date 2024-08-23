
from transformers import GPT2Model

def build_transformer():
    model = GPT2Model.from_pretrained('gpt2')
    return model
