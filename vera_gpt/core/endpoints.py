import os
import json
import requests

from openai import OpenAI

from .completions import Completions
from .completions import Tasks


class GPT:
    def __init__(
        self,
        system_prompt: str = None,
        completions_options: dict = {},
    ) -> None:
        self.client = OpenAI()
        self.system_prompt = system_prompt
        self.completions_options = completions_options

    def __call__(
        self,
        user_prompt: str,
    ) -> str:
        completions = Completions(
            user_prompt,
            self.system_prompt,
            self.completions_options,
        )

        chat_completion = self.client.chat.completions.create(**completions)
        response = chat_completion.choices[0].message.content
        return response


class GPTBatch:
    def __init__(
        self,
        system_prompt: str = None,
        completions_options: dict = {},
        endpoint: str = "/v1/chat/completions",
        completion_window: str = "24h",
    ) -> None:
        self.client = OpenAI()
        self.system_prompt = system_prompt
        self.completions_options = completions_options
        self.endpoint = endpoint
        self.completion_window = completion_window

    def __call__(
        self,
        user_prompts: list[str],
    ) -> dict:
        tasks = Tasks()
        task_file = tasks.generate_tasks(
            user_prompts,
            system_prompt=self.system_prompt,
            completions_options=self.completions_options,
        )
        batch_file = self.client.files.create(
            file=task_file,
            purpose="batch",
        )
        batch_job = self.client.batches.create(
            input_file_id=batch_file.id,
            endpoint=self.endpoint,
            completion_window=self.completion_window,
        )
        response = batch_job.__dict__
        del response["request_counts"]
        return response


class Ollama:
    OLLAMA_API_ENDPOINT = os.environ.get("OLLAMA_API_ENDPOINT")

    def __init__(self, options={}):
        # Change this value to any model you have already pulled using ollama
        DEFAULT_OPTIONS = {
            "model": "mistral",
        }
        self.options = DEFAULT_OPTIONS | options

    def __call__(self, prompt):
        r = requests.post(
            f"{self.OLLAMA_API_ENDPOINT}/api/generate",
            json={
                "model": self.options["model"],
                "prompt": prompt,
                "context": [],
            },
            stream=True,
        )
        r.raise_for_status()

        for line in r.iter_lines():
            body = json.loads(line)
            response_part = body.get("response", "")
            # the response streams one token at a time
            # print that as we receive it
            print(response_part, end="", flush=True)

            if "error" in body:
                raise Exception(body["error"])

            if body.get("done", False):
                return body["context"]
