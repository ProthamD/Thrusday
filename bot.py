import discord
from discord.ext import commands
from config import OPENROUTER_API_KEY, MAX_HISTORY_LENGTH
from utils.data_helpers import load_user_data, save_user_data
from cogs.moderation import Moderation
from cogs.image_generation import ImageGeneration

# Initialize bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Load user data
user_data = load_user_data()

# Load cogs
async def setup_cogs():
    await bot.add_cog(Moderation(bot))
    await bot.add_cog(ImageGeneration(bot))

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await setup_cogs()

# Run the bot
bot.run(os.getenv('TOKEN'))