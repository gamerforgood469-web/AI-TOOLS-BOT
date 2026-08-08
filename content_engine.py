import json

from ai_engine import generate
from database import get_history, save_post


async def create_post():

    history = get_history(100)

    previous_posts = json.dumps(
        history,
        ensure_ascii=False
    )

    prompt = f"""
Create ONE completely fresh Telegram post for an
AI Tools & Tricks channel.

Previous posts are listed below:

{previous_posts}

IMPORTANT:
- Do NOT repeat a previous topic.
- Do NOT repeat a previous tool.
- Do NOT repeat the same trick.
- Do NOT simply rewrite an old post.
- Make the new post genuinely useful.
- Prefer lesser-known but useful AI tools and techniques.
- Never invent facts, links, features, or prices.

Possible categories:
AI Tools
AI Prompts
AI Workflows
AI Productivity
AI Study
AI Coding
AI Creativity

Choose whether this post should be:

IMAGE_AND_TEXT

or

TEXT_ONLY

Use IMAGE_AND_TEXT only when a visual genuinely improves
the post.

Return EXACTLY this format:

TITLE:
[short attractive title]

TOPIC:
[unique topic]

FORMAT:
[IMAGE_AND_TEXT or TEXT_ONLY]

POST:
[complete Telegram post]

IMAGE_PROMPT:
[image-generation prompt if IMAGE_AND_TEXT;
otherwise write NONE]
"""

    result = await generate(prompt)

    title = extract_section(result, "TITLE", "TOPIC")
    topic = extract_section(result, "TOPIC", "FORMAT")
    post_format = extract_section(result, "FORMAT", "POST")
    post = extract_section(result, "POST", "IMAGE_PROMPT")
    image_prompt = extract_section(
        result,
        "IMAGE_PROMPT",
        None
    )

    if not title or not post:
        raise ValueError(
            "AI returned an invalid post format."
        )

    save_post(
        title=title,
        topic=topic,
        content=post,
        post_format=post_format
    )

    return {
        "title": title,
        "topic": topic,
        "format": post_format,
        "post": post,
        "image_prompt": image_prompt
    }


def extract_section(text, start, end):

    marker = start + ":"

    if marker not in text:
        return ""

    value = text.split(
        marker,
        1
    )[1]

    if end:

        end_marker = "\n" + end + ":"

        if end_marker in value:

            value = value.split(
                end_marker,
                1
            )[0]

    return value.strip()
