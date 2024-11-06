## GPT


### *class* `vera_gpt.GPT`(*system_prompt=None, options={}*)

Make a standard completions call and receive a result immediately.

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

#### `__call__`(*user_prompt*)

Execute the completions call.

##### Parameters

user_prompt: *str*

&emsp;The prompt to which you want a response.

##### Returns

response: *str*

&emsp;`json` string representation of OpenAI response.


## Example

```
import json
from vera_gpt.models import GPT


model = GPT(system_prompt=SYSTEM_PROMPT)
result = model(USER_PROMPT)
print(result)
```
