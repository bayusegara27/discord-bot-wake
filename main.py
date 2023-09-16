import discord
import asyncio
import requests
import os
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv('BOT_TOKEN')
prefix = os.getenv('PREFIX')
ip_address = os.getenv('IP_ADDRESS')
powersw_key = os.getenv('POWERSW_KEY')

intents = discord.Intents.all()
intents.messages = True

bot = commands.Bot(command_prefix=prefix, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands(s)")
    except Exception as e:
        print(e)

@bot.tree.command(name='pcon')
async def turn_on_computer(interaction: discord.Interaction):
    # change to your display name discord
    if interaction.user.name == "nakumi":
        response = requests.get(f'{ip_address}/short?key={powersw_key}')
        if response.status_code == 200:
            await interaction.response.send_message("Komputer telah dinyalakan!")
        else:
            await interaction.response.send_message("Gagal menghidupkan komputer.", ephemeral=True)
    else:
        await interaction.response.send_message("Maaf, Anda tidak memiliki izin untuk menggunakan perintah ini.", ephemeral=True)

@bot.tree.command(name='pcoff')
async def turn_off_computer(interaction: discord.Interaction):
    # change to your display name discord
    if interaction.user.name == "nakumi":  
        await interaction.response.send_message('Mengirim permintaan untuk mematikan komputer...')
        async def send_request():
            response = requests.get(f'{ip_address}/long?key={powersw_key}')
            if response.status_code == 200:
                await interaction.followup.send('Komputer telah dimatikan!')
            else:
                await interaction.followup.send('Gagal mematikan komputer.', ephemeral=True)
        await asyncio.gather(send_request())
    else:
        await interaction.response.send_message("Maaf, Anda tidak memiliki izin untuk menggunakan perintah ini.", ephemeral=True)

@bot.tree.command(name='pcstatus')
async def check_computer_status(interaction: discord.Interaction):
    response = requests.get(f'{ip_address}/statuspc?key={powersw_key}')
    if response.status_code == 200:
        status = response.text
        await interaction.response.send_message(f'Status {status}')
    else:
        await interaction.response.send_message('Gagal memeriksa status komputer.')

bot.run(bot_token)
