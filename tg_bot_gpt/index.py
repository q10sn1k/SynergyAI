import openai
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import logging
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

token = os.getenv('TELEGRAM_BOT_TOKEN')
openai.api_key = os.getenv("OPEN_AI_TOKEN_API")

bot = Bot(token)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

messages = {}
@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    try:
        username = message.from_user.username
    except AttributeError:
        await message.answer("Пожалуйста, поставьте себе ник в Телеграмм, чтобы вести диалог с ботом.")
        return
    messages[username] = []
    messages[username].append({"role": "system", "content": "Ты аналитик крипторынка (bitcoin), который имеет богатый опыт и знания в этой сфере."
                                                             "Твоя задача - разбираться в сложных вопросах крипторынка и предоставлять подробный анализ."
                                                             "Ты можешь давать советы о потенциальных инвестициях и текущих трендах рынка."
                                                             "Ты должен быть аккуратным в своих прогнозах, так как люди полагаются на твои советы."
                                                             "Делай первый шаг, задавай вопросы."})
    await message.answer(
        "Приветствую! Я бот, который использует API GPT-3.5-turbo (ChatGPT).\n Вот функции, которыми можно пользоваться:\n/help - показать доступные функции"
        "\n/newtopic - начать новый диалог\n/sp - установить новую роль."
        "\n"
        "\n"
        "Пример описания роли:"
        "\n"
        "/sp Ты аналитик крипторынка (bitcoin), который имеет богатый опыт и знания в этой сфере."
        "Твоя задача - разбираться в сложных вопросах крипторынка и предоставлять подробный анализ."
        "Ты можешь давать советы о потенциальных инвестициях и текущих трендах рынка."
        "Ты должен быть аккуратным в своих прогнозах, так как люди полагаются на твои советы.")


@dp.message_handler(commands=['sp'])
async def set_prompt_cmd(message: types.Message):
    username = message.from_user.username
    prompt = message.text.split(' ', 1)[1]
    messages[username] = []
    messages[username].append({"role": "system", "content": prompt})
    await message.answer(f"Системная роль - '{prompt}'.")

@dp.message_handler(commands=['newtopic'])
async def new_topic_cmd(message: types.Message):
    username = message.from_user.username
    messages[username] = []
    await message.answer("Новый диалог создан.")

@dp.message_handler(commands=['help'])
async def help_cmd(message: types.Message):
    help_text = "/help - показать доступные функции\n/newtopic - начать новый диалог\n/sp - установить новую роль."\
                "\n"\
                "\n"\
                "Пример описания роли:"\
                "\n"\
                "/sp Ты опытный финансовый юрист, специализирующийся в области корпоративного права, сделок и налогов."\
                "Тебе знакомы международные стандарты и законодательство разных стран."\
                "Твоя задача - предоставлять консультации по юридическим вопросам, связанным с финансами и инвестициями."\
                "Ты должен быть аккуратным в своих советах, так как люди полагаются на твои знания и опыт."
    await message.answer(help_text)

@dp.message_handler()
async def echo(message: types.Message):
    user_message = message.text
    username = message.from_user.username
    if username not in messages:
        messages[username] = []
        messages[username].append({"role": "system", "content": "Ты аналитик крипторынка (bitcoin), который имеет богатый опыт и знания в этой сфере."
                                                                "Твоя задача - разбираться в сложных вопросах крипторынка и предоставлять подробный анализ."
                                                                "Ты можешь давать советы о потенциальных инвестициях и текущих трендах рынка."
                                                                "Ты должен быть аккуратным в своих прогнозах, так как люди полагаются на твои советы."
                                                                "Делай первый шаг, задавай вопросы."})

    messages[username].append({"role": "user", "content": user_message})


    logging.info(f'{username}: {user_message}')
    logging.info('')
    logging.info('')


    should_respond = not message.reply_to_message or message.reply_to_message.from_user.id == bot.id

    if should_respond:
        try:
            text = messages[username]
            chatgpt_response = open_ai_request(text, username)
            messages[username].append({"role": "assistant", "content": chatgpt_response['content']})

            logging.info(f'ChatGPT response: {chatgpt_response["content"]}')
            logging.info('')
            logging.info('')

            if len(messages[username]) > 13:
                messages[username].pop(1)
                messages[username].pop(1)

            await message.reply(chatgpt_response['content'], parse_mode='Markdown')
        except:

            messages[username].pop(1)
            messages[username].pop(1)
            messages[username].pop(1)
            messages[username].pop(1)

            text = messages[username]
            chatgpt_response = open_ai_request(text, username)
            messages[username].append({"role": "assistant", "content": chatgpt_response['content']})

            logging.info(f'ChatGPT response: {chatgpt_response["content"]}')
            logging.info('')
            logging.info('')

            await message.reply(chatgpt_response['content'], parse_mode='Markdown')



def open_ai_request(text, username):
    completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=text,
                #max_tokens=3000,
                #temperature=0.9,
                #frequency_penalty=0.3,
                #presence_penalty=0.3,
                user=username
                )
    chatgpt_response = completion.choices[0]['message']
    return chatgpt_response


executor.start_polling(dp, skip_updates=True)
