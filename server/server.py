import asyncio

import websockets

TARGET_WS_SERVER = "ws://localhost:8765"


# Список всех подключённых WebSocket-клиентов для порта 8766
connected_clients = set()

# Обработчик для подключения платы MicroPython (на порту 8765)
async def handle_micropython(websocket, path):
    async for message in websocket:
        print(f"Received message from MicroPython: {message}")
        
        # Отправляем сообщение всем подключённым клиентам на порте 8766
        for client in connected_clients:
            try:
                if client != websocket:
                    await client.send(message)
            except Exception as e:
                print(f"Error sending message to client: {e}")

# Обработчик для подключения фронтенда (на порту 8766)
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
    # Запуск сервера для платы MicroPython на порту 8765
    server_micropython = await websockets.serve(handle_micropython, "localhost", 8765)
    print("MicroPython server is running on ws://localhost:8765")

    # Запуск сервера для фронтенда на порту 8766
    server_frontend = await websockets.serve(handle_frontend, "localhost", 8766)
    print("Frontend server is running on ws://localhost:8766")

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
