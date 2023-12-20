from openai import OpenAI


class ChatGPT:
    def __init__(self, api_key,model="gpt-3.5-turbo"):
        self.api_key = api_key
        self.model=model
        self.max_tokens=1024
        #self.models = self.get_available_models()
        self.system_prompt="You are an ai"
        self.client = OpenAI(api_key=api_key)

    #def get_available_models(self):
        # TODO: The resource 'Engine' has been deprecated
        ## engines = openai.Engine.list()
        #return [engine.id for engine in engines.data]


    def start_session(self, model):
        if model not in self.models:
            raise ValueError("Model not available")
        self.session = self.client.chat.completions.create(model=model, api_key=self.api_key)

    
    def send_message(self,user_prompt):
        new_style=["gpt-3.5-turbo","gpt-4"]
        old_style=["text-davinci-002"]

        if self.model in old_style:
            # Use the OpenAI API to generate content based on title and context
            response = self.client.completions.create(engine=self.model,
            prompt=self.system_prompt,
            max_tokens=self.max_tokens,  # Adjust as needed
            n=1,  # Number of completions
            stop=None)
            text=response.choices[0].text
            return text

        if self.model in new_style:
            response = self.client.chat.completions.create(model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_prompt }
            ])
            text=response.choices[0].message.content.strip()
        return text



    def end_session(self):
        self.session = None

