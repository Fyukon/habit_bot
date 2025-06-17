from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()


async def send_reminder(bot, user_id):
    await bot.send_message(user_id, "Не забудь выполнить свои привычки сегодня!")
