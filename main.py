import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.command(name="damage")
async def damage(context, num: int):
    celebrate = False
    with open('rejections.txt', 'r') as f:
        rejections = int(f.readlines()[-1].strip('\n'))
    if num < 1000:
        for r in range(num):
            rejections += 1
            if rejections % 100 == 0:
                celebrate = True
        with open('rejections.txt', 'w+') as f:
            f.write(str(rejections) + '\n')
        if celebrate == True:
            await context.reply(f"You are at {rejections} rejections, and that means: congratulations, you've reached another 100 rejections!  Rejection-sama demands that you go celebrate!")
        else:
            await context.reply(f"Rejection-sama thanks you for the rejections!  You're at {rejections} rejections.")
    else:
        await context.reply("Rejection-sama knows you are lying and does not wish to be toyed with in this way >:(")

@bot.command(name="oops")
async def damage(context, num: int):
    with open('rejections.txt', 'r') as f:
        rejections = int(f.readlines()[-1].strip('\n'))
    rejections -= num
    with open('rejections.txt', 'w+') as f:
        f.write(str(rejections) + '\n')
    await context.reply(f"Rejection-sama has removed {num} rejections!  You are now at {rejections} rejections.")

@bot.event
async def on_ready():
    print(f'Rejection-sama has been summoned!')

with open('../rejection_token_file.txt', 'r') as f:
    TOKEN = f.read()
bot.run(TOKEN)

