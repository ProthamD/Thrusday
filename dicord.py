import discord
from discord.ext import commands
import os
from datetime import timedelta
from dotenv import load_dotenv
import requests
import json
from collections import defaultdict
import base64
from io import BytesIO
import asyncio  # Import asyncio for sleep functionality

# Load the .env file
load_dotenv()

# Stable Horde API details
STABLE_HORDE_API_KEY = os.getenv('STABLE_HORDE_API_KEY')  # Your Stable Horde API key
STABLE_HORDE_API_URL = "https://stablehorde.net/api/v2/generate/async"

# Bad words list (fallback in case AI fails)
bad_words = ['furry', 'fuck', 'bitch', 'kys', 'kill yourself', 'killyour self', 'kill your self']

intents = discord.Intents.default()
intents.message_content = True

# Initialize the bot with intents
bot = commands.Bot(command_prefix="!", intents=intents)

# Store conversation history (temporary)
conversation_history = defaultdict(list)  # Key: user ID, Value: list of messages
MAX_HISTORY_LENGTH = 10  # Maximum number of messages to store in history

# Store permanent user data
USER_DATA_FILE = "user_data.json"

# Load user data from file (if it exists)
if os.path.exists(USER_DATA_FILE):
    with open(USER_DATA_FILE, "r") as f:
        user_data = json.load(f)
else:
    user_data = {}

def save_user_data():
    """Save user data to a file."""
    with open(USER_DATA_FILE, "w") as f:
        json.dump(user_data, f, indent=4)

@bot.event
async def on_ready():
    print('We have been successfully logged in as {0.user}'.format(bot))

@bot.event
async def on_message(message):
    msg = message.content
    if message.author == bot.user:
        return

    user_id = str(message.author.id)

    # Initialize user data if not already present
    if user_id not in user_data:
        user_data[user_id] = {
            "name": message.author.name,  # Store the user's name
            "preferences": {}
        }
        save_user_data()

    # Add the user's message to the conversation history
    conversation_history[user_id].append({"role": "user", "content": msg})

    if len(conversation_history[user_id]) > MAX_HISTORY_LENGTH:
        conversation_history[user_id].pop(0)

    # Check if the bot is mentioned in the message
    if bot.user in message.mentions:
        try:
            # Prepare the conversation history for the AI
            messages_for_ai = conversation_history[user_id].copy()
            messages_for_ai.insert(0, {
                "role": "system",
                "content": f"You are Thursday, a mature and independent woman. You are talking to {user_data[user_id]['name']}. Always address them by their name and maintain the context of the conversation."
            })

            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://your-site-url.com",  # Optional
                    "X-Title": "Your Site Name",  # Optional
                },
                data=json.dumps({
                    "model": "deepseek/deepseek-r1:free",  # Use the desired model
                    "messages": messages_for_ai,
                })
            )

            if response.status_code == 200:
                msg_response = response.json()["choices"][0]["message"]["content"].strip()
                conversation_history[user_id].append({"role": "assistant", "content": msg_response})
                await message.channel.send(f"{msg_response}")
            else:
                # Handle API errors
                await message.channel.send("Sorry, I couldn't generate a response. Please try again later.")
                print(f"API Error: {response.status_code} - {response.text}")

        except Exception as e:
            await message.channel.send("An error occurred while generating a response. Please try again later.")
            print(f"Error: {e}")

    if msg.startswith('hello'):
        await message.channel.send(f'Look who got spawned {message.author.mention}, Hello')

    # Check for bad words using AI
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://your-site-url.com",  # Optional / NA
                "X-Title": "Your Site Name",  # Optional / NA
            },
            data=json.dumps({
                "model": "deepseek/deepseek-r1:free",  # Use the desired model
                "messages": [
                    {
                        "role": "user",
                        "content": f"Check the following message for slangs or swearing words. Reply with only 'yes' or 'no'. Only reply 'yes' if the message contains explicit slurs, hate speech, or severe profanity. Ignore mild or casual language like 'idiot', 'okey', or similar words. Message: \"{msg}\""
                    }
                ],
            })
        )

        # Parse the AI response
        if response.status_code == 200:
            ai_response = response.json()["choices"][0]["message"]["content"].strip().lower()
            if ai_response == "yes":
                # Delete the message
                await message.delete()
                # Timeout the user for 1 hour
                try:
                    await message.author.timeout(timedelta(hours=1), reason="Used inappropriate language")
                    await message.channel.send(f"{message.author.mention} has been timed out for 1 hour for using inappropriate language.")
                except discord.Forbidden:
                    await message.channel.send(f"I don't have permission to timeout {message.author.mention}.")
                except discord.HTTPException as e:
                    await message.channel.send(f"An error occurred while trying to timeout {message.author.mention}: {e}")

        else:
            if any(words in msg.lower() for words in bad_words):
                await message.delete()
                try:
                    await message.author.timeout(timedelta(hours=1), reason="Used inappropriate language")
                    await message.channel.send(f"{message.author.mention} has been timed out for 1 hour for using inappropriate language.")
                except discord.Forbidden:
                    await message.channel.send(f"I don't have permission to timeout {message.author.mention}.")
                except discord.HTTPException as e:
                    await message.channel.send(f"An error occurred while trying to timeout {message.author.mention}: {e}")
    except Exception as e:
        print(f"An error occurred while checking for bad words: {e}")

    # Process commands
    await bot.process_commands(message)

@bot.command()
@commands.has_permissions(moderate_members=True)
async def timeout(ctx: commands.Context, member: discord.Member):
    """
    Timeout a member for 1 hour.
    Usage: !timeout @user
    """
    await member.timeout(timedelta(hours=1), reason=f"Requested by {ctx.author}")
    await ctx.send(f"I've timed out {member.mention} for 1 hour.")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def create_channels(ctx, num_channels: int):
    """
    Create channels with AI-generated names using OpenRouter.ai.
    Usage: !create_channels <number_of_channels>
    """
    if num_channels <= 0:
        await ctx.send("Please provide a valid number of channels to create.") 
        return

    # Generate channel names using OpenRouter.ai
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://your-site-url.com",  # Optional / NA
                "X-Title": "Your Site Name",  # Optional / NA
            },
            data=json.dumps({
                "model": "deepseek/deepseek-r1:free", 
                "messages": [
                    {
                        "role": "user",
                        "content": f"Generate {num_channels} creative and unique Discord channel names. Separate each name with a newline."
                    }
                ],
            })
        )

        # Parse the response
        if response.status_code == 200:
            channel_names = response.json()["choices"][0]["message"]["content"].strip().split('\n')
            channel_names = [name.strip() for name in channel_names if name.strip()]
        else:
            await ctx.send(f"Failed to generate channel names: {response.text}")
            return
    except Exception as e:
        await ctx.send(f"An error occurred while generating channel names: {e}")
        return

    # Create channels in the server
    guild = ctx.guild
    created_channels = []
    for name in channel_names[:num_channels]:  # *Ensure we don't exceed the requested number
        try:
            new_channel = await guild.create_text_channel(name)
            created_channels.append(new_channel.mention)
        except discord.Forbidden:
            await ctx.send("I don't have permission to create channels.")
            return
        except discord.HTTPException as e:
            await ctx.send(f"Failed to create a channel: {e}")
            return

    # Send a confirmation message
    await ctx.send(f"Successfully created {len(created_channels)} channels: {', '.join(created_channels)}")

@bot.command()
async def img(ctx: commands.Context, *, prompt: str):
    """
    Generate an image using the Stable Horde API.
    Usage: !img <prompt>
    """
    await ctx.send(f"Generating an image for: `{prompt}`. Please wait...")

    try:
        # Prepare the request payload for Stable Horde
        payload = {
            "prompt": prompt,
            "params": {
                "n": 1,  # Number of images to generate
                "width": 512,  # Image width
                "height": 512,  # Image height
                "steps": 20,  # Number of diffusion steps
                "cfg_scale": 7.5,  # Guidance scale
                "sampler_name": "k_euler",  # Sampler
                "seed": "-1",  # Random seed (must be a string)
            },
            "nsfw": False,  # Disable NSFW content
            "trusted_workers": False,  # Use trusted workers
            "models": ["stable_diffusion"],  # Model to use
            "censor_nsfw": False,  # Do not censor NSFW content
            "r2": True,  # Use Cloudflare R2 for image delivery
            "shared": False,  # Do not share the image with LAION
        }

        # Send the request to Stable Horde
        headers = {
            "apikey": STABLE_HORDE_API_KEY,
            "Content-Type": "application/json",
        }
        response = requests.post(STABLE_HORDE_API_URL, json=payload, headers=headers)

        # Check if the request was accepted
        if response.status_code == 202:
            # Get the request ID
            request_id = response.json().get("id")
            if not request_id:
                await ctx.send("Failed to start image generation. Please try again.")
                return

            # Wait for the image to be generated
            await ctx.send("Image generation started. Please wait...")
            image_url = f"https://stablehorde.net/api/v2/generate/status/{request_id}"
            while True:
                status_response = requests.get(image_url, headers=headers)
                if status_response.status_code == 200:
                    status_data = status_response.json()
                    if status_data.get("done"):
                        # Check if the image data is valid
                        if "generations" not in status_data or not status_data["generations"]:
                            await ctx.send("Failed to generate an image. Please try again.")
                            return

                        # Get the generated image
                        image_data = status_data["generations"][0].get("img")
                        if not image_data:
                            await ctx.send("Failed to retrieve image data. Please try again.")
                            return

                        # Decode the Base64 image data
                        try:
                            image_bytes = base64.b64decode(image_data)
                            if len(image_bytes) < 100:  # Check if the image data is too small
                                await ctx.send("Failed to generate a valid image. Please try again.")
                                return

                            # Send the image to the Discord channel
                            image_file = BytesIO(image_bytes)
                            await ctx.send(file=discord.File(image_file, filename="generated_image.png"))
                            break
                        except Exception as e:
                            await ctx.send(f"Failed to decode the image: {e}")
                            return
                    else:
                        # Wait a few seconds before checking again
                        await asyncio.sleep(5)  # Use asyncio.sleep for async waiting
                else:
                    await ctx.send("Failed to check image generation status. Please try again.")
                    break
        else:
            await ctx.send("Failed to start image generation. Please try again.")
            print(f"Stable Horde API Error: {response.status_code} - {response.text}")

    except Exception as e:
        await ctx.send(f"An error occurred while generating the image: {e}")
        print(f"Error: {e}")
# Run the bot
bot.run(os.getenv('TOKEN'))