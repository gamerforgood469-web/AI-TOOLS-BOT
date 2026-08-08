import asyncio

from telegram import Bot

from config import (
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHANNEL
)

from database import initialize

from content_engine import create_post


async def main():

    print("🤖 Starting automatic publisher...")

    # Create the database if it doesn't exist
    initialize()

    # Generate a completely fresh post
    result = await create_post()

    title = result["title"]
    post = result["post"]

    message = (
        f"🔥 {title}\n\n"
        f"{post}\n\n"
        f"🤖 AI Tools & Tricks"
    )

    bot = Bot(
        token=TELEGRAM_BOT_TOKEN
    )

    # Publish directly to the channel
    await bot.send_message(
        chat_id=TELEGRAM_CHANNEL,
        text=message,
        disable_web_page_preview=True
    )

    print("✅ Post published successfully!")


if __name__ == "__main__":
    asyncio.run(main())
