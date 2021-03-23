import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()

import os
token = os.environ.get("TOKEN")

from datetime import datetime

bot = commands.Bot(command_prefix='.')


""" helper functions """

#print ready in terminal
@bot.event
async def on_ready():
    print ('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=discord.Game("Das einzig arbeitende Vorstandsmitglied."))

#prints bot ping
@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency*1000)} ms')
""" end helper functions """

""" start poll section"""
#list of letter emojis for polls
options =["🇦","🇧","🇨","🇩","🇪","🇫","🇬","🇭","🇮","🇯","🇰","🇱","🇲","🇳","🇴","🇵","🇶","🇷","🇸","🇹","🇺","🇻","🇼","🇽","🇾","🇿"]
#list of poll attributes for poll handling


#our very own poll bot
@bot.command()
async def poll(ctx, question, *answers):
    if len(answers) < 2:
        await ctx.send('Diese Poll hat nicht genug Antworten.')
    elif len(answers) > 26:
        await ctx.send('Es sind leider nur 26 Antwortmöglichkeiten erlaubt.')
    else:
        #creates embed for poll question and reactions
        embed = discord.Embed(title = "📊"+question, timestamp=datetime.utcnow())
        fields = [("Antworten", "\n".join([f"{options[idx]} {answer}" for idx, answer in enumerate(answers)]), False)]
        embed.set_footer(text='Abstimmung erstellt von {}'.format(ctx.author.display_name))

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        
        #adds emoji reactions for answers
        await ctx.send("Bitte gebt jetzt eure Stimmen ab.") # todo get bot to mention @here to alert everyone not idle
        msg = await ctx.send(embed=embed)

        for emoji in options[:len(answers)]:
            await msg.add_reaction(emoji)

"""" end poll section"""

""" general bot functionality and msg reactions """
#on_message functionality for specific messages
@bot.event
async def on_message(message):
    #checks for commands first before checking for specific message content
    await bot.process_commands(message)

    if message.author == bot.user:
        return

    if message.content.startswith('.Hallo'):
        await message.channel.send(f'Hallo, {message.author.mention}! ')
        return

""" end general functionality """

bot.run(token)