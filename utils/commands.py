import asyncio
import threading
from abc import abstractmethod, ABC

import numpy as np

from utils.pnm_format import PnmFormat
from utils.pnm_importer import PnmImporter


class Command(ABC):
    """
    The Command interface declares a method for executing a command.
    """

    @abstractmethod
    async def execute(self) -> None:
        pass


class ImportCommand(Command):
    """
    Some commands can implement simple operations on their own.
    """

    def __init__(self, filename: str, presenter_receiver) -> None:
        self._filename = filename
        self._presenter_receiver = presenter_receiver

    async def execute(self) -> None:
        pixels, width, height, max_rgb_value = (
            PnmImporter.get_pixels_and_max_value_from_file(self._filename)
        )
        self._presenter_receiver.view.draw_image(pixels, width, height, max_rgb_value)


class ExportCommand(Command):
    def __init__(
        self, filename: str, algorithm: PnmFormat, arr: np.ndarray, max_value: int
    ) -> None:
        self._filename = filename
        self._algorithm = algorithm
        self._arr = arr
        self._max_value = max_value

    async def execute(self) -> None:
        PnmImporter.export_file(
            self._filename, self._algorithm, self._arr, self._max_value
        )


class InvokerQueue:
    def __init__(self):
        self._queue = asyncio.Queue()
        self._processing = False

    async def add_command(self, cmd: Command):
        await self._queue.put(cmd)
        if not self._processing:
            asyncio.create_task(self._process())

    async def _process(self):
        self._processing = True
        while not self._queue.empty():
            cmd = await self._queue.get()
            await cmd.execute()
            self._queue.task_done()
        self._processing = False


class AsyncLoopThread:
    def __init__(self):
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self._start_loop, daemon=True)
        self.thread.start()

    def _start_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def run_coroutine(self, coro):
        return asyncio.run_coroutine_threadsafe(coro, self.loop)
