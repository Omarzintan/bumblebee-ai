from features.default import BaseFeature
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


class Feature(BaseFeature):
    def __init__(self, bumblebee_api):
        self.tag_name = "chatbot"
        self.patterns = []
        self.bs = bumblebee_api.get_speech()
        self.step = 0
        self.model_name = "microsoft/DialoGPT-medium"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)

    def action(self, spoken_text, arguments_list: list = []):
        if isinstance(spoken_text, list):
            spoken_text = ' '.join(spoken_text)

        # encode the user input and add end of string token
        input_ids = self.tokenizer.encode(
            spoken_text + self.tokenizer.eos_token, return_tensors="pt"
        )

        # concatenate new user input with chat history (if there is)
        bot_input_ids = torch.cat(
            [chat_history_ids, input_ids], dim=-1
        ) if self.step > 0 else input_ids

        # generate a bot response
        chat_history_ids = self.model.generate(
            bot_input_ids,
            max_length=1000,
            do_sample=True,
            top_p=0.95,
            top_k=50,
            temperature=0.75,
            pad_token_id=self.tokenizer.eos_token_id,
        )
        # print the output
        output = self.tokenizer.decode(
            chat_history_ids[:, bot_input_ids.shape[-1]:][0],
            skip_special_tokens=True
        )
        # print(f"DialoGPT: {output}")
        self.bs.respond(output)
        return output
