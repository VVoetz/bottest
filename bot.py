import discord
from discord.ext import commands
import asyncio
import aex
from datetime import datetime
import schedule

def run_discord_bot():
    TOKEN = 'ODg3NDc2OTkyMzI3NDM0Mjcw.GNSMP7.OhI7jW25-m3CwFY-9SYrsjpnKeK3U0psGlQI-I'
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)
    channel_id = "887476371264249868"

    async def ava_change():
        test = False
        while not test:
            test = aex.get_chart()
        with open("image.png", 'rb') as f:
            chart = f.read()
        await client.user.edit(avatar=chart)
    
    def print_summary():

        # TODO:
        # check weekdag/weekend

        info = aex.get_winners_losers()
        message = f"Goedemorgen, het is weer 10 uur dus de daily summary:"
        winners = list()
        for i in info[:3]:
            winners.append(f"{i[0]} {i[1]} {i[4]}")
        for i in winners:
            print(i)

        client = discord.Client(intents=intents)
        async def on_ready():
            print('test')
            channel = client.get_channel(channel_id)
            if channel:
                await channel.send(message)
            else:
                print('error')
            client.close()

    schedule.every().day.at("18:03:30").do(print_summary)

    @client.event
    async def on_ready():
        await client.change_presence(status=discord.Status.online, activity=discord.Game(f"gettin' ready"))
        print(f"{client.user} is now running!'")

        # intents.message_content = True
        # bot = commands.Bot(command_prefix='!', intents=intents)
        # channel = bot.get_channel("934004565102198858")
        # print(channel)

        i = 0
        while True:
            # print(i)
            schedule.run_pending()
            # get market information
            koers = aex.get_koers()
            lasttradetime = int(koers[5][1:3]) * 60 +  int(koers[5][4:6])
            time = datetime.now().hour * 60 + datetime.now().minute

            if time - lasttradetime > 5 or time - lasttradetime < 0:
                distatus = discord.Status.idle
            else:
                distatus = discord.Status.online
                # if i % 40 == 0:
                #     await ava_change()
                pass
                
            if koers[3][0] == '+':
                await client.change_presence(status=distatus, activity=discord.Game(f"€{koers[2]}🟢 {koers[4]} {koers[5]}"))
            else:
                await client.change_presence(status=distatus, activity=discord.Game(f"€{koers[2]}🔴 {koers[4]} {koers[5]}"))
                
            await asyncio.sleep(10)
            i += 1
            

    client.run(TOKEN)
    