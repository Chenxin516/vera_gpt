# Vera GPT

This package makes the OpenAI API accessible in a format similar to inference using trained ML models.
This allows OpenAI completions and batch calls to be integrated into other python applications, namely our Ray serving service.


## Installing

`pip install -e vera-gpt`


## Setup

Requires an OpenAI API key.
Assign the key to the `OPENAI_API_KEY` environment variable.


## Usage

### Endpoints

These are classes which are used to run "inference" on datasets of prompts by processing them and sending them to the appropriate endpoint.

#### [GPT](https://github.com/JunGroupProductions/vera-gpt/tree/main/docs/guide/gpt.md)

The standard completions endpoint.
Useable for streaming inference; provides an immediate result.

#### [GPTBatch](https://github.com/JunGroupProductions/vera-gpt/tree/main/docs/guide/gptbatch.md)

The endpoint for submitting a batch job.
Useable for performing inference on a set of prompts not requiring an immediate result.

The batch API provides much higher rate limits and 50% lower costs.

#### Ollama


### Batch Jobs

Classes for retrieving and extracting batch results.
These would be used in a separate process to monitor and receive batch results, and process them to their final inference desintations.

[Batch user guide](https://github.com/JunGroupProductions/vera-gpt/tree/main/docs/guide/batch.md)


### Models

This is a library of "models" which implement the `vera-gpt` endpoints to perform a specific task.
