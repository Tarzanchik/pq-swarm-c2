"""
Asynchronous simulation of swarm message passing.
Each node runs as a task and listens to a message queue.
"""

import json
import os
import asyncio
from pq_swarm.node import Node
from pq_swarm.logger import log_msg, log_feedback

class AsyncNode(Node):
    def __init__(self, node_id: str):
        super().__init__(node_id)
        self.inbox = asyncio.Queue()

    async def run(self):
        """Main async loop: process incoming messages."""
        while True:
            self.check_command_file()
            try:
                msg = await asyncio.wait_for(self.inbox.get(), timeout=1)
                print(f"[{self.node_id}] received: {msg}")
                self.inbox.task_done()
            except asyncio.TimeoutError:
                pass

    def send(self, message: str):
        """Broadcast message to all peers."""
        for peer in self.peers.values():
            full_msg = f"{self.node_id} → {peer.node_id}: {message}"
            asyncio.create_task(peer.inbox.put(full_msg))
            log_msg(full_msg)

    def check_command_file(self):
        """Check if there's a command in swarm_api.json addressed to this node."""
        if not os.path.exists("swarm_api.json"):
            return
        with open("swarm_api.json", "r") as f:
            data = json.load(f)
        if data["target"] == self.node_id and data["last_command"]:
            full_msg = f"[EXECUTE] {self.node_id}: {data['last_command']}"
            print(full_msg)
            log_msg(full_msg)
            log_feedback(f"{self.node_id} ACK: {data['last_command']}")

            # очистить команду после исполнения
            with open("swarm_api.json", "w") as f:
                json.dump({"target": "", "last_command": ""}, f)

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

    # ждём обработки очередей и команды из JSON
    await asyncio.sleep(10)

    # останавливаем симуляцию
    for t in tasks:
        t.cancel()

asyncio.run(main())
