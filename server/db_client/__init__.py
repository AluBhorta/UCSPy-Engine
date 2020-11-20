import json


class DBClient:
    def __init__(self):
        pass

    def update_solver(self, _id=None, _value=None):
        raise NotImplementedError

    def _to_json(self):
        return json.dumps(
            self.to_dict()
        )
