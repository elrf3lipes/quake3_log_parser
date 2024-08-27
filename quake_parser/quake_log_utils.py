# quake_log_utils.py

import re
import aiofiles
from collections import defaultdict

# Means of death mapping
means_of_death = {
    "1": "MOD_SHOTGUN",
    "2": "MOD_GAUNTLET",
    "3": "MOD_MACHINEGUN",
    "4": "MOD_GRENADE",
    "5": "MOD_GRENADE_SPLASH",
    "6": "MOD_ROCKET",
    "7": "MOD_ROCKET_SPLASH",
    "8": "MOD_PLASMA",
    "9": "MOD_PLASMA_SPLASH",
    "10": "MOD_RAILGUN",
    "11": "MOD_LIGHTNING",
    "12": "MOD_BFG",
    "13": "MOD_BFG_SPLASH",
    "14": "MOD_WATER",
    "15": "MOD_SLIME",
    "16": "MOD_LAVA",
    "17": "MOD_CRUSH",
    "18": "MOD_TELEFRAG",
    "19": "MOD_FALLING",
    "20": "MOD_SUICIDE",
    "21": "MOD_TARGET_LASER",
    "22": "MOD_TRIGGER_HURT",
    "23": "MOD_NAIL",
    "24": "MOD_CHAINGUN",
    "25": "MOD_PROXIMITY_MINE",
    "26": "MOD_KAMIKAZE",
    "27": "MOD_JUICED",
    "28": "MOD_GRAPPLE"
}

# Compile regex patterns
kill_pattern = re.compile(r'^\s*\d+:\d+\sKill:\s(\d+)\s(\d+)\s(\d+):\s(.+)\skilled\s(.+)\sby\s(.+)$')


async def parse_log(file_path):
    games = []

    try:
        async with aiofiles.open(file_path, 'r') as file:
            content = await file.read()
            if not content.strip():  # Check if the file is empty
                raise ValueError("The log file is empty.")

    except FileNotFoundError:
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")

    except ValueError as ve:
        raise ve

    except Exception as e:
        raise RuntimeError(f"An error occurred while reading the file: {str(e)}")

    async with aiofiles.open(file_path, 'r') as file:
        content = await file.read()

    lines = content.splitlines()
    current_game = None

    for line in lines:
        if 'InitGame:' in line:
            if current_game:
                games.append(current_game)
            current_game = {
                'total_kills': 0,
                'players': set(),
                'kills': defaultdict(int),
                'kills_by_means': defaultdict(int)
            }

        matches = kill_pattern.findall(line)
        for match in matches:
            killer_id, victim_id, mod, killer, victim, weapon = match

            current_game['total_kills'] += 1
            current_game['players'].add(victim)
            means = means_of_death.get(mod, "MOD_UNKNOWN")
            current_game['kills_by_means'][means] += 1

            if killer == victim:  # Self-kill
                current_game['kills'][killer] -= 1
            elif killer != '<world>':
                current_game['players'].add(killer)
                current_game['kills'][killer] += 1
            else:
                current_game['kills'][victim] -= 1  # <world> kill

    if current_game:  # Append last game
        games.append(current_game)

    return games


def get_total_kills(games):
    """ Returns the total number of kills across all games. """
    return sum(game['total_kills'] for game in games)


def get_player_kills(games):
    """ Returns a dictionary with players and their total kill counts for all games. """
    player_kills = defaultdict(int)
    for game in games:
        for player, kills in game['kills'].items():
            player_kills[player] += kills
    return dict(player_kills)


def get_kills_by_means(games):
    """ Returns a dictionary with kill means and their counts for all games. """
    means_counts = defaultdict(int)
    for game in games:
        for means, count in game['kills_by_means'].items():
            means_counts[means] += count
    return dict(means_counts)


def get_used_means_by_player(games):
    """ Returns a dictionary with players and the number of times they used each means of death. """
    player_means = defaultdict(lambda: defaultdict(int))

    for game in games:
        for killer, _ in game['kills'].items():
            for means, count in game['kills_by_means'].items():
                player_means[killer][means] += count

    # Sort the means by count in descending order for each player
    sorted_player_means = {
        player: dict(sorted(means.items(), key=lambda item: item[1], reverse=True))
        for player, means in player_means.items()
    }

    return sorted_player_means


