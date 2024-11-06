import io
import json
import time
from datetime import timedelta

import openai
from openai import OpenAI


class BatchResponse:
    def __init__(
        self,
        batch_job: dict,
    ) -> None:
        self.job_id = batch_job["id"]
        self.job_agent = GPTBatchAgent(self.job_id)

    @staticmethod
    def extract_content(line: str) -> dict:
        chat_completions = json.loads(line)["response"]["body"]
        content = chat_completions["choices"][0]["message"]["content"]
        return json.loads(content)

    def __call__(
        self,
        update_interval: int = 300,
    ) -> list[dict]:
        _ = self.job_agent.wait_result(update_interval=update_interval)
        batch_result = self.job_agent.retrieve_result()
        f = io.BytesIO(batch_result)
        self.response = [
            __class__.extract_content(line) for line in f.readlines()
        ]
        return self.response


class GPTBatchAgent:
    pending_status = [
        "validating",
        "in_progress",
        "finalizing",
    ]
    failure_status = [
        "failed",
        "expired",
        "cancelling",
        "cancelled",
    ]
    completed_status = "completed"

    def __init__(
        self,
        batch_job_id: str,
    ) -> None:
        self.client = OpenAI()
        self.batch_job_id = batch_job_id
        self.batch_job = self.client.batches.retrieve(self.batch_job_id)

    def refresh(self) -> None:
        self.batch_job = self.client.batches.retrieve(self.batch_job_id)

    def status(self) -> tuple[str, int]:
        self.refresh()
        return self.batch_job.status, self.batch_job.request_counts

    def wait_result(
        self,
        update_interval: int,
    ) -> openai.types.batch.Batch:
        print(f"Awaiting batch '{self.batch_job_id}'")
        print(f"Updating at {update_interval}s intervals")

        status, counts = self.status()
        while status != self.completed_status:
            elapsed = timedelta(
                seconds=int(time.time() - self.batch_job.created_at)
            )
            if status in self.failure_status:
                print(f"({elapsed}) Batch '{self.batch_job_id}' {status}")
                print(counts)
                return self.batch_job
            elif status in self.pending_status:
                print(f"({elapsed}) Batch '{self.batch_job_id}' in progress")
                print(counts)
            else:
                print(
                    f"({elapsed}) Batch '{self.batch_job_id}' status unknown"
                )
                return self.batch_job
            time.sleep(update_interval)
            status, counts = self.status()

        elapsed = timedelta(
            seconds=int(
                self.batch_job.completed_at - self.batch_job.created_at
            )
        )
        print(f"({elapsed}) Batch '{self.batch_job_id}' completed")
        print(counts)
        return self.batch_job

    def retrieve_result(self) -> bytes:
        status, _ = self.status()
        if status != self.completed_status:
            raise Exception(f"No result for batch '{self.batch_job_id}'")

        if self.batch_job.output_file_id:
            file_id = self.batch_job.output_file_id
        else:
            file_id = self.batch_job.error_file_id
        result = self.client.files.content(file_id).content
        return result
