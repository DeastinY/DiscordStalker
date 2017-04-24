import json
import asyncio
import discord
import logging

logging.basicConfig(level=logging.INFO)

client = discord.Client()
server = 'overwatsch'
channel = 'general'
games = ['overwatch']
audience = []  # The ids of the channels to post to


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    print('Possible Channels')
    for c in client.get_all_channels():
        print("{} \t {}".format(c.server, c.name))
        server_name = str(c.server).lower()
        channel_name = str(c).lower()
        if server in server_name and channel in channel_name and not c.type is discord.ChannelType.voice:
            audience.append(c)
            #await client.send_message(c, 'Bot online')
    print('Registered for Channels : {}'.format(["{}:{}".format(c.name, c.server) for c in audience]))


@client.event
async def on_message(message):
    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')


@client.event
async def on_member_update(before, after):
    if before.game != after.game:
        if any([g in str(after.game).lower() for g in games]):
            message = "{} started playing {} !".format(after.nick, after.game)
            for a in audience:
                await client.send_message(a, message)

credentials = {'email': "", "password": ""}
with open('credentials.json') as fin:
    credentials = json.load(fin)

if "token" in credentials:
    client.run(credentials["token"])
else:
    client.run(credentials["email"], credentials["password"])