import discord
from discord.ext import commands
from googletrans import Translator
from discord.commands import Option
import os
from dotenv import load_dotenv
from languages import languages


load_dotenv()
translator = Translator()
intents = discord.Intents.all()
bot = commands.Bot(command_prefix= ">", help_command = None,auto_sync_commands= True, intents = intents)
TOKEN = os.getenv("TOKEN")

async def get_key(val, dictionary:dict):
	for key, value in dictionary.items():
			if val == value:
				return key
	return "invalid key"

#-----------------------------------------------------------------------------------------------------------------------
@bot.message_command(name = "Translate")
async def translate_command(self, ctx, message:discord.Message):
	output = translator.translate(f"{str(message.content)}", dest = "en")
	data = output.text
	await ctx.respond(f"{data}", ephemeral = True)

@bot.slash_command(name = "translate",description = "Translate your english message to the preferred languages")
async def translate_command(
	ctx,
	lang : Option(str, "The language you wish to translate the message in"),
	text : Option(str, "The text you wish to translate.")
):
	language = await get_key(lang, languages)
	if language == "invalid key":
		return await ctx.respond("This language is invalid. Please refer the documentation to find the valid languages.", ephemeral = True)
	output = translator.translate(text, dest = language)
	data = output.text
	await ctx.respond(f"{data}", ephemeral = True)	

bot.run(TOKEN)
