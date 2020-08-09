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
    # {
    #     "name": "**Get Specific Help on using a Command in this List:**",
    #     "value": "`command: !help !<command name>`"
    # },
    {
        "name": "**Clear Messages (EXECUTIVE ONLY):**",
        "value": "Deletes the number of specified messages\n`command: r.clear <num>`"
    },
    {
        "name": "**Check Server Latency:**",
        "value": "Returns latency in milliseconds\n`command: r.ping`"
    },  # 4
    {
        "name": "**Create a Custom Poll for People to React To:**",
        "value": "Creates a poll which other members can react to\n`command: r.createpoll <question>`"
    },
    {
        "name": "**Get Random Quote**",
        "value": "Returns a random anime quote:\n`command: r.quote <name of character, show, or leave it empty to get random quote>`"
    },  # 12
    {
        "name": "**Get Random Joke**",
        "value": "Returns a random joke:\n`command: r.joke`"
    },  # 13
    {
        "name": "**Random Insult**",
        "value": "Insult someone with this command:\n`command: r.insult <name of person you wanna insult>`"
    },  # 14
    {
        "name": "**Get Random Advice**",
        "value": "Returns some random advice:\n`command: r.advice`"
    },
    {
        "name": "**Search any Anime**",
        "value": "Returns a list of search results based on your search query:\n`command: r.anime <anime name/anime id>`"
    },  # 13
    {
        "name": "**Search any Manga**",
        "value": "Returns a list of search results based on your search query:\n`command: r.manga <anime name/anime id>`"
    },  # 13
    {
        "name": "**Find Currently Airing Shows**",
        "value": "Returns a list of shows which are currently airing on a specific day of the week:\n`command: r.airing <mon/tue/wed/etc.>`"
    }
]
bot_prefix = "r."
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
@commands.has_role("Executive")
async def clear(ctx, amount=1):
    await ctx.channel.purge(limit=amount + 1)


@client.command()
async def createpoll(ctx, *, text):
    await ctx.channel.purge(limit=1)
    embed = discord.Embed(title="Question", colour=yellow)
    embed.add_field(name="⠀", value=text, inline=False)
    message = await ctx.send(embed=embed)
    await message.add_reaction("👍")
    await message.add_reaction("👎")


@client.command(pass_context=True)  # You need to allow to pass the Context object to the command function
async def joke(cntx, *args):
    r = requests.get("https://sv443.net/jokeapi/v2/joke/Any?blacklistFlags=racist,sexist")
    _joke = ""
    if r.json().get("type") == "twopart":
        _joke = "\n{}\n\n\n\n{}\n\n- ({})".format(r.json().get("setup"), r.json().get("delivery"), r.json().get("category"))
    else:
        _joke = "\n{}\n\n- ({})".format(r.json().get("joke"), r.json().get("category"))
    # print(_joke)
    embed = discord.Embed(title="", colour=yellow)
    embed.add_field(name="⠀", value=f"```{_joke}```", inline=False)
    embed.set_footer(text=f"Emsee (latency: {round(client.latency * 1000)}ms)")  # if you like to
    await cntx.send(embed=embed)


@client.command(pass_context=True)  # You need to allow to pass the Context object to the command function
async def insult(cntx, *args):
    r = requests.get("https://evilinsult.com/generate_insult.php?lang=en&type=json")
    # print(r.json()["insult"])
    recievee = " ".join(args)
    message = r.json()["insult"]
    embed = discord.Embed(title="", colour=yellow)
    embed.add_field(name=f"{recievee}", value=f"```{message}```", inline=False)
    embed.set_footer(text=f"Emsee (latency: {round(client.latency * 1000)}ms)")  # if you like to
    await cntx.send(embed=embed)


@client.command(pass_context=True)  # You need to allow to pass the Context object to the command function
async def advice(cntx, *args):
    r = requests.get("https://api.adviceslip.com/advice")
    message = r.json()["slip"]["advice"]
    embed = discord.Embed(title="", colour=yellow)
    embed.add_field(name="⠀", value=f"```{message}```", inline=False)
    embed.set_footer(text=f"Emsee (latency: {round(client.latency * 1000)}ms)")  # if you like to
    await cntx.send(embed=embed)


@client.command(pass_context=True)  # You need to allow to pass the Context object to the command function
async def quote(cntx, *args):
    query = " ".join(args)
    if len(query) != 0:
        try:
            r = requests.get("https://anime-chan.herokuapp.com/api/quotes?anime={}".format(query))
            rand = random.randint(0, len(r.json()))
            quote = r.json()[rand]
            # print(quote)

            embed = discord.Embed(title="Anime: " + quote.get("anime"), colour=yellow)
            embed.add_field(name="Character: " + quote.get("character"), value="```{}```".format(quote["quote"]), inline=False)
            embed.set_footer(text=f"Emsee (latency: {round(client.latency * 1000)}ms)")  # if you like to
            await cntx.send(embed=embed)
        except:
            try:
                r = requests.get("https://anime-chan.herokuapp.com/api/quotes?char={}".format(query))
                rand = random.randint(0, len(r.json()))
                quote = r.json()[rand]
                print(quote)
                embed = discord.Embed(title="Anime: " + quote.get("anime"), colour=yellow)
                embed.add_field(name="Character: " + quote.get("character"), value="```{}```".format(quote["quote"]), inline=False)
                embed.set_footer(text=f"Emsee (latency: {round(client.latency * 1000)}ms)")  # if you like to
                await cntx.send(embed=embed)
                # print(quote)
            except:
                print("sorry that anime or character was not found")
                embed = discord.Embed(title="", colour=yellow)
                embed.add_field(name="Error", value="```Sorry that anime or character was not found. Or, it doesn't exist in the database.```", inline=False)
                embed.set_footer(text=f"Emsee (latency: {round(client.latency * 1000)}ms)")  # if you like to
                await cntx.send(embed=embed)
    else:
        r = requests.get("https://anime-chan.herokuapp.com/api/quotes/random")
        # rand = random.randint(0, len(r.json()))
        quote = r.json()[0]
        # print(quote)
        # print(type(quote))
        embed = discord.Embed(title="Anime: " + quote["anime"], colour=yellow)
        embed.add_field(name="Character: " + quote.get("character"), value="```{}```".format(quote["quote"]), inline=False)
        embed.set_footer(text=f"Emsee (latency: {round(client.latency * 1000)}ms)")  # if you like to
        await cntx.send(embed=embed)
        # print(quote)


@client.command(pass_context=True)  # You need to allow to pass the Context object to the command function
async def anime(cntx, *args):
    try:
        # print("apple pie")
        ID = int("".join(args))

        r = requests.get("https://api.jikan.moe/v3/anime/{}".format(ID))

        type_ = r.json()["type"]
        title = "{} [{}]\n({})".format(r.json()["title_english"], type_, r.json()["title_japanese"])
        url = r.json()["url"]
        poster = r.json()["image_url"]
        synopsis = r.json()["synopsis"]

        score = r.json()["score"]
        rank = r.json()["rank"]
        rating = r.json()["rating"]

        episodes = r.json()["episodes"]

        genres = ", ".join([genre["name"] for genre in r.json()["genres"]])
        duration = r.json()["duration"]
        premiered = r.json()["premiered"]
        trailer = r.json()["trailer_url"]

        embed = discord.Embed(title=f"{title}", description="*{}*\n[Click here to visit MAL for more info on this anime]({})".format(synopsis, url), colour=yellow)
        # print(poster)
        embed.set_image(url=poster)

        embed.add_field(name=f"Genres", value=f"`{genres}`", inline=False)
        embed.add_field(name=f"Rating", value=f"`{rating}`", inline=False)

        embed.add_field(name=f"Score:", value=f"`{score}/10`", inline=True)
        embed.add_field(name=f"Rank", value=f"`#{rank} in the Top  Anime List`", inline=True)

        embed.add_field(name=f"Episodes", value=f"`{episodes} episodes with each being {duration} in duration`", inline=False)
        embed.add_field(name=f"Premiered", value=f"`{premiered}`", inline=False)
        embed.add_field(name=f"Trailer", value=f"[Click here to watch the trailer for this anime]({trailer})", inline=False)
        embed.set_footer(text=f"Emsee (latency: {round(client.latency * 1000)}ms)")  # if you like to
        await cntx.send(embed=embed)

    except Exception as ex:
        # print(ex)
        r = requests.get("https://api.jikan.moe/v3/search/anime?q={}".format(" ".join(args)))

        asearch_results = r.json()["results"][0:10]
        anime_search_titles = [e["title"] for e in asearch_results]
        anime_search_ids = [e["mal_id"] for e in asearch_results]
        aresults = list(zip(anime_search_titles, anime_search_ids))

        embed = discord.Embed(title="Multiple Search Results: ", description="Please pick an anime and type its respective command...", colour=yellow)

        for name in aresults:
            embed.add_field(name=f"{name[0]}", value=f"`r.anime {name[1]}`", inline=False)

        embed.set_footer(text=f"Emsee (latency: {round(client.latency * 1000)}ms)")  # if you like to
        await cntx.send(embed=embed)


@client.command(pass_context=True)
async def airing(cntx, *args):
    day = process.extractOne("".join(args), ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"])[0]
    print(day)
    r = requests.get("https://api.jikan.moe/v3/schedule/{}".format(day))

    titles = [e["title"] for e in r.json()[day]]
    ids = [e["mal_id"] for e in r.json()[day]]
    results = list(zip(titles, ids))

    embed = discord.Embed(title="Current Airing List for {}".format(day.capitalize()), description="Please pick an anime and type its respective command...", colour=yellow)

    for name in results:
        embed.add_field(name=f"{name[0]}", value=f"`r.anime {name[1]}`", inline=False)

    embed.set_footer(text=f"Emsee (latency: {round(client.latency * 1000)}ms)")  # if you like to
    await cntx.send(embed=embed)


@client.command(pass_context=True)  # You need to allow to pass the Context object to the command function
async def manga(cntx, *args):
    try:
        # print("apple pie")
        ID = int("".join(args))

        r = requests.get("https://api.jikan.moe/v3/manga/{}".format(ID))

        type_ = r.json()["type"]
        title = "{} [{}]\n({})".format(r.json()["title_english"], type_, r.json()["title_japanese"])
        url = r.json()["url"]
        poster = r.json()["image_url"]
        synopsis = r.json()["synopsis"]

        score = r.json()["score"]
        rank = r.json()["rank"]
        popularity = r.json()["popularity"]

        # episodes = r.json()["episodes"]

        genres = ", ".join([genre["name"] for genre in r.json()["genres"]])
        authors = ", ".join([author["name"] for author in r.json()["authors"]])
        # duration = r.json()["duration"]
        # premiered = r.json()["premiered"]
        # trailer = r.json()["trailer_url"]

        embed = discord.Embed(title=f"{title}", description="*{}*\n[Click here to visit MAL for more info on this manga]({})".format(synopsis, url), colour=yellow)
        # print(poster)
        embed.set_image(url=poster)

        embed.add_field(name=f"Genres", value=f"`{genres}`", inline=False)
        embed.add_field(name=f"Popularity", value=f"`{popularity}`", inline=False)

        embed.add_field(name=f"Score:", value=f"`{score}/10`", inline=True)
        embed.add_field(name=f"Rank", value=f"`#{rank} in the Top  Manga List`", inline=True)

        # embed.add_field(name=f"Episodes", value=f"`{episodes} episodes with each being {duration} in duration`", inline=False)
        # embed.add_field(name=f"Premiered", value=f"`{premiered}`", inline=False)
        # embed.add_field(name=f"Trailer", value=f"[Click here to watch the trailer for this anime]({trailer})", inline=False)
        embed.set_footer(text=f"Emsee (latency: {round(client.latency * 1000)}ms)")  # if you like to
        await cntx.send(embed=embed)

    except Exception as ex:
        print(ex)
        r = requests.get("https://api.jikan.moe/v3/search/manga?q={}".format(" ".join(args)))

        msearch_results = r.json()["results"][0:10]
        manga_search_titles = [e["title"] for e in msearch_results]
        manga_search_ids = [e["mal_id"] for e in msearch_results]
        mresults = list(zip(manga_search_titles, manga_search_ids))

        embed = discord.Embed(title="Multiple Search Results: ", description="Please pick a manga and type its respective command...", colour=yellow)

        for name in mresults:
            embed.add_field(name=f"{name[0]}", value=f"`r.manga {name[1]}`", inline=False)

        embed.set_footer(text=f"Emsee (latency: {round(client.latency * 1000)}ms)")  # if you like to
        await cntx.send(embed=embed)


with open('env.json') as f:
    data = json.load(f)

client.run(data['DISCORD_TOKEN'])
