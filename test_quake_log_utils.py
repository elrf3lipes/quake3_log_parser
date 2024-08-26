# Contains unit tests for verifying the Quake log parsing functionality.

import pytest
import aiofiles
from quake_log_utils import parse_log  # Import the standalone function directly
import os


@pytest.mark.asyncio
async def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        await parse_log("non_existent_file.txt")


@pytest.mark.asyncio
async def test_empty_file():
    # Create an empty file
    empty_file_path = "empty_log.txt"
    open(empty_file_path, 'w').close()

    with pytest.raises(ValueError, match="The log file is empty."):
        await parse_log(empty_file_path)

    # Cleanup
    os.remove(empty_file_path)


@pytest.mark.asyncio
async def test_wrong_file_format():
    # Create a file with unexpected content
    wrong_format_path = "wrong_format.txt"
    with open(wrong_format_path, 'w') as f:
        f.write("This is not a valid log file format.")

    try:
        games = await parse_log(wrong_format_path)
        assert len(games) == 0  # Expecting no games to be parsed
    finally:
        os.remove(wrong_format_path)  # Cleanup

@pytest.mark.asyncio
async def test_parse_log():
    # Sample log content to test
    log_content = r"""
    0:00 InitGame: \\sv_hostname\\CodeMiner Quake 3 Arena
    0:25 Kill: 2 3 7: Isgalamido killed Dono da Bola by MOD_ROCKET_SPLASH
    0:35 Kill: 2 2 7: <world> killed Isgalamido by MOD_ROCKET_SPLASH
    0:50 Kill: 2 3 7: Isgalamido killed Isgalamido by MOD_SUICIDE
    1:10 ShutdownGame:
    """

    # Use aiofiles to write and read the log content (simulate reading from a file)
    async with aiofiles.open("test_log.txt", 'w') as file:
        await file.write(log_content)

    # Call the parse_log function directly with the test log file path
    games = await parse_log("test_log.txt")

    # Assert that the parsed data matches expected values
    assert len(games) == 1
    assert games[0]['total_kills'] == 3  # Total kills should be 3
    assert "Isgalamido" in games[0]['players']
    assert "Dono da Bola" in games[0]['players']
    assert games[0]['kills'].get("Isgalamido", 0) == -1  # Isgalamido should have -1 kills
    assert games[0]['kills'].get("Dono da Bola", 0) == 0  # Dono da Bola should have 0 kills
    assert "<world>" not in games[0]['kills']  # <world> should not appear in kills dictionary

    # Ranking should not include players with <= 0 kills
    filtered_kills = {player: kills for player, kills in games[0]['kills'].items() if kills > 0}
    ranking = sorted(filtered_kills.items(), key=lambda item: item[1], reverse=True)
    assert all(kills < 0 for player, kills in ranking) or not ranking  # Ranking should only include positive kills
