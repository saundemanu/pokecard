import os

import discord
from discord.ext import commands
from scraper import Scraper

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True

# Use commands.Bot instead of discord.Client for command handling
bot = commands.Bot(command_prefix="!", intents=intents)

scraper = Scraper()


@bot.command()
async def card(ctx, *, card_name: str):
    # Fetch card data (limit 5 results per search)
    cards = scraper.scrape_pokellector(card_name)

    if isinstance(cards, str):
        await ctx.reply(cards)
        return

    current_page = 0
    embed = await create_embed(cards[current_page])
    message = await ctx.reply(embed=embed)

    if len(cards) > 1:
        # Add reactions for pagination
        await message.add_reaction("⬅️")
        await message.add_reaction("➡️")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["⬅️", "➡️"]

    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=30.0, check=check)

            # Handle page changes
            if str(reaction.emoji) == "➡️":
                current_page += 1
                if current_page >= len(cards):  # Loop back to the first page
                    current_page = 0
            elif str(reaction.emoji) == "⬅️":
                current_page -= 1
                if current_page < 0:  # Loop to the last page
                    current_page = len(cards) - 1

            # Update the embed with the new card's details
            embed = await create_embed(cards[current_page])
            await message.edit(embed=embed)

            # Remove the user's reaction to prevent multiple responses
            await message.remove_reaction(reaction, user)

        except Exception as e:
            # Timeout or other errors will break the loop
            break


async def create_embed(card):
    # Create embed without async since embed creation doesn't need async
    embed = discord.Embed(title=card.name, description=f"{card}")
    embed.set_image(url=card.image)
    return embed


async def fetch_card_data(card_name):
    # Fetch the card data for the search term
    card_data = scraper.scrape_pokellector(card_name)
    if not card_data:
        return None
    return card_data


@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # This block allows handling commands directly in the message
    if message.content.startswith("!card"):
        card_name = message.content[6:]  # Everything after !card
        await message.channel.send(f"Searching for {card_name}...")

        card_data = await fetch_card_data(card_name)
        if card_data:
            await card(message, card_name=card_name)
        else:
            await message.channel.send("No card found!")


bot.run(DISCORD_TOKEN)
