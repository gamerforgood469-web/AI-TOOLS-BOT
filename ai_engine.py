from google import genai
from google.genai import types

from config import GEMINI_API_KEY, GEMINI_MODEL


client = genai.Client(
    api_key=GEMINI_API_KEY
)


SYSTEM_PROMPT = """
You create useful, original content for an AI Tools & Tricks
Telegram channel.

Topics can include:
- AI tools
- AI prompts
- AI workflows
- AI productivity
- AI study
- AI coding
- AI creativity

Every post must be genuinely useful and different from previous
posts.

Never invent facts, links, prices, or features.

Keep the content clear, attractive, and suitable for Telegram.

Return only the requested content.
"""


async def generate(prompt):

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            max_output_tokens=1500
        )
    )

    return response.text.strip()
