import re

from bs4 import BeautifulSoup


def text_from_html(body):
    soup = BeautifulSoup(body, "html.parser")
    return re.sub(r"\s+", " ", soup.get_text())


def truncate_content_for_gpt(
    page_content,
    gpt_input_word_limit,
):
    return " ".join(page_content.split()[:gpt_input_word_limit])
