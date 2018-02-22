import aiohttp

import settings.config


# Post guild count to update count for either discordbots.org or bots.discord.pw
async def update_guild_count(bot, api_url, token):
    api_url += 'api/bots/' + str(bot.user.id) + '/stats'
    headers = {"Authorization": token}
    payload = {"server_count": len(bot.guilds)}

    async with aiohttp.ClientSession() as aio_client:
        if 'bots.discord.pw' in api_url:
            await aio_client.post(api_url, json=payload, headers=headers,
                                  timeout=10)

        else:
            await aio_client.post(api_url, data=payload, headers=headers,
                                  timeout=10)


# Get a list of user IDs who have upvoted FlandersBOT
async def get_upvoters():
    async with aiohttp.ClientSession() as aio_client:
        db_headers = {"Authorization": settings.config.DB_TOKEN}
        resp = await aio_client.get('https://discordbots.org/api/bots/2216096' +
                                    '83562135553/votes?onlyids=true',
                                    headers=db_headers)
        if resp.status == 200:
            upvoters = await resp.json()
            return upvoters

        else:
            return []
