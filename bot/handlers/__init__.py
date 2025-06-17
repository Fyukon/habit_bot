from .base import router as base_router
from .habits_buttons import router as habits_btn_router
from .habits_commands import router as habits_cmd_router
from .handlers_FSM import router as handler_fsm
from .handlers_text import router as handler_text
from .states import *

routers = [base_router, habits_btn_router, habits_cmd_router, handler_text, handler_fsm]
