#!/opt/xsite/cte/tools/python/bin/python3
import sys
import asyncio
sys.path.append(f"..")
from bazaarci.runner.asyncgraph import asyncGraph
from bazaarci.runner.asyncstep import asyncStep
from bazaarci.runner.asyncproduct import asyncProduct
import random

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

def main():
    session = asyncGraph('asyncTest')
    prod1 = asyncProduct('p1')
    prod2 = asyncProduct('p2')
    node1 = asyncStepTest('step1', session)
    node2 = asyncStepTest('step2', session)
    node3 = asyncStepTest('step3', session)
    node1.produces(prod1)
    node2.produces(prod2)
    node3.consumes(prod1)
    node3.consumes(prod2)
    session.run()
    results = [step.output for step in session]
    print(results)

if __name__ == "__main__":
    rc = main()
    sys.exit(rc)
