import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.command(name="damage")
async def damage(context, num: int):
    celebrate = False
    with open('rejections.txt', 'r') as f:
        rejections = int(f.readlines()[-1].strip('\n'))
    if num < 100:
        for r in range(num):
            rejections += 1
            if rejections % 25 == 0:
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
    if rejections < 0:
        rejections = 0
        await context.reply(f"Rejection-sama cannot give you negative rejections, much as Rejection-sama would like... you are now at 0 rejections.")
    else:
        await context.reply(f"Rejection-sama has removed {num} rejections!  You are now at {rejections} rejections.")
    with open('rejections.txt', 'w+') as f:
        f.write(str(rejections) + '\n')

@bot.event
async def on_ready():
    print(f'Rejection-sama has been summoned!')

def main():
    with open('./rejection_token_file.txt', 'r') as f:
        TOKEN = f.read()
    bot.run(TOKEN)

if __name__ == '__main__':
    main()
