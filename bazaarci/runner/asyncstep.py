""" asyncStep
Definition of the Step class and run behavior decorator functions
"""
from functools import reduce, wraps
import asyncio
from asyncio import Event
from typing import Callable, Optional

from bazaarci.runner.node import Node
from bazaarci.runner.asyncproduct import asyncProduct


class asyncStep(Node):
    def __init__(self, name, graph: Optional["Graph"] = None, target: Optional[Callable] = None):
        super().__init__(name, graph)
        self._consumes = set()
        self._produces = set()
        self.target = target
        self.output = None
        if self.graph is not None:
            self.graph.add(self)

    # NOTE: Should produces and consumes be awaitable?
    def produces(self, item: str = None):
        if item is None:
            return self._produces
        # The ability to call item.set() is necessary for outputs.
        elif hasattr(item, "set") and callable(item.set):
            self._produces.add(item)

    def consumes(self, item: str = None):
        if item is None:
            return self._consumes
        # The ability to call item.wait() is necessary for inputs.
        elif hasattr(item, "wait") and callable(item.wait):
            self._consumes.add(item)

#    async def start(self):
#        self.thread = Thread(target=self.run)
#        self.thread.start()

    async def run(self):
        [await asyncproduct.wait() for asyncproduct in self.consumes()]
        if self.target and asyncio.iscoroutinefunction(self.target):
            self.output = await self.target()
        [asyncproduct.set() for asyncproduct in self.produces()]

#    async def wait(self):
#        if self.thread and self.thread.is_alive():
#            self.thread.join()

    def __str__(self):
        return self.name

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.name)

# Was kind of a pain to set up with async. Ignoring this for now
#async def set_run_behavior(class_or_instance, *args):
#    """ Build the run function from _run and the
#    incoming list of behaviorals
#    """
#    run_function = class_or_instance._run
#    for wrapper in reversed(args):
#        run_function = await wrapper(run_function)
#    setattr(class_or_instance, "run", run_function)
#
#
#async def wait_for_producers(func):
#    """ Waits on all `Product`s in `self.consumes` before
#    calling the function.
#    """
#    @wraps(func)
#    def wrapped(self):
#        [await asyncproduct.wait() for asyncproduct in self.consumes()]
#        await func(self)
#    return wrapped
#
#
#def skip_if_redundant(func):
#    """ Calls the function only if any output `Product`s
#    have not been set yet.
#    """
#    @wraps(func)
#    def wrapped(self):
#        # If there are output products and they have all already been set,
#        # then this step is not required to run.
#        # TODO: await the wait?
#        all_set = reduce(lambda x, y: x and y.wait(0), self.produces(), True)
#        if len(self.produces()) == 0 or not all_set:
#            func(self)
#    return wrapped


# By default, Step should wait for producers
#set_run_behavior(Step, wait_for_producers)
