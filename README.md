# listenmoe
Unofficial python3 API wrapper to get information about the listen.moe live stream using aiohttp.<br><br>
## Installation
### Using pip
```
pip install listenmoe
```
### Using git
```
pip install git+https://github.com/Zenrac/listenmoe
```

### Requirements: <br>
- Python3+<br>
- [aiohttp](https://github.com/aio-libs/aiohttp) <br>
- asyncio<br>
## Examples: <br>
Handler to get the current song forever<br>
```py
import listenmoe
import asyncio

async def hand(self, msg):
    if msg.type == listen.message.SONG_INFO:
        self.now = msg
    else:
        self.now = msg.raw

moe = listenmoe.client.Client(loop=Optional, aiosession=OptionalToo)
moe.register_handler(self.hand)
task = asyncio.ensure_future(moe.start())
```
To get kpop updates, use `kpop=True` in Client.
```py
listen.client.Client(loop=Optional, aiosession=OptionalToo, kpop=True)
```

## Credits

- [Listen from Yarn](https://github.com/Yarn/Listen) <br>
- [Lavalink.py from Devoxin](https://github.com/Devoxin/Lavalink.py) <br>

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
