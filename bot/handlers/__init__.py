from .base import router as base_router
from .habits_buttons import router as habits_btn_router
from .habits_commands import router as habits_cmd_router

routers = [base_router, habits_btn_router, habits_cmd_router]
