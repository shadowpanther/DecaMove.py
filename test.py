from ctypes import POINTER
import DecaMove

env = DecaMove.deca_move_env_desc()
callbacks = DecaMove.deca_move_callbacks()
deca_move = DecaMove.deca_move()

DecaMove.decaMoveInit(env, callbacks, POINTER(deca_move))
