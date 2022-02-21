
from core.models.UCSPyEngine import UCSPyEngine


class UCSPyEngineTest:
    def __init__(self, config_file="ucsp.config.json"):
        self.ucspy_engine = UCSPyEngine()

    def run_tests(self):
        # test solve
        self.ucspy_engine.solve(epochs=5)

        # test inspect
        self.ucspy_engine.inspect()

        # test plot
        self.ucspy_engine.plot(should_wait=False)
