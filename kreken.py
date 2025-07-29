from rich import print
from rich.console import Console

import sys
import json
import asyncio
import aiosqlite
import pyfiglet
import yaspin
import typer
import rich

DB_PATH = 'data/data.db'

async def check_db(prefix, db):
    sql_query = "SELECT prefix FROM prefixes WHERE prefix = ?"

    cursor = await db.execute(sql_query, (prefix, ))

    prefixes = await cursor.fetchone()

    return False if not prefixes else True


async def search_db(prefix, fullhash, db):
    sql_query = "SELECT password, hash FROM fullPairings WHERE prefix = ? AND hash = ?"
    cursor = await db.execute(sql_query, (prefix, fullhash))

    results = await cursor.fetchone()
    
    return results

async def listening():
    db = await aiosqlite.connect(DB_PATH) 

    # Return the running event loop in the current OS thread.
    loop = asyncio.get_event_loop()
    # Read data from IO stream
    reader = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(reader)
    # Make stidin non-blocking for reading
    await loop.connect_read_pipe(lambda: protocol, sys.stdin)

    while True:
        console.log(f"[bold cyan2]{'Receiver':10}[/bold cyan2] Listening for hash values")

        line = await reader.readline()
        json_string = line.strip()

        if json_string:
            mapping = []
            data = json.loads(json_string)
            hash0, _ = data[0].split(':')
            prefix = hash0[:5]

            has_prefix = await check_db(prefix, db)

            if has_prefix:                 
                console.log(f"[bold cyan2]{'Receiver':10}[/bold cyan2] Looking for hash values starting with [light_slate_blue]{prefix}[/light_slate_blue]")

                for row in data:
                    full_hash,_ = (row.strip()).split(':')
                    results = await search_db(prefix, full_hash.lower(), db)

                    if not results:
                        continue
                    else:
                        mapping.append(results)
            else:
                console.log(f"[bold grey66]{'Not Found':10}[/bold grey66][grey66] No hashes in database that start with [/grey66][light_slate_blue]{prefix}[/light_slate_blue].", end='\n\n')


            if mapping:
                console.log(f"[bold spring_green2]{'Found':10}[/bold spring_green2][spring_green2] Found hash-plaintext pairs for starting with [/spring_green2][light_slate_blue]{prefix}[/light_slate_blue].")
                print()
                print(f"{' ':22}[bold spring_green2]{'Plaintext':40}{'Hash':20}[/bold spring_green2]")
                for m in mapping:
                    print(f"{' ':22}[spring_green2]{m[0]:40}[/spring_green2][dim spring_green2]{m[1]:20}[/dim spring_green2]")
                print()
            else:
                console.log(f"[bold grey66]{'Not Found':10}[/bold grey66][grey66] No hash-plaintext pairs found that starts with [/grey66][light_slate_blue]{prefix}[/light_slate_blue].", end='\n\n')
            


def main():
    asyncio.run(listening())

if __name__ == '__main__':
    console = Console()
    main()