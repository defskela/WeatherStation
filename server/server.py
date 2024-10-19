import asyncio

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
                for client in connected_clients:
                    try:
                        if client != websocket:
                            await client.send(message)
                    except Exception as e:
                        print(f"Error sending message to client: {e}")
    except websockets.ConnectionClosedError as e:
        print(f"Connection closed: {e}")

# Обработчик для подключения фронтенда
async def handle_frontend(websocket, path):
    # Добавляем нового клиента в список подключённых
    connected_clients.add(websocket)
    try:
        # Ожидаем, пока клиент не отключится
        await asyncio.Future()  # Это позволит держать соединение открытым
    except asyncio.CancelledError:
        print("Frontend client disconnected.")
    finally:
        # Удаляем клиента из списка при отключении
        connected_clients.remove(websocket)


async def main():
    server_micropython = await websockets.serve(handle_micropython, MICROPYTHON_HOST, MICROPYTHON_PORT, ping_interval=30, ping_timeout=15)
    print("MicroPython server is running")

    server_frontend = await websockets.serve(handle_frontend, FRONTEND_HOST, FRONTEND_PORT)
    print("Frontend server is running")

    try:
        # Бесконечное ожидание
        await asyncio.Future()
    except asyncio.CancelledError:
        print("Servers is stopping...")
        server_micropython.close()
        await server_micropython.wait_closed()

        server_frontend.close()
        await server_frontend.wait_closed()
    finally:
        # Корректно останавливаем серверы
        server_micropython.close()
        await server_micropython.wait_closed()

        server_frontend.close()
        await server_frontend.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
