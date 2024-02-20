import discord
from discord.ext import commands
import csv
import os

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.slash_command(guild_ids=[GUILD_ID], description="Inspect server users")
async def inspect(ctx, arg: str):
    print(f"Received command: /inspect {arg} from {ctx.author}")  # Print when a command is received

    if arg == "users":
        print("Gathering user information...")  # Indicate the start of user info gathering
        headers = ["Username", "ID", "Nickname", "Profile Picture URL", "Roles"]
        csv_file_name = "user_info.csv"

        with open(csv_file_name, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(headers)

            for guild in bot.guilds:
                print(f"Processing guild: {guild.name}")  # Print the guild being processed
                for member in guild.members:
                    username = f'{member.name}#{member.discriminator}'
                    user_id = member.id
                    nickname = member.nick or 'None'
                    avatar_url = str(member.avatar.url) if member.avatar else 'No avatar'
                    role_names = [role.name for role in member.roles if role.name != "@everyone"]
                    roles = ', '.join(role_names) if role_names else 'No roles'
                    writer.writerow([username, user_id, nickname, avatar_url, roles])

        print("User information gathered. Sending file...")  # Indicate the file is being sent
        await ctx.respond("Here's the user info:")
        await ctx.send(file=discord.File(csv_file_name))
        print("File sent successfully.")  # Confirm the file has been sent

        os.remove(csv_file_name)
        print(f"Temporary file {csv_file_name} deleted.")  # Confirm the temporary file deletion


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} and ready to serve!')  # Confirm the bot is logged in and ready


bot.run('DISCORD_BOT_TOKEN')
