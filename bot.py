import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import time
import requests
import json
from pprint import pprint
import requests
from bs4 import BeautifulSoup as bs
import random
from fuzzywuzzy import process

help_list = [
    {
        "name": "**Clear Messages (EXECUTIVE ONLY):**",
        "value": "Deletes the number of specified messages\n`command: r.clear <num>`"
    },
    {
        "name": "**Check Server Latency:**",
        "value": "Returns latency in milliseconds\n`command: r.ping`"
    }
]

bot_prefix = "thread."
client = commands.Bot(command_prefix=bot_prefix)
yellow = discord.Color(15314177)

client.remove_command("help")


@client.event
async def on_ready():
    print("Ready when you are!")
    print("I am running on " + client.user.name)
    print("With the iD: " + str(client.user.id))
    await client.change_presence(activity=discord.Game("Steins Gate VN"))


@client.command(pass_context=True)  # You need to allow to pass the Context object to the command function
async def help(cntx, *args):
    embed = discord.Embed(title="Welcome to the Command Menu!",
                          description="*Note: Arguments in <this format> or (format) do not require the '<', '>' or '(', ')' characters*",
                          colour=yellow)

    for e in help_list:
        embed.add_field(name=e["name"], value="{}".format(e["value"]), inline=False)

    embed.set_footer(text=f"Emsee (latency: {round(client.latency * 1000)}ms)")  # if you like to
    await cntx.send(embed=embed)


@client.command()
async def ping(ctx):
    await ctx.send(f"Latency: {round(client.latency * 1000)}ms")


@client.command(aliases=['snap'])
# @commands.has_role("Executive")
async def clear(ctx, amount=1):
    await ctx.channel.purge(limit=amount + 1)


text = []
pinned = []


@client.command(aliases=['add'])
async def start(cntx, *args):
    if len(text) < 1:
        text.append("""**{}, entry {}**\n```{}```""".format(cntx.message.author.name, 0, " ".join(args)))
        message = await cntx.send(text[0])
        await message.pin()
        pinned.append(message)
    else:
        await pinned[-1].unpin()
        text.append("""**{}, entry {}**\n```{}```""".format(cntx.message.author.name, len(text), " ".join(args)))
        message = await cntx.send(text[0])

        for i, e in enumerate(text):
            if i == 0:
                pass
            else:
                await cntx.send(e)

        await message.pin()


@client.command()
async def edit(cntx, *args):
    " ".join(args)
    num = int(args[0])
    text[num] = """**{}, entry {}**\n```{}```""".format(cntx.message.author.name, len(text), " ".join(args))

    await pinned[-1].unpin()
    # text.append("""**{}, entry {}**\n```{}```""".format(cntx.message.author.name, len(text), " ".join(args)))
    message = await cntx.send(text[0])

    for i, e in enumerate(text):
        if i == 0:
            pass
        else:
            await cntx.send(e)

    await message.pin()

client.run("")
