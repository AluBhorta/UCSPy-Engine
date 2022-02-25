
from core.UCSPyEngine import UCSPyEngine


class UCSPyEngineTest:
    def __init__(self, config_file="ucsp.config.json"):
        self.ucspy_engine = UCSPyEngine()

    def run(self):
        try:
            # test solve
            self.ucspy_engine.solve(epochs=5)

            # test inspect
            self.ucspy_engine.inspect()

            # test plot
            self.ucspy_engine.plot(should_wait=False)

            print("\ntests succeeded! ✅")
        except Exception as e:
            print("\ntests failed! ❌")
            raise e
            
