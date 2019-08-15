import aiohttp
import asyncio
import logging
import inspect

from .message import wrap_message

log = logging.getLogger('listenmoe')


class Client():
    def __init__(self, loop=None, aiosession=None, kpop: bool = False, url=None):
        self._headers = {
            "User-Agent": "listenmoe (https://github.com/Zenrac/listenmoe)",
            "Content-Type": "application/json",
            "Accept": "application/vnd.listen.v4+json",
            "library": "kpop" if kpop else "jpop",
        }
        self.url = ('wss://listen.moe/kpop/gateway_v2' if kpop \
                else 'wss://listen.moe/gateway_v2') if not url else url
        self.handler = None
        self._loop = loop or asyncio.get_event_loop()
        self._ws = None
        self._session = aiosession if aiosession \
            else aiohttp.ClientSession(loop=self._loop)
        self._closers = [aiohttp.WSMsgType.close,
                         aiohttp.WSMsgType.closing,
                         aiohttp.WSMsgType.closed]

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        return self._loop

    @property
    def connected(self):
        """ Returns whether the websocket is connected to Lavalink. """
        return self._ws is not None and not self._ws.closed

    async def connect(self):
        log.debug('Connecting to listen.moe!')
        attempt = 0

        while not self.connected:
            attempt += 1

            try:
                self._ws = await self._session.ws_connect(self.url, headers=self._headers)
            except aiohttp.ClientError:
                if attempt == 1:
                    log.warning('Failed to connect to listen.moe!')

                wait = min(5 * attempt, 60)  # Max wait 60 secs.
                await asyncio.sleep(wait)
            else:
                log.info('Connected to listen.moe!')
                asyncio.ensure_future(self._send(op=0, d={'auth': ''}))
                asyncio.ensure_future(self.listen())

    async def listen(self):
        async for msg in self._ws:
            if self.handler:

                if msg.type == aiohttp.WSMsgType.text:
                    await self._handle_message(msg.json())
                elif msg.type in self._closers:
                    await self._websocket_closed(msg.data, msg.extra)
                    return
            else:
                raise RuntimeError("No function handler specified")

        await self._websocket_closed()

    async def _handle_message(self, data: dict):
        op = data['op']
        if op == 0:
            heartbeat = data['d']['heartbeat'] / 1000
            asyncio.ensure_future(self._send_pings(heartbeat))

        if op == 1:
            wrapped_message = wrap_message(data)
            try:
                if inspect.iscoroutinefunction(self.handler):
                    await self.handler(wrapped_message)
                else:
                    self.handler(wrapped_message)
            except Exception as e:  # pylint: disable=W0703
                log.warning('Event handler encountered an exception!', e)

    async def _send_pings(self, interval=45):
        while self.connected:
            await asyncio.sleep(interval)
            log.debug('Sending heartbeat to listen.moe')            
            await self._send(op=9)

    async def _send(self, **data):
        if self.connected:
            await self._ws.send_json(data)

    async def _websocket_closed(self, code: int = None, reason: str = None):
        log.debug('Connection to listen.moe closed code: {}, reason: {}!'.format(code, reason))
        self._ws = None
        await self.connect()

    async def start(self):
        asyncio.ensure_future(self.connect())

    def register_handler(self, handler):
        """Registers a function handler to allow you to do something with the socket API data"""
        self.handler = handler
