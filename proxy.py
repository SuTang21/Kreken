from mitmproxy import http
from mitmproxy.tools.dump import DumpMaster
from mitmproxy.options import Options
from rich import print
from rich.console import Console

import asyncio
import logging
import zlib
import json
import pyfiglet
import typer

app = typer.Typer()
logging.getLogger("mitmproxy").setLevel(logging.CRITICAL)

class HIBPLogger():
    def __init__(self):
        self.process = None

    async def start_process(self):
        self.process = await asyncio.create_subprocess_exec(
            "python3", "kreken.py",
            stdin=asyncio.subprocess.PIPE
        )
    
    async def stop_process(self):
        if self.process:
            self.process.terminate()
            await self.process.wait()
            console.log("[bold red] Receiver has shut down.")

    def response(self, flow: http.HTTPFlow):
        filter = "https://api.pwnedpasswords.com/range/"

        if (filter in flow.request.pretty_url):
            prefix = flow.request.pretty_url[-5:].lower()
            
            console.log(f"[bold dodger_blue2]{'Proxy':10}[/bold dodger_blue2] Intercepted HIBP API: [light_slate_blue]{prefix}[/light_slate_blue]")
            if flow.response:
                content_encoding = flow.response.headers.get("Content-Encoding", "").lower()
                raw_content = flow.response.content

                if content_encoding == "gzip":
                    try:
                        decompressed = zlib.decompress(raw_content, zlib.MAX_WBITS | 16)
                        suffix = decompressed.decode('utf-8')
                    except Exception as e:
                        console.log(f"[bold red]{'Exception':10}[/bold red] Failed to decompress gzip response: []{e}[/]")
                        suffix = raw_content.decode('utf-8', errors='replace')
                else:
                    suffix = raw_content.decode('utf-8', errors='replace')
            
                suffix = list(prefix+i for i in suffix.split('\n'))

                if suffix:
                    console.log(f"[bold dodger_blue2]{'Proxy':10}[/bold dodger_blue2] Sending to receiver ...")

                    json_suffix = json.dumps(suffix)
                    self.process.stdin.write((json_suffix+"\n").encode())

async def start_proxy():
    options = Options(listen_host = "127.0.0.1", listen_port=8080)
    proxy = DumpMaster(options, with_termlog=False, with_dumper=False)
    addon = HIBPLogger()
    await addon.start_process()
    proxy.addons.add(addon)
    console.log(f"[bold dodger_blue2]{'Proxy':10}[/bold dodger_blue2] Starting proxy on http://127.0.0.1:8080")

    listener_task = asyncio.create_task(shutdown_listener(proxy, addon))

    try:
        await proxy.run()
    except KeyboardInterrupt:
        console.log(f"[bold dodger_blue2]{'Proxy':10}[/bold dodger_blue2] Proxy shutting down ...")
    finally:
        proxy.shutdown()
        listener_task.cancel()

@app.command()
def proxy_main():
    asyncio.run(start_proxy())

async def shutdown_listener(proxy, addon):
    loop = asyncio.get_running_loop()

    while True:
        user_input = await loop.run_in_executor(None, input, "")
        if user_input.strip().lower() == "x":
            console.log("[bold red]Shutting down proxy ... [/bold red]")
            proxy.shutdown()
            await addon.stop_process()
            break

if __name__ == "__main__":
    console = Console()
    print()
    print()
    print(f"[white]{pyfiglet.figlet_format("KREKEN", font="slant")}[/white]")
    print(f"[white]{'*'*60}\n\nKreken intercepts SHA1 hash password prefix queries" \
    "\n" \
    "sent to Have I Been Pwned (HIBP) API and returns\n" \
    "plaintext mappings of response from HIBP\n" \
    "using a rainbow table with data from SecList. \n\n" \
    "Server listens on localhost:8080 (127.0.01:8080).\n\n" \
    f"To exit, press 'x'. \n\n{'*'*60}\n\n[/white]")

    proxy_main()
