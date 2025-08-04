from openai import AzureOpenAI

class OpenAIClient:
    def __init__(self, endpoint, api_key, api_version, model_name):
        self.client = AzureOpenAI(
            api_version=api_version,
            azure_endpoint=endpoint,
            api_key=api_key,
        )
        self.model_name = model_name

    def get_completion(self, prompt, max_retries=5):
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.choices[0].message.content
            except Exception as e:
                if "429" in str(e):
                    time.sleep(60)  # Wait before retrying
                else:
                    raise e
        return None