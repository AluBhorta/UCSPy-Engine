
from core.models.UCSPyEngine import UCSPyEngine


class UCSPyEngineTest:
    def __init__(self, config_file="ucsp.config.json"):
        self.ucspy_engine = UCSPyEngine()

    def run_tests(self):
        self._test_solve("ga", epochs=5)
        self._test_solve("meme", epochs=5)
        
    def _test_solve(self, *a, **kw):
        s = self.ucspy_engine.solve(*a, **kw)
