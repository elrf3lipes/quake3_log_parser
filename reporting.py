# This code generates reports and rankings from parsed Quake game data

def print_report(games):
    for idx, game in enumerate(games, start=1):
        print("\n")
        print(f"game_{idx}:")
        print(f"  total_kills: {game['total_kills']}")
        print(f"  players: {sorted(list(game['players']))}")
        print("  kills: {")
        for player, kills in game['kills'].items():
            print(f'    "{player}": {kills},')
        print("  }")

        print("  Ranking:")
        # Include players with zero kills, exclude negative kills
        filtered_kills = {player: kills for player, kills in game['kills'].items() if kills >= 0}
        sorted_players = sorted(filtered_kills.items(), key=lambda item: item[1], reverse=True)
        for rank, (player, kills) in enumerate(sorted_players, start=1):
            print(f"    {rank}. {player} - {kills} kills")

        print("\n  Kills by means:")
        for means, count in game['kills_by_means'].items():
            print(f"    {means}: {count}")
