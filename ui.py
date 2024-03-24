import discord
from decouple import config
from discord.ext import commands, tasks
import json
import time
import os
import backend

# Initialize bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

# Load user data from a JSON file
backend.load_users()

# Listen to user messages
@bot.event
async def on_message(message):
    # Ignore messages from bots
    if message.author.bot:
        return

    user_id = str(message.author.id)

    # Load users data
    bot.users_data = backend.load_users()

    # If user not in data, initialize cooldowns
    if user_id not in bot.users_data:
        bot.users_data[user_id] = backend.initialize_cooldowns(user_id)
        backend.save_users(bot.users_data)
    print(message)
    await bot.process_commands(message)

# Task to tick down cooldowns every hour
@tasks.loop(hours=1)
async def tick_cooldowns():
    bot.users_data = backend.load_users()  # Reload users data
    for user_id, data in bot.users_data.items():
        data['mission_cooldown'] -= 1  # 1 hour in seconds
        data['reminder_cooldown'] -= 3600  # 1 hour in seconds
    backend.save_users(bot.users_data)

# Check for cooldowns and offer missions
@bot.event
async def on_message(message):
    # Ignore messages from bots
    if message.author.bot:
        return

    user_id = str(message.author.id)

    # Load users data
    bot.users_data = backend.load_users()

    # If user cooldowns are over, offer a mission
    if user_id in bot.users_data and bot.users_data[user_id]['mission_cooldown'] <= 0:
        # Send the user a message offering a mission
        user = bot.get_user(int(user_id))
        if user:
            await user.send("Hey, it's time for a new mission! Are you ready?")

        # Reset mission cooldown
        bot.users_data[user_id]['mission_cooldown'] = 24 * 3600  # Reset to 24 hours
        backend.save_users(bot.users_data)

# Run bot
bot.run(config("BOT_TOKEN"))