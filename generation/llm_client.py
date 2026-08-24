from openai import OpenAI

import config


class LLMClient:
    def __init__(self, api_key: str=config.GROQ_API_KEY,
                 model_name: str=config.GROQ_MODEL_NAME):

        self._api_key = api_key
        self._model_name = model_name

        self.client = OpenAI(
            api_key = api_key,
            base_url= "https://api.groq.com/openai/v1"
        )

    def generate(self, system_prompt: str, user_prompt: str)-> str :

        response = self.client.chat.completions.create(
           messages =[ 
                        {
                    "role": "system",
                    "content": system_prompt
                        },

                        {
                     "role": "user",
                    "content": user_prompt
                    }
                ],

            model = self._model_name
        )

        return response.choices[0].message.content



        