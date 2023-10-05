import asyncio

from binance import AsyncClient, BinanceSocketManager


async def listen(api_key: str, api_secret: str, symbol: str):
    client = await AsyncClient.create(api_key=api_key, api_secret=api_secret)
    bm = BinanceSocketManager(client)
    # start any sockets here, i.e a trade socket
    ts = bm.kline_socket(symbol=symbol)
    # then start receiving messages
    async with ts as tscm:
        while True:
            try:
                res = await tscm.recv()
                print(res)
            except Exception as e:
                print(e)
                break

    await client.close_connection()


async def main(api_key: str, api_secret: str, symbols: list):
    G = await asyncio.gather(*(listen(api_key, api_secret, s) for s in symbols))
    print(G)


if __name__ == "__main__":
    symbols = ["BTCUSDT", "ETHUSDT"]
    asyncio.run(main(None, None, symbols))
