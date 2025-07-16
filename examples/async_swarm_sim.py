"""
Asynchronous simulation of swarm message passing.
Each node runs as a task and listens to a message queue.
"""

import asyncio
from pq_swarm.node import Node

class AsyncNode(Node):
    def __init__(self, node_id: str):
        super().__init__(node_id)
        self.inbox = asyncio.Queue()

    async def run(self):
        """Main async loop: process incoming messages."""
        while True:
            msg = await self.inbox.get()
            print(f"[{self.node_id}] received: {msg}")
            self.inbox.task_done()

    def send(self, message: str):
        """Broadcast message to all peers."""
        for peer in self.peers.values():
            asyncio.create_task(peer.inbox.put(f"{self.node_id}: {message}"))

async def main():
    # создаём 10 узлов
    nodes = [AsyncNode(f"n{i}") for i in range(10)]

    # соединяем всех со всеми
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            nodes[i].connect(nodes[j])

    # запускаем узлы как асинхронные задачи
    tasks = [asyncio.create_task(node.run()) for node in nodes]

    # отправляем сообщение от n0
    nodes[0].send("COMMAND: SWEEP LEFT")

    # ждём обработки очередей
    await asyncio.sleep(1)

    # останавливаем симуляцию
    for t in tasks:
        t.cancel()

asyncio.run(main())
