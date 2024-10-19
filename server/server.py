import asyncio
import signal

import websockets
from security import *

# Список всех подключённых WebSocket-клиентов
connected_clients = set()


# Обработчик для подключения платы MicroPython
async def handle_micropython(websocket, path):
    try:
        async for message in websocket:
            if message == "ping":
                await websocket.send("pong")
            else:
                print(f"Received message from MicroPython: {message}")

                # Отправляем сообщение всем подключённым клиентам
                for client in list(connected_clients):  # Создаём копию списка
                    try:
                        if client != websocket:
                            await client.send(message)
                    except websockets.ConnectionClosed:
                        print(f"Client connection closed. Removing from list.")
                        connected_clients.remove(client)
                    except Exception as e:
                        print(f"Error sending message to client: {e}")
                        connected_clients.remove(client)
    except Exception as e:
        print(f"Error in MicroPython connection: {e}")
    finally:
        # Гарантированно удаляем WebSocket из списка, если он ещё там
        if websocket in connected_clients:
            connected_clients.remove(websocket)
        await websocket.close()


async def handle_frontend(websocket, path):
    connected_clients.add(websocket)
    try:
        await asyncio.Future()
    except asyncio.CancelledError:
        print("Frontend client disconnected.")
    finally:
        if websocket in connected_clients:
            connected_clients.remove(websocket)
        await websocket.close()
        print("WebSocket connection closed.")


async def main():
    server_micropython = await websockets.serve(handle_micropython,
                                                MICROPYTHON_HOST,
                                                MICROPYTHON_PORT,
                                                ping_interval=30,
                                                ping_timeout=15)
    print("MicroPython server is running")

    server_frontend = await websockets.serve(handle_frontend, FRONTEND_HOST,
                                             FRONTEND_PORT)
    print("Frontend server is running")

    # Ожидаем пока оба сервера работают
    await asyncio.gather(server_micropython.wait_closed(),
                         server_frontend.wait_closed())


def shutdown():
    print("Shutting down...")


if __name__ == "__main__":
    try:
        # Используем asyncio.run для корректной работы с Ctrl+C
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Interrupted by user, shutting down servers...")
