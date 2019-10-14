#!/opt/xsite/cte/tools/python/bin/python3
import sys
import asyncio
sys.path.append(f"..")
from bazaarci.runner.asyncgraph import asyncGraph
from bazaarci.runner.asyncstep import asyncStep
from bazaarci.runner.asyncproduct import asyncProduct
import random
import logging

class asyncStepTest(asyncStep):
    def __init__(self, name, session):
        self.name = name
        self.session = session
        super().__init__(
            name=name, 
            graph=session,
            target=self.asyncFunc)

    async def asyncFunc(self):
        print(f'{self.name} starting')
        await asyncio.sleep(random.random())
        print(f'{self.name} ending')
        return self.name

async def main():
    session = asyncGraph('asyncTest')
    prod1 = asyncProduct('p1')
    prod2 = asyncProduct('p2')
    prod3 = asyncProduct('p3')
    prod4 = asyncProduct('p4')
    node1 = asyncStepTest('step1', session)
    node2 = asyncStepTest('step2', session)
    node3 = asyncStepTest('step3', session)
    node4 = asyncStepTest('step4', session)
    node1.produces(prod1)
    node2.produces(prod2)
    node4.produces(prod4)
    node3.produces(prod3)
    node3.consumes(prod1)
    node3.consumes(prod2)
    products = [prod.name for prod in session.produces()]
    consumes = [prod.name for prod in session.consumes()]
    print(f"PRODUCES : {products}")
    print(f"CONSUMES : {consumes}")
    results = await session.runInLoop()
    print(results)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except:
        logging.exception(f"Unexpected exception")
    finally:
        loop.close()
    sys.exit(0)
