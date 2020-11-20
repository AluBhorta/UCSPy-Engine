from ..db_client import DBClient

class SolverV2:
    def __init__(self, solver_dict: dict, db_client: DBClient):
        self._id = solver_dict.get("id")
        self._name = solver_dict.get("name")
        self._status = solver_dict.get("status")
        self._userConfig = solver_dict.get("userConfig")
        self._createdAtTimestamp = solver_dict.get("createdAtTimestamp")
        self._startedAtTimestamp = solver_dict.get("startedAtTimestamp")
        self._terminatedAtTimestamp = solver_dict.get("terminatedAtTimestamp")
        self._logFileName = solver_dict.get("logFileName")
        self._numSchFileName = solver_dict.get("numSchFileName")
        self._strSchFileName = solver_dict.get("strSchFileName")
        self._db_client = db_client

    def start(self):
        """
        update: status, startedAtTimestamp
        start runnng UCSPSolver.solve()
        save to db

        if UCSPSolver.solve() runs into exception,
            return self._terminate("FAILED")

        if 'stop' is emitted,
            return self.stop()

        when solve() returns, i.e. when COMPLETED
            return self._terminate("COMPLETED")
        """
        raise NotImplementedError

    def stop(self):
        """ 
        interrupt UCSPSolver.solve()
            return self._terminate("STOPPED")
        """
        raise NotImplementedError

    def to_dict(self):
        return {
            "id": self._id,
            "name": self._name,
            "status": self._status,
            "userConfig": self._userConfig,
            "createdAtTimestamp": self._createdAtTimestamp,
            "startedAtTimestamp": self._startedAtTimestamp,
            "terminatedAtTimestamp": self._terminatedAtTimestamp,
            "logFileName": self._logFileName,
            "numSchFileName": self._numSchFileName,
            "strSchFileName": self._strSchFileName,
        }

    def _terminate(self, status="COMPLETED"):
        """ 
        update: status, _terminatedAtTimestamp, _logFileName, _numSchFileName, _strSchFileName
        save to db
        return an event signalling 'status'
        """
        raise NotImplementedError

    def _save_to_db(self):
        self._db_client.update_solver(
            _id=self._id,
            _value=self.to_dict()
        )

    def is_running(self):
        return self._status == "RUNNING"

    def has_terminated(self):
        return self._status in ["COMPLETED", "STOPPED", "FAILED"]


class ConfigDescription:
    def __init__(
        self,
        scheduleParamNames,
        hardConstraints,
        softConstraints,
        fitnessFunctionNames,
        algorithmNames
    ):
        self.scheduleParamNames = scheduleParamNames
        self.hardConstraints = hardConstraints
        self.softConstraints = softConstraints
        self.fitnessFunctionNames = fitnessFunctionNames
        self.algorithmNames = algorithmNames

    def to_api_dict(self):
        return {
            "scheduleParamNames": self.scheduleParamNames,
            "constraints": {
                "hardConstraints": self.hardConstraints,
                "softConstraints": self.softConstraints,
            },
            "fitness": {
                "functionNames": self.functionNames
            },
            "algorithm": {
                "algorithmNames": self.algorithmNames
            }
        }


class HardConstraint:
    def __init__(self, id, desc):
        self.id = id
        self.desc = desc

    def to_api_dict(self):
        return {
            "id": self.id,
            "desc": self.desc,
        }


class SoftConstraint:
    def __init__(self, id, desc, unitPenalty):
        self.id = id
        self.desc = desc
        self.unitPenalty = unitPenalty

    def to_api_dict(self):
        return {
            "id": self.id,
            "desc": self.desc,
            "unitPenalty": self.unitPenalty
        }


class UserConfig:
    def __init__(self, userConfigDict: dict):
        self.scheduleParamName = userConfigDict.get('scheduleParamName')
        self.userHardConstraints = userConfigDict['constraints'].get(
            'userHardConstraints')
        self.userSoftConstraints = userConfigDict['constraints'].get(
            'userSoftConstraints')
        self.fitnessFunc = userConfigDict['fitness'].get('use')
        self.minAcceptableFitness = userConfigDict['fitness'].get(
            'minAcceptableFitness')
        self.algorithm = userConfigDict.get('algorithm')

    def to_api_dict(self):
        return {
            "scheduleParamName": self.scheduleParamName,
            "constraints": {
                "hardConstraints": self.userHardConstraints,
                "softConstraints": self.userSoftConstraints
            },
            "fitness": {
                "use": self.fitnessFunc,
                "minAcceptableFitness": self.minAcceptableFitness
            },
            "algorithm": self.minAcceptableFitness
        }
