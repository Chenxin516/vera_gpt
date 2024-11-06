import types
import asyncio

from abc import ABC
from abc import abstractmethod


class ModelBase(ABC):
    def __init__(
        self,
        async_call: bool = True,
        completions_options: dict = {},
    ) -> None:
        self.async_call = async_call
        self.completions_options = completions_options

    def predict(
        self,
        content: str,
    ):
        result = self.async_predict(
            content=content,
        )
        if self.async_call:
            return result
        return asyncio.run(result)

    def predict_batch(
        self,
        contents: iter,
        update_interval: int,
    ):
        result = self.async_predict_batch(
            contents=contents,
            update_interval=update_interval,
        )
        if self.async_call:
            return result
        return asyncio.run(result)

    @abstractmethod
    async def async_predict(
        self,
        content: str,
    ) -> types.CoroutineType:
        raise NotImplementedError("'async_predict' not implemented")

    @abstractmethod
    async def async_predict_batch(
        self,
        contents: iter,
        update_interval: int,
    ) -> types.CoroutineType:
        raise NotImplementedError("'async_predict_batch' not implemented")
