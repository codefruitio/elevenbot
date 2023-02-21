import discord
from discord import app_commands
from dotenv import load_dotenv
import requests
import os
import random
import json as j

class aclient(discord.Client):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.activity = discord.Activity(type=discord.ActivityType.watching, name="you")

client = aclient()
        
@client.event
async def on_ready():
    await client.tree.sync()


@client.tree.command(name="synthesize", description="Generate audio.")
async def synthesize(interaction: discord.Interaction, *, text: str, voice: str):
    global eleven_api
    await interaction.response.send_message("Synthesizing...", ephemeral=True, delete_after=3)
    site = "https://api.elevenlabs.io/v1/text-to-speech/" + voice
    headers = {
        'accept': 'audio/mpeg',
        'xi-api-key': f"{eleven_api}",
        'Content-Type': 'application/json'
        }
    if len(text) > 1000:
        await interaction.channel.send("WARNING: Text is over 1000 characters! Please try a sentence less than 1000 characters.")
        return
    else:
        r = requests.post(site, json={"text": f"{text}"}, headers=headers)
        if r.status_code == 400:
            await interaction.channel.send("ERROR: Entered voice ID does not exist! Did you enter the ID correctly?")
            return
        else:
            audiofilename = "synth-" + str(random.randint(1, 372855)) + ".mp3"
            with open(audiofilename, 'wb') as out:
                out.write(r.content)
            await interaction.channel.send(f"Done ✅! Sending audio file...\nYou have used {len(text)} characters.", delete_after=3)
            f = discord.File(audiofilename)
            await interaction.channel.send(file=f)
            os.remove(audiofilename)
            return
        

@client.tree.command(name="voices", description="List all available voices.")
async def voices(interaction: discord.Interaction):
    global eleven_api
    await interaction.response.send_message("Fetching voices...", ephemeral=True, delete_after=3)
    site = "https://api.elevenlabs.io/v1/voices"
    headers = {
        'accept': 'application/json',
        'xi-api-key': f"{eleven_api}",
        'Content-Type': 'application/json'
        }
    r = requests.get(site, headers=headers)
    fileobj = j.dumps(r.json(), indent=4)
    with open("voices.json", 'w') as outfile:
        outfile.write(fileobj)
    f = discord.File("voices.json")
    await interaction.channel.send(file=f)
    os.remove("voices.json")

if __name__ == '__main__':
    load_dotenv()
    discord_token = os.getenv("DISCORD_BOT_TOKEN")
    eleven_api = os.getenv("ELEVENLABS_API")
    client.run(discord_token)