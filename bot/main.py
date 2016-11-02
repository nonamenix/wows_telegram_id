import os

from aiotg import Bot
import logging

# Logging
logging.basicConfig(
    level=getattr(logging, os.environ.get('BOT_LOGGING_LEVEL', 'DEBUG')),
    format='%(asctime)s | %(name)s | %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
logger.addHandler(ch)

bot = Bot(
    api_token=os.environ["BOT_TOKEN"],
    botan_token=os.environ["BOTAN_TOKEN"]
)


@bot.command("/start")
async def start(chat, message):
    await chat.send_text('Добро пожаловать на супертест, Капитан!')
    await info(chat, message)


@bot.command("/restart")
async def restart(chat, message):
    await chat.send_text(
        'С возвращением на супертест, Капитан!',
        disable_web_page_preview=True
    )


@bot.command("/stop")
async def stop(chat, message):
    await chat.send_text(
        'Всего хорошего, Капитан!',
        disable_web_page_preview=True
    )


@bot.command('/info')
@bot.command('кто я')
async def info(chat, message):
    userinfo = {
        'userid': chat.message['from']['id'],
        'username': chat.message['from'].get('username', 'unknown'),
        'first_name': '',
        'last_name': '',
        'chatid': chat.id
    }
    try:
        userinfo['first_name'] = chat.message['from'].get('first_name', '')
        userinfo['last_name'] = chat.message['from'].get('last_name', '')
    except KeyError:
        pass
    try:
        text = """
Капитан, я узнал что тебя зовут: {username}

И еще немного подробностей о тебе:
Username: {username}
Name: {first_name} {last_name}
User id: {userid}
Chat id: {chatid}
""".format(**userinfo)
    except:
        text = 'Что-то пошло не так!'

    await chat.send_text(text)


@bot.default
async def default(chat, match):
    await chat.send_text(
        'Да, капитан!? Я пока умею только /info'
    )


if __name__ == "__main__":
    logger.info("Running...")
    bot.run()
