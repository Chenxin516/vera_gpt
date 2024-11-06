## Batch Jobs

```
from vera_gpt import batch
```

Classes for retrieving and extracting batch results.


### *class* `batch.GPTBatchAgent`(*batch_job_id*)

Monitor the batch job and retrieve the result when complete.

##### Parameters

batch_job_id: *str*

&emsp;The batch job ID obtained from the batch job response.

#### `wait_result`(*update_interval=300*)

##### Parameters

Update interval: *int=300*

&emsp;The amount of delay between checks for the batch job status.

##### Returns

batch_job: *Batch*

&emsp;An OpenAI batch object which contains the final batch job status and attributes.

#### `retrieve_result`()

##### Returns

result: *bytes*

&emsp;The raw content extracted from the OpenAI batch output file.


### *class* `batch.BatchResponse`(*batch_result*)

Extracts the serveable content from the output batch result and formats it into an appropriate API response.

##### Parameters

batch_result: *bytes*

&emsp;The raw content extracted from the OpenAI batch output file.

##### Attributes

result: *list[bytes]*

&emsp;A list of individual OpenAI completions responses to batch prompts.

response: *str*

&emsp;`json` string representation of the result.
