import aiohttp
import aiofiles
import ssl
import certifi
import os
from fastapi import FastAPI, HTTPException
from typing import Dict

# Import the necessary functions from quake_log_utils
from quake_log_utils import parse_log, get_total_kills, get_player_kills, get_kills_by_means, get_used_means_by_player

app = FastAPI()

# URL to the log file
GIST_URL = "https://gist.githubusercontent.com/cloudwalk-tests/be1b636e58abff14088c8b5309f575d8/raw/df6ef4a9c0b326ce3760233ef24ae8bfa8e33940/qgames.log"
FILE_NAME = "qgames.log"

# Cache to store parsed log data
cache = {}


async def download_log_file(url: str, file_path: str):
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=ssl_context) as response:
            if response.status != 200:
                raise HTTPException(status_code=404, detail="Log file could not be downloaded")
            async with aiofiles.open(file_path, 'wb') as file:
                await file.write(await response.read())


async def get_or_parse_log(file_path: str):
    if file_path in cache:
        return cache[file_path]

    games = await parse_log(file_path)
    cache[file_path] = games  # Store parsed data in cache
    return games


@app.get("/download_and_parse")
async def download_and_parse():
    try:
        # Download the log file
        await download_log_file(GIST_URL, FILE_NAME)

        # Parse the log file after download, using cache
        games = await get_or_parse_log(FILE_NAME)

        # Clean up by deleting the log file
        os.remove(FILE_NAME)

        return {"games": games}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


@app.get("/player_kills")
async def player_kills_endpoint():
    try:
        games = await get_or_parse_log(FILE_NAME)
        player_kills = get_player_kills(games)
        sorted_player_kills = dict(sorted(player_kills.items(), key=lambda item: item[1], reverse=True))
        return {"player_kills": sorted_player_kills}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/means_usage")
async def means_usage_endpoint():
    try:
        games = await get_or_parse_log(FILE_NAME)
        kills_by_means = get_kills_by_means(games)
        sorted_means_usage = dict(sorted(kills_by_means.items(), key=lambda item: item[1], reverse=True))
        return {"means_usage": sorted_means_usage}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/total_kills")
async def total_kills_endpoint():
    try:
        games = await get_or_parse_log(FILE_NAME)
        total_kills = get_total_kills(games)
        return {"total_kills": total_kills}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/used_means_by_player")
async def used_means_by_player_endpoint():
    try:
        games = await get_or_parse_log(FILE_NAME)
        means_by_player = get_used_means_by_player(games)
        sorted_means_by_player = {
            player: dict(sorted(means.items(), key=lambda item: item[1], reverse=True))
            for player, means in means_by_player.items()
        }
        return {"used_means_by_player": sorted_means_by_player}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
