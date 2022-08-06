import asyncio
import sys

import pytest


@pytest.fixture(scope="session", autouse=True)
def fix_set_wakeup_fd_issue():
    """
    see https://stackoverflow.com/questions/60359157/valueerror-set-wakeup-fd-only-works
    -in-main-thread-on-windows-on-python-3-8-wit
    """
    if sys.platform == "win32" and sys.version_info >= (3, 8, 0):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
