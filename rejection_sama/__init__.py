import discord
from discord.ext import commands
import os
import pandas as pd

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# global variables
rejections_file = None
col_names = ['Guild','Goal','Rejections','Celebrations','Reset']
default_goal = 25

# record a rejection, and celebrate if you've hit your goal
@bot.command(name="damage")
async def damage(context, num: int):
    celebrate = False
    rejections_df, guild_id, goal, rejections, celebrations, reset = get_guild_info(context) 
    for r in range(num):
        rejections += 1
        if (rejections-reset) % goal == 0:
            celebrate = True
    rejections_df.loc[rejections_df['Guild'] == guild_id, 'Rejections'] = rejections
    rejections_df.to_csv(rejections_file, index=False)
    if celebrate == True:
        await context.reply(f"You are at {rejections} rejections, and that means: congratulations, you've reached another {goal} rejections!  Rejection-sama demands that you go celebrate!")
    else:
        await context.reply(f"Rejection-sama thanks you for the rejections!  You're at {rejections} rejections.")

# remove rejections if you accidentally on purpose add too many 
@bot.command(name="oops")
async def oops(context, num: int):
    rejections_df, guild_id, goal, rejections, celebrations, reset = get_guild_info(context)
    rejections -= num
    if rejections < 0:
        rejections = 0
        await context.reply(f"Rejection-sama cannot give you negative rejections, much as Rejection-sama would like... you are now at 0 rejections.")
    else:
        await context.reply(f"Rejection-sama has removed {num} rejections!  You are now at {rejections} rejections.")
    rejections_df.loc[rejections_df['Guild'] == guild_id, 'Rejections'] = rejections
    rejections_df.to_csv(rejections_file, index=False)

# print the current number of rejections and the number of rejections left to the goal
@bot.command(name="progress")
async def progress(context):
    rejections_df, guild_id, goal, rejections = get_guild_info(context)
    to_go = goal - (rejections-reset) % goal
    await context.reply(f"You are at {rejections} rejections.  {to_go} rejections left to your next goal!")

# set goal number of rejections 
# if the new goal means a celebration has been reached, a celebration will be prompted, but only one
# TODO: Make sure this behaves the way you think it should!
@bot.command(name="goal")
async def goal(context, num: int):
    rejections_df, guild_id, goal, rejections, celebrations, reset = get_guild_info(context)
    if int((rejections-reset)/goal) < int((rejections-reset)/num):
        await context.reply(f"By resetting your goal to {num}, you have reached another celebration!  You may go celebrate if you wish!")
        await context.reply(f"Your goal is now to reach another {num} rejections, you have {goal} rejections left to your next goal!")
        reset = rejections
    to_go = num - (rejections-reset) % num
    await context.reply(f"Your goal is now to reach another {num} rejections, you have {to_go} rejections left to your next goal!")
    rejections_df.loc[rejections_df['Guild'] == guild_id, 'Goal'] = num
    rejections_df.to_csv(rejections_file, index=False)    

@bot.event
async def on_ready():
    print(f'Rejection-sama has been summoned! Target rejections set to {default_goal}, to set to another value, use goal command.')
        
def get_guild_info(context):
    guild_id = context.message.guild.id
    rejections_df = pd.read_csv(rejections_file)
    if guild_id not in rejections_df['Guild'].values:
        guild_to_append = pd.DataFrame({col_names[0]:[guild_id],col_names[1]:[default_goal],col_names[2]:[0]})
        if rejections_df.empty:
            rejections_df = guild_to_append
        else:
            rejections_df = pd.concat([rejections_df,guild_to_append],names=col_names) 
        rejections_df.to_csv(rejections_file, index=False)
    guild_loc = rejections_df['Guild'] == guild_id 
    rejections = rejections_df.loc[guild_loc, 'Rejections'].item()
    goal = rejections_df.loc[guild_loc, 'Goal'].item()
    celebrations = rejections_df.loc[guild_loc, 'Celebrations'].item()
    resets = rejections_df.loc[guild_loc, 'Resets'].item() 
    return(rejections_df, guild_id, goal, rejections, celebrations, resets)

def main():
    with open(os.environ.get('DISCORD_TOKEN_FILE', './rejection_token_file.txt'), 'r') as f:
        TOKEN = f.read()
    global rejections_file
    rejections_file = os.environ.get('REJECTIONS_FILE', './rejections.csv')
    bot.run(TOKEN)

if __name__ == '__main__':
    main()
