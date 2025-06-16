from .base import router as base_router
from .habits_buttons import router as habits_buttons_router
from .habits_commands import router as habits_commands_router

routers = [base_router, habits_buttons_router, habits_commands_router]

