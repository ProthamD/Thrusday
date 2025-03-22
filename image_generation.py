from discord.ext import commands
from utils.api_helpers import stable_horde_image_generation
import asyncio
import base64
from io import BytesIO

class ImageGeneration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def img(self, ctx, *, prompt: str):
        """Generate an image using Stable Horde API."""
        await ctx.send(f"Generating an image for: `{prompt}`. Please wait...")
        request_id = stable_horde_image_generation(prompt)
        if not request_id:
            await ctx.send("Failed to start image generation. Please try again.")
            return

        await ctx.send("Image generation started. Please wait...")
        image_url = f"https://stablehorde.net/api/v2/generate/status/{request_id}"
        while True:
            status_response = requests.get(image_url, headers=headers)
            if status_response.status_code == 200:
                status_data = status_response.json()
                if status_data.get("done"):
                    image_data = status_data["generations"][0].get("img")
                    if image_data:
                        image_bytes = base64.b64decode(image_data)
                        image_file = BytesIO(image_bytes)
                        await ctx.send(file=discord.File(image_file, filename="generated_image.png"))
                        break
            await asyncio.sleep(5)

async def setup(bot):
    await bot.add_cog(ImageGeneration(bot))