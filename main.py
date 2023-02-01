import os
from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext import Filters
from telegram import ReplyKeyboardMarkup

import random
import json


SECRET = os.environ['token']


with open('ru_serb.json') as f:
    dictionary = json.load(f)


def generate_question():
    answers = random.sample(list(dictionary.keys()), 4)
    question = random.choice(answers)

    correct_answer = dictionary[question]
    translated_answers = [dictionary[answer] for answer in answers]
    return translated_answers, question, correct_answer


def start(update, context):
    chat_id = update.effective_chat.id
    answers, question, correct_answer = generate_question()

    keyboard = ReplyKeyboardMarkup.from_column(answers,
                                               one_time_keyboard=True,
                                               resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat_id,
        text=f"What is the Serbian equivalent for '{question}'?",
        reply_markup=keyboard)

    context.user_data['correct'] = correct_answer


def answer_question(update, context):
    chat_id = update.effective_chat.id
    text = update.effective_message.text

    correct_answer = context.user_data['correct']

    if correct_answer == text:
        context.bot.send_message(chat_id=chat_id, text="\U00002705 Correct!")
    else:
        context.bot.send_message(
            chat_id=chat_id,
            text=f"\U0000274c Correct answer is' {correct_answer}'")

    start(update, context)


updater = Updater(SECRET)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.text, answer_question))

updater.start_polling()
