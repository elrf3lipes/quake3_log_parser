# This  code coordinates the parsing of the Quake log file and generates a report
import asyncio
from quake_log_utils import parse_log
from reporting import print_report


async def main():
    # Test archive path for production
    log_file_path = "quake_log.txt"

    try:
        # Parse the log file and print the report
        games = await parse_log(log_file_path)
        print_report(games)
    except FileNotFoundError as fnfe:
        print(fnfe)
    except ValueError as ve:
        print(ve)
    except RuntimeError as re:
        print(re)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
