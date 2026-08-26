from foundry_local_sdk import Configuration, FoundryLocalManager


class Chatbot:
    def __init__(self):


        self.manager = FoundryLocalManager.instance

        self.model = self.manager.catalog.get_model(
            "qwen2.5-0.5b"
        )

        self.model.download(
            lambda progress: print(
                f"\rChat modeli indiriliyor: {progress:.1f}%",
                end="",
                flush=True
            )
        )

        print()

        self.model.load()

        self.client = self.model.get_chat_client()

    def generate_answer(self, prompt):
        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]

        answer = ""

        for chunk in self.client.complete_streaming_chat(messages):
            if not chunk.choices:
                continue

            content = chunk.choices[0].delta.content

            if content:
                answer += content

        return answer

    def unload(self):
        self.model.unload()