from ctypes import *
import os
import pathlib

if __name__ == "__main__":
    exit()

# deca_move_state
kDecaMoveStateClosed    = 0
kDecaMoveStateOpen      = 1
kDecaMoveStatePaired    = 2
kDecaMoveStateStreaming = 3
deca_move_state = c_int

# deca_move_status
kDecaMoveStatusSuccess             = 0
kDecaMoveStatusErrorDataPort       = 1
kDecaMoveStatusErrorNotConnected   = 2
kDecaMoveStatusErrorNotImplemented = 3
kDecaMoveStatusErrorUnknown        = 4
deca_move_status = c_int

# deca_move_feedback
kDecaMoveFeedbackEnteringSleep = 0
kDecaMoveFeedbackLeavingSleep  = 1
kDecaMoveFeedbackShuttingDown  = 2
kDecaMoveFeedbackSingleClick   = 3
kDecaMoveFeedbackDoubleClick   = 4
kDecaMoveFeedbackTripleClick   = 5
deca_move_feedback = c_int

# deca_move_accuracy

# deca_move_env_flag

# deca_move_env_log_level
kDecaMoveEnvLogLevelTrace    = 1
kDecaMoveEnvLogLevelDebug    = 2
kDecaMoveEnvLogLevelInfo     = 3
kDecaMoveEnvLogLevelWarn     = 4
kDecaMoveEnvLogLevelErr      = 5
kDecaMoveEnvLogLevelCritical = 6
deca_move_env_log_level = c_int

class deca_move_quaternion_components(Structure):
    _fields_ = [
        ("x", c_float),
        ("y", c_float),
        ("z", c_float),
        ("w", c_float)
    ]
class deca_move_quaternion_union(Union):
    _anonymous_ = ("components", )
    _fields_ = [
        ("components", deca_move_quaternion_components),
        ("array", c_float * 4)
    ]
class deca_move_quaternion(Structure):
    _anonymous_ = ("union", )
    _fields_ = [
        ("union", deca_move_quaternion_union)
    ]

deca_move_env_log_callback_t = CFUNCTYPE(c_void_p, deca_move_env_log_level, c_char_p, c_void_p)
class deca_move_env_desc(Structure):
    _fields_ = [
        ("flags", c_uint32),
        ("log_callback", deca_move_env_log_callback_t),
        ("log_user_data", c_void_p)
    ]

class deca_move_callbacks(Structure):
    _fields_ = [
        ("user_data", c_void_p),
        ("feedback_cb", CFUNCTYPE(None, c_int, c_void_p)),
        ("battery_update_cb", CFUNCTYPE(None, c_float, c_void_p)),
        ("orientation_update_cb", CFUNCTYPE(None, deca_move_quaternion, c_int, c_float, c_void_p)),
        ("position_update_cb", CFUNCTYPE(None, c_float, c_float, c_float, c_void_p)),
        ("state_update_cb", CFUNCTYPE(None, c_int, c_void_p)),
        ("imu_calibration_request_cb", CFUNCTYPE(None, c_void_p))
    ]

class deca_move(Structure):
    _fields_ = [
        ("_", c_void_p)
    ]

os.add_dll_directory(pathlib.Path().absolute())
DecaMoveLib = CDLL("deca_sdk")

decaMoveInit = DecaMoveLib.decaMoveInit
decaMoveInit.restype = deca_move_status
decaMoveInit.argtypes = (
    deca_move_env_desc,
    deca_move_callbacks,
    POINTER(deca_move)
)
# class DecaMove:
    # def __init__(self) -> None:
    #     pass
        # try:
            # os.add_dll_directory(pathlib.Path().absolute())
            # self.DecaMoveLib = CDLL("deca_sdk")
        # except Exception as e:
            # print(e)