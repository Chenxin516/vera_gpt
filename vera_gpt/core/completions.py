import io
import json


class Completions(dict):
    options = {
        "model": "gpt-4o-mini",
        "temperature": 1.5,
        "response_format": {"type": "json_object"},
        "seed": 42,
    }

    def __init__(
        self,
        user_prompt: str,
        system_prompt: str = None,
        options: dict = {},
    ) -> None:
        self.options = self.options | options
        self.messages = []
        if system_prompt:
            self.messages.append(
                {
                    "role": "system",
                    "content": system_prompt,
                }
            )
        self.messages.append(
            {
                "role": "user",
                "content": user_prompt,
            }
        )
        self.options["messages"] = self.messages
        super().__init__(self.options)


class Tasks:
    def __init__(
        self,
        method: str = "POST",
        url: str = "/v1/chat/completions",
    ) -> None:
        self.task_config = {
            "method": method,
            "url": url,
        }

    def generate_tasks(
        self,
        user_prompts: list[str],
        system_prompt: str = None,
        completions_options: dict = {},
        task_prefix: str = "task",
    ) -> io.BytesIO:
        self.tasks = []
        f = io.BytesIO()
        for i, user_prompt in enumerate(user_prompts):
            task = self.task_config.copy()
            task_id = f"{task_prefix}-{i}"
            task["custom_id"] = task_id

            completions = Completions(
                user_prompt,
                system_prompt,
                completions_options,
            )
            task["body"] = completions
            self.tasks.append(task)

            task_line = json.dumps(task) + "\n"
            f.write(task_line.encode("utf-8"))

        f.seek(0)
        return f
