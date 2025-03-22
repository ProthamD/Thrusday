from discord.ext import commands
from datetime import timedelta
from utils.api_helpers import openrouter_chat_completion
from config import BAD_WORDS

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def timeout(self, ctx, member: discord.Member):
        """Timeout a member for 1 hour."""
        await member.timeout(timedelta(hours=1), reason=f"Requested by {ctx.author}")
        await ctx.send(f"I've timed out {member.mention} for 1 hour.")

    @commands.Cog.listener()
    async def on_message(self, message):
        """Check for bad words in messages."""
        if message.author == self.bot.user:
            return

        msg = message.content.lower()
        if any(word in msg for word in BAD_WORDS):
            await message.delete()
            try:
                await message.author.timeout(timedelta(hours=1), reason="Used inappropriate language")
                await message.channel.send(f"{message.author.mention} has been timed out for 1 hour for using inappropriate language.")
            except discord.Forbidden:
                await message.channel.send(f"I don't have permission to timeout {message.author.mention}.")
            except discord.HTTPException as e:
                await message.channel.send(f"An error occurred while trying to timeout {message.author.mention}: {e}")

async def setup(bot):
    await bot.add_cog(Moderation(bot))