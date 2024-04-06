from datetime import datetime
from typing import Final
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler , Application , filters , MessageHandler , JobQueue
import requests
import logging
TOKEN = "Your_Bot_Token"

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Hi {update.effective_user.first_name}!"
    )
async def echo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=update.message.text
    )

async def fact_handler (update : Update , context : ContextTypes.DEFAULT_TYPE):
    data = requests.get("https://uselessfacts.jsph.pl/api/v2/facts/random")
    fact = data.json()["text"]
    await context.bot.send_message(chat_id=update.effective_chat.id , text=fact)


async def facts_handler (update : Update , context : ContextTypes.DEFAULT_TYPE) :
    try :
        a = int(context.args[0])
        if a < 5 :
            await context.bot.send_message(chat_id=update.effective_chat.id , text="please enter a number greater than 5")
            return
        # job_facts_handler is a call back fucntion and run repeatly
        # here you can set name of your jobs
        job_name = str(update.effective_user.id)
        job_exists = delete_facts_job_if_exists(job_name, context)
        if job_exists:
            context.job_queue.run_repeating(
                job_facts_handler,
                interval=a,
                chat_id=update.effective_chat.id,
                name=job_name)

            await context.bot.send_message(chat_id=update.effective_chat.id,
                                text="your Previous job were delete and you will receive a fact every {} seconds".format(
                                    a))
        else :
            context.job_queue.run_repeating(job_facts_handler , interval=a , chat_id=update.effective_chat.id , name = job_name)
            await context.bot.send_message(chat_id=update.effective_chat.id , text="you will receive a fact every {} seconds".format(a))
    except (IndexError , ValueError) :
            await context.bot.send_message(chat_id=update.effective_chat.id , text="please enter a number greater than 5 not anything else")

            

# job only get on input in self def 
# this is job from job_queue
async def job_facts_handler(context : ContextTypes.DEFAULT_TYPE) :
    job = context.job
    data = requests.get("https://uselessfacts.jsph.pl/api/v2/facts/random")
    fact = data.json()["text"]
    await context.bot.sendMessage(chat_id=job.chat_id , text=fact)


# set a remove job 
async def unset_facts_job_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jobs = context.job_queue.get_jobs_by_name(str(update.effective_user.id))
    for job in jobs:
        job.schedule_removal()
    await context.bot.send_message(chat_id=update.effective_chat.id, text="you will no more receive facts")

def delete_facts_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE):
    jobs = context.job_queue.get_jobs_by_name(name)
    if not jobs:
        return False
    for job in jobs:
        job.schedule_removal()
    return True

if __name__ == "__main__":
    # Create the Application and pass it your bot's token
    application = Application.builder().token(TOKEN).build()
    # Command Handler
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("fact", fact_handler))
    application.add_handler(CommandHandler("facts", facts_handler))
    application.add_handler(CommandHandler("unset", unset_facts_job_handler))
    # Message Handler
    application.add_handler(MessageHandler(filters.TEXT, echo_handler))
    # Run the Bot
    application.run_polling()