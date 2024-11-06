import types
import json
from abc import abstractmethod

from .. import ModelBase

from ... import GPT
from ... import GPTBatch
from ... import batch

from .system_prompts import SENTIMENT_PROMPT
from .system_prompts import SHOPPER_PROMPT
from .system_prompts import PURCHASE_PROMPT


class SentimentBase(ModelBase):
    @property
    @abstractmethod
    def prompt(self):
        pass

    async def async_predict(
        self,
        content: str,
    ) -> types.CoroutineType:
        response = GPT(
            system_prompt=self.prompt,
            completions_options=self.completions_options,
        )(content)
        output = json.loads(response).get("summary")
        return output

    async def async_predict_batch(
        self,
        contents: iter,
        update_interval: int,
    ) -> types.CoroutineType:
        batch_job = GPTBatch(
            system_prompt=self.prompt,
            completions_options=self.completions_options,
        )(contents)
        response = batch.BatchResponse(batch_job)(
            update_interval=update_interval
        )
        outputs = [x.get("summary") for x in response]
        return outputs


class Sentiment(SentimentBase):
    prompt = SENTIMENT_PROMPT


class Purchase(SentimentBase):
    prompt = PURCHASE_PROMPT


class Shopper(SentimentBase):
    prompt = SHOPPER_PROMPT
