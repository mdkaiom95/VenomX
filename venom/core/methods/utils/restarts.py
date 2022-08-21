# taken from USERGE-X

import os
import signal
import psutil
import sys

from pyrogram import Client as RClient

from venom import logging

_LOG = logging.getLogger(__name__)
_LOG_STR = "### %s ###"

class Restart():

    async def restart(self, update_req: bool = False, hard: bool = False) -> None:
        _LOG.info(_LOG_STR, "Restarting VenomX")
        await self.stop()
        if update_req:
            _LOG.info(_LOG_STR, "Updating requirements")
            os.system("pip3 install -U pip && pip3 install -U -r requirements.txt")
            _LOG.info(_LOG_STR, "Requirements updated")
        if hard:
            os.kill(os.getpid(), signal.SIGUSR1)
        else:
            try:
                c_p = psutil.Process(os.getpid())
                for handler in c_p.open_files() + c_p.connections():
                    os.close(handler.fd)
            except Exception as c_e:  # pylint: disable=broad-except
                print(_LOG_STR % c_e)
            os.execl(sys.executable, sys.executable, '-m', 'venom')
            sys.exit()