import discord
import gspread
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

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


gc = login_to_google()
sheet_id = 'YOUR_SHEET_ID'
sheet = gc.open_by_key(sheet_id).sheet1

# Define column headers
headers = ["Username", "ID", "Nickname", "Profile Picture URL", "Roles"]
sheet.update('A1:E1', [headers])  # Update the first row with headers if necessary


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    for guild in client.guilds:
        print(f'--- Guild: {guild.name} ---')
        all_member_data = []
        batch = []
        batch_size = 100
        row_index = 2

        async for member in guild.fetch_members(limit=None):
            username = f'{member.name}#{member.discriminator}'
            user_id = member.id
            nickname = member.nick or 'None'
            avatar_url = member.avatar.url if member.avatar else 'No avatar'
            role_names = [role.name for role in member.roles if role.name != "@everyone"]
            roles = ', '.join(role_names) if role_names else 'No roles'
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
            sheet.batch_update([{
                'range': data['range'],
                'values': data['values']
            }], value_input_option='USER_ENTERED')

client.run('DISCORD_PRIVATE_TOKEN')
