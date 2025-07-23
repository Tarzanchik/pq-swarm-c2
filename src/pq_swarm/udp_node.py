import asyncio

class UDPNode:
    def __init__(self, name: str, port: int, peers: list[int]):
        self.name = name
        self.port = port
        self.peers = peers  # list of peer UDP ports
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        print(f"[{self.name}] Listening on port {self.port}")

    def datagram_received(self, data, addr):
        print(f"[{self.name}] Received from {addr}: {data.decode()}")

    async def start(self):
        loop = asyncio.get_running_loop()
        await loop.create_datagram_endpoint(
            lambda: self,
            local_addr=('127.0.0.1', self.port)
        )

    def send(self, message: str):
        for peer_port in self.peers:
            self.transport.sendto(
                f"{self.name}: {message}".encode(),
                ('127.0.0.1', peer_port)
            )
