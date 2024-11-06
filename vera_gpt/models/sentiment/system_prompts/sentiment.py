SENTIMENT_PROMPT = """
Here is some user comments on influence social media posts about certain products.
Can you summarize the sentiment as positive or negatve?
You must return your response as a JSON object.
The key is called "summary" and the value is a int of either 1 indicating positive or 0 indicating negative.
"""

PURCHASE_PROMPT = """
Here is some user comments on influence social media posts about certain products.
Can you summarize whether the comment indicates purchase consideration?
For Purchase Consideration, it would be things like "I can't wait to try this!" "Adding to cart now" "I need to have this" etc.
You must return your response as a JSON object where the key is called "summary" and the value is a int of either 1 indicating purchase or 0 indicating no purchase.
"""

SHOPPER_PROMPT = """
Here is some user comments on influence social media posts about certain products.
Can you summarize whether the comment is from current shopper?
For Current Shopper, it's typically comments like "I love Ghirardelli Chocolate" or "I grew up eating this!" "This is my go-to" etc.
You must return your response as a JSON object where the key is called "summary" and the value is a int of either 1 indicating current shopper or 0 indicating non-current shopper.
"""
