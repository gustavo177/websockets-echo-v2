import asyncio
import http
import signal

import websockets

# Lista de conexiones
connections = set()

async def echo(websocket):
    # Agregar la nueva conexión a la lista
    connections.add(websocket)
    try:
        # Recibir y enviar mensajes a los clientes conectados
        async for message in websocket:
            for connection in connections:
                await connection.send(message)
    finally:
        # Eliminar la conexión de la lista
        connections.remove(websocket)


async def health_check(path, request_headers):
    if path == "/healthz":
        return http.HTTPStatus.OK, [], b"OK\n"


async def main():
    # Set the stop condition when receiving SIGTERM.
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    async with websockets.serve(
        echo,
        host="",
        port=8080,
        process_request=health_check,
    ):
        await stop


if __name__ == "__main__":
    asyncio.run(main())