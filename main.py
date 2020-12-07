## Env ##
import PointsSystem
import discord
from discord.ext import commands
import asyncio
from helpers import *
import os
from dotenv import load_dotenv
os.system("")
load_dotenv()


## Client Setup ##
client = commands.Bot(command_prefix=os.getenv("PREFIX"), intents=discord.Intents.all())
client.channels = [int(channel) for channel in os.getenv("CHANNEL_IDS").split(",")]
client.color = os.getenv("EMBED_COLOR")
client.color = int(client.color) if client.color.isdigit() else client.color
client.onlyimages = True if os.getenv("ONLY_IMAGES").lower() == "true" else False

## Points System Setup ##
PointsSystem = PointsSystem.Points(client)

@client.event
async def on_ready():
    print(f"{OKCYAN}Ready as {str(client.user)}")
    print(f"Invite link:{ENDC} {UNDERLINE}https://discord.com/oauth2/authorize?client_id={client.user.id}&scope=bot&permissions=8{ENDC}\n")
    PointsSystem.cleanse_data()
    print(f"{OKGREEN}Cleansed all data!{ENDC}")
    

@client.event
async def on_member_remove(member):
    PointsSystem.remove_user(member)
    client.log_channel = client.get_channel(os.getenv("LOGS_CHANNEL_ID"))

async def log(message:str):
    await client.log_channel.send(embed=discord.Embed(color=client.color, description=f"{pencil} {message}"))

@client.event
async def on_message(message):
    if message.guild is not None:
        if message.channel.id in client.channels:
            
            if client.onlyimages:
                if message.attachments:
                    amount = len(message.attachments)
                    PointsSystem.add_points(message.author, amount=amount)
                    await log(f"Added {amount} point{'s' if amount != 1 else ''} to {message.author.mention}")
            else:
                PointsSystem.add_points(message.author)
                await log(f"Added 1 point to {message.author.mention}")
                
    await client.process_commands(message)


@client.command()
@commands.check(is_admin)
async def add(ctx, member: discord.Member, amount: int = 1):
    PointsSystem.add_points(member, amount)
    await ctx.send(content=f"{check_mark} Successfully added {amount} points!", embed=PointsSystem.member_embed(member))


@client.command()
@commands.check(is_admin)
async def remove(ctx, member: discord.Member, amount: int = 1):
    PointsSystem.remove_points(member, amount)
    await ctx.send(content=f"{check_mark} Successfully removed {amount} points!", embed=PointsSystem.member_embed(member))


@client.command()
@commands.check(is_admin)
async def reset(ctx):
    await ctx.send(embed=discord.Embed(color=client.color, description=":warning: Are you sure you want to reset all information related to your server?"))

    try:
        answer = await client.wait_for('message', check=lambda m: m.channel == ctx.channel and m.author.id == ctx.author.id, timeout=10)
    except asyncio.TimeoutError:
        return await ctx.send(embed=discord.Embed(color=client.color, description=f"{x_mark} You took too long to answer!!"))

    if answer.content.lower() == "yes":
        PointsSystem.reset_guild(ctx.guild)
        return await ctx.send(embed=discord.Embed(color=client.color, description=f"{check_mark} Successfully reset your server!"))

    return await ctx.send(embed=discord.Embed(color=client.color, description=f"{check_mark} Successfully cancelled the reset!"))


@client.command()
@commands.check(is_admin)
async def raffle(ctx):
    winner = PointsSystem.random_raffle(ctx.guild)
    if winner is None:
        return await ctx.send(embed=discord.Embed(color=client.color, description=f"{x_mark} Couldn't determine a winner!"))

    return await ctx.send(embed=discord.Embed(color=client.color, description=f"{popper} {winner.mention} is the winner!"))


@client.command()
async def points(ctx, member: discord.Member = None):
    return await ctx.send(embed=PointsSystem.member_embed(member if member else ctx.author))


@client.command()
async def leaderboard(ctx):
    return await ctx.send(embed=PointsSystem.get_leaderboard(ctx.guild))


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return

    elif isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(
            description=f"{x_mark} Slow down {ctx.author.name}! Please try again in {error.retry_after:.2f}s", color=client.color)
        await ctx.send(embed=embed)

    elif isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
        await ctx.send_help(ctx.command)

    elif isinstance(error, commands.CheckFailure):
        embed = discord.Embed(
            color=13840175, description=f"{x_mark} Not allowed!")
        await ctx.send(embed=embed)

    else:
        raise error


client.run(os.getenv("TOKEN"))
