import asyncio

import websockets

TARGET_WS_SERVER = "ws://localhost:8765"


connected_clients = set()

async def echo(websocket, path):
    # Добавляем нового клиента в список подключенных
    if websocket not in connected_clients:
        connected_clients.add(websocket)
    try:
        async for message in websocket:
            print(f"Received message from MicroPython: {message}")

            # Отправляем сообщение другим клиентам (например, FrontEnd)
            for client in connected_clients:
                if client != websocket:
                    await client.send(message)
            
            # Также отправляем на другой WebSocket-сервер, если нужно
            try:
                async with websockets.connect(TARGET_WS_SERVER) as target_ws:
                    print(f"Sending message to target server: {message}")
                    await target_ws.send(message)
            except websockets.exceptions.ConnectionClosedError as e:
                print(f"Connection closed unexpectedly: {e.code} {e.reason}")
            except Exception as e:
                print(f"Error sending message to another WebSocket: {e}")

    except websockets.exceptions.ConnectionClosedError:
        print("Connection closed")
    finally:
        # Удаляем клиента, если он отключился
        connected_clients.remove(websocket)


async def main():
    server_1 = await websockets.serve(echo, "localhost", 8765)

    print("Server is running on ws://localhost:8765")
    try:
        # Бесконечное ожидание
        await asyncio.Future()
    except asyncio.CancelledError:
        print("Server was stopped.")
    finally:
        # Закрываем сервер корректно при завершении программы
        server_1.close()
        await server_1.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
