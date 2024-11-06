CATEGORY_PROMPT = """
This is a summary of a web page.
You are an expert on IAB standards.
Based on the summary, assign the {N_CATEGORIES} most applicable IAB subcategories for this content.
Return only a valid JSON object containing a key called "categories" where the value is a list of IAB category IDs.
Use only categories found in the following list:
{IAB_CATEGORIES}
"""
