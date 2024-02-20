import csv
import os
import gspread
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents)

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']


def login_to_google():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return gspread.authorize(creds)


@bot.slash_command(description="Sends user data in a CSV file")
async def inspector_csv(ctx):
    await ctx.defer()
    await generate_and_send_csv(ctx)


async def generate_and_send_csv(ctx):
    headers = ["Username", "ID", "Nickname", "Profile Picture URL", "Roles"]
    csv_file_name = "user_info.csv"
    with open(csv_file_name, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(headers)
        for member in ctx.guild.members:
            writer.writerow(await get_member_data(member))
    await ctx.respond("Here's the user info:", file=discord.File(csv_file_name))
    os.remove(csv_file_name)


@bot.slash_command(description="Sends user data to a Google Sheet")
async def inspector_gsheet(ctx):
    await ctx.defer()
    await update_google_sheets(ctx)


async def update_google_sheets(ctx):
    gc = login_to_google()
    sheet_id = 'YOUR_SHEET_ID'
    sheet = gc.open_by_key(sheet_id).sheet1

    headers = ["Username", "ID", "Nickname", "Profile Picture URL", "Roles"]
    sheet.update('A1:E1', [headers])  # Update the first row with headers if necessary

    all_member_data = []
    batch = []
    batch_size = 100
    row_index = 2

    for member in ctx.guild.members:
        username = f'{member.name}#{member.discriminator}'
        user_id = member.id
        nickname = member.nick or 'None'
        avatar_url = member.avatar.url if member.avatar else 'No avatar'
        roles = ', '.join([role.name for role in member.roles if role.name != "@everyone"])
        batch.append([username, str(user_id), nickname,
                      f'=IMAGE("{avatar_url}")' if avatar_url != 'No avatar' else 'No avatar', roles])

        if len(batch) == batch_size:
            all_member_data.append({
                'range': f'A{row_index}:E{row_index + batch_size - 1}',
                'values': batch
            })
            row_index += batch_size
            batch = []

    if batch:  # Add any remaining members in the last batch
        all_member_data.append({
            'range': f'A{row_index}:E{row_index + len(batch) - 1}',
            'values': batch
        })

    for data in all_member_data:  # Update the sheet in batches
        sheet.batch_update([data], value_input_option='USER_ENTERED')

    await ctx.respond("User information updated to Google Sheets.")


async def get_member_data(member):
    username = f'{member.name}#{member.discriminator}'
    user_id = member.id
    nickname = member.nick or 'None'
    avatar_url = str(member.avatar.url) if member.avatar else 'No avatar'
    role_names = [role.name for role in member.roles if role.name != "@everyone"]
    roles = ', '.join(role_names) if role_names else 'No roles'  # Updated line
    return [username, str(user_id), nickname, avatar_url, roles]


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} and ready to serve!')

bot.run('DISCORD_BOT_TOKEN')
