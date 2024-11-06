import json

from .. import ModelBase

from ... import GPT
from ... import GPTBatch
from ... import batch

from .system_prompts import SUMMARY_PROMPT
from .system_prompts import CATEGORY_PROMPT
from .system_prompts import IAB_CATEGORIES


class IAB(ModelBase):
    def __init__(
        self,
        len_summary=10,
        n_categories=5,
        async_call=True,
        completions_options={},
    ):
        super().__init__(
            async_call=async_call,
            completions_options=completions_options,
        )

        self.summary_prompt = SUMMARY_PROMPT.format(
            LEN_SUMMARY=len_summary,
        )
        self.category_prompt = CATEGORY_PROMPT.format(
            N_CATEGORIES=n_categories,
            IAB_CATEGORIES=IAB_CATEGORIES,
        )

        self.async_call = async_call
        self.completions_options = completions_options

    async def async_predict(self, content):
        summarize = GPT(
            system_prompt=self.summary_prompt,
            completions_options=self.completions_options,
        )(content)
        summary = json.loads(summarize).get("summary")

        categorize = GPT(
            system_prompt=self.category_prompt,
            completions_options=self.completions_options,
        )(summary)
        categories = json.loads(categorize).get("categories", [])

        category_names = list(
            map(
                lambda x: IAB_CATEGORIES.get(x, "INVALID_CATEGORY"), categories
            )
        )

        output = [
            categories,
            category_names,
            summary,
        ]
        return output

    async def async_predict_batch(
        self,
        contents,
        update_interval,
    ):
        print("STARTING SUMMARY BATCH")
        summary_job = GPTBatch(
            system_prompt=self.summary_prompt,
            completions_options=self.completions_options,
        )(contents)
        summary_response = batch.BatchResponse(summary_job)(
            update_interval=update_interval
        )
        batch_summaries = [x["summary"] for x in summary_response]

        print("STARTING CATEGORY BATCH")
        category_job = GPTBatch(
            system_prompt=self.category_prompt,
            completions_options=self.completions_options,
        )(batch_summaries)
        category_response = batch.BatchResponse(category_job)(
            update_interval=update_interval
        )
        batch_categories = [x["categories"] for x in category_response]

        batch_category_names = [
            list(
                map(
                    lambda x: IAB_CATEGORIES.get(x, "INVALID CATEGORY"),
                    categories,
                )
            )
            for categories in batch_categories
        ]

        batch_output = list(
            map(
                list,
                zip(
                    batch_categories,
                    batch_category_names,
                    batch_summaries,
                ),
            )
        )
        return batch_output
