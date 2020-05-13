class UnitManagementException(Exception):
    pass

class WorkerManagementException(UnitManagementException):
    pass

class SoldierManagementException(UnitManagementException):
    pass

class StructureManagementException(UnitManagementException):
    pass
