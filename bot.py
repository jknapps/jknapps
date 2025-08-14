import os
import requests
import discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")
RANDOM_ORG_KEY = os.getenv("RANDOM_ORG_API_KEY")
API_URL = "https://api.random.org/json-rpc/2/invoke"

bot = commands.Bot(command_prefix="!")

def roll_random_org(n: int):
    """Fetch n random integers (1–10) from random.org."""
    payload = {
        "jsonrpc": "2.0",
        "method": "generateIntegers",
        "params": {
            "apiKey": RANDOM_ORG_KEY,
            "n": n,
            "min": 1,
            "max": 10,
            "replacement": True,
        },
        "id": 42,
    }
    resp = requests.post(API_URL, json=payload)
    resp.raise_for_status()
    return resp.json()["result"]["random"]["data"]

def roll_cod_dice(pool: int, again: int = 10):
    """Roll a Chronicles of Darkness dice pool with variable -again rules."""
    results = []
    to_roll = pool
    while to_roll > 0:
        dice = roll_random_org(to_roll)
        results.extend(dice)
        to_roll = sum(1 for r in dice if r >= again)
    successes = sum(1 for r in results if r >= 8)
    return results, successes

def format_results(results, again):
    formatted = []
    for r in results:
        if r >= again:
            formatted.append(f"**`{r}`**")
        elif r >= 8:
            formatted.append(f"`{r}`")
        else:
            formatted.append(str(r))
    return " ".join(formatted)

@bot.command(name="roll")
async def roll(ctx, pool: int, again: int = 10):
    if pool <= 0:
        await ctx.send("Dice pool must be positive.")
        return
    if again not in (8, 9, 10):
        await ctx.send("Again value must be 8, 9, or 10.")
        return
    results, successes = roll_cod_dice(pool, again)
    formatted = format_results(results, again)
    await ctx.send(
        f"Rolled {pool} dice ({again}-again): {formatted} \u27a1 {successes} success(es)"
    )

bot.run(TOKEN)
