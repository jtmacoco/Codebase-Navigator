from transformers import StoppingCriteria, StoppingCriteriaList
class StoppingCriteriaSub(StoppingCriteria):
    def __init__(self,eos_token):
        self.eos_token_id = eos_token
    def __call__(self,input_ids,scores, **kwargs):
        return input_ids[0,-1].item()==self.eos_token_id

