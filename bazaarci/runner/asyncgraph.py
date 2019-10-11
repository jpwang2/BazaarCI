from typing import Optional
import logging

from bazaarci.runner.node import Node
import asyncio

class asyncGraph(Node, set):
    def __init__(self, name: str, graph: Optional["Graph"] = None):
        super().__init__(name, graph)

    def produces(self):
        for node in self:
            for product in node.produces():
                yield product

    def consumes(self):
        for node in self:
            for product in node.consumes():
                yield product

#    def start(self):
#        [step.start() for step in self]
#
#    def wait(self):
#        [step.wait() for step in self]

    async def runInLoop(self):
        '''Run the graph if it's already being called in an event loop'''
        asyncRuns = [step.run() for step in self]
        groupRuns = asyncio.gather(*asyncRuns)


    def run(self):
        asyncRuns = [step.run() for step in self]
        groupRuns = asyncio.gather(*asyncRuns)
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(groupRuns)
        except:
            logging.exception(f"Unexpected exception")
        finally:
            loop.close()
