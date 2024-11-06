## GPTBatch


### *class* `vera_gpt.GPTBatch`(*system_prompt=None, options={}, endpoint='/v1/chat/completions', completion_window='24h',*)

Submit a set of completions tasks to the batch API. Batches are quoted to complete within 24 hours, but "often more quickly".

The batch API provides much higher rate limits and 50% lower costs.

##### Parameters

system_prompt: *str=None*

&emsp;Initial set of instructions that serve as the starting point when starting a new chat session.

options: *dict={}*

&emsp;Options to add to or overwrite default completions options.
Defaults are:
```
{
    "model": "gpt-4-turbo-preview",
    "temperature": 1.5,
    "response_format": {"type": "json_object"},
    "seed": 42,
}
```

endpoint: *str='/v1/chat/completions'*

&emsp;The endpoint to which tasks are submitted. The other available endpoint is '/v1/embeddings'

completion_window: *str='24h'*

&emsp;Currently the only available competion window is 24 hours.

#### `__call__`(*user_prompts*)

Submits the batch job containing prompts to evaluate.

##### Parameters

user_prompts: *iter[str]*

&emsp;An iterable containing promopts to evaluate as strings.

##### Returns

response: *str*

&emsp;`json` string representation of a batch job, critically containing the batch ID required to retrieve the job and results.


## Example

```
import json

from vera_gpt.models import GPTBatch

from vera_gpt.batch import GPTBatchAgent
from vera_gpt.batch import BatchResponse


model = GPTBatch(system_prompt=SYSTEM_PROMPT)
batch_job = model(USER_PROMPTS)
print(batch_job)
```
```
'{
    "id": "batch_giylFdYWU3cjgRQ0KCld8P7M",
    "completion_window": "24h",
    "created_at": 1716743427,
    "endpoint": "/v1/chat/completions",
    "input_file_id": "file-IxQmP359pCKgEsSXvEkVf76E",
    "object": "batch",
    "status": "validating",
    "cancelled_at": null,
    "cancelling_at": null,
    "completed_at": null,
    "error_file_id": null,
    "errors": null,
    "expired_at": null,
    "expires_at": 1716829827,
    "failed_at": null,
    "finalizing_at": null,
    "in_progress_at": null,
    "metadata": null,
    "output_file_id": null
}'
```
```
batch_job_id = json.loads(batch_job)["id"]
agent = GPTBatchAgent(batch_job_id)
result = agent.wait_result()
```
```
Awaiting batch result
Updating at 300s intervals
Batch batch_giylFdYWU3cjgRQ0KCld8P7M completed
```
```
response = BatchResponse(result).response
print(response)
```
