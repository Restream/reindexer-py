import shlex
import subprocess

import requests
from requests.adapters import HTTPAdapter, Retry

from tests.helpers.log_helper import log_fixture


session = requests.Session()
Retry.DEFAULT_BACKOFF_MAX = 0.03
retry = Retry(total=100, backoff_factor=0.03)
adapter = HTTPAdapter(max_retries=retry)
session.mount("http://", adapter)


class ReindexerServer:

    def __init__(self, http_port=9088, rpc_port=6534, storage="/tmp/reindex_test",
                 auth=False, user=None, password=None):
        self.http_port = http_port
        self.rpc_port = rpc_port
        self.httpaddr = f"127.0.0.1:{http_port}"
        self.rpcaddr = f"127.0.0.1:{rpc_port}"

        self.storage = storage

        self.auth = auth
        self.user = user
        self.password = password

        self.proc = None

        self.__cmd = f"reindexer_server --db {self.storage} --httpaddr={self.httpaddr} --rpcaddr={self.rpcaddr}"
        if self.auth:
            self.__cmd += " --security"

    def run(self, *args):
        command = shlex.split(self.__cmd) + list(args)
        self.proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                     universal_newlines=True, bufsize=1)
        self.is_running()
        log_fixture.info(f"Reindexer server started at {self.http_port} http port")

    def is_running(self):
        try:
            url = f"http://{self.httpaddr}/api/v1/check"
            auth = (self.user, self.password) if self.auth else None
            session.get(url=url, auth=auth)
            return True
        except (ConnectionError, requests.exceptions.ConnectionError, RecursionError, ChildProcessError,
                AssertionError):
            self.terminate()
            if not hasattr(self.proc, "returncode"):
                raise ChildProcessError("Server is not running")
            else:
                raise ChildProcessError(f"Server status code is {self.proc.returncode}")

    def terminate(self):
        try:
            self.proc.terminate()
            self.proc.wait(timeout=1)
        except subprocess.TimeoutExpired:
            self.proc.kill()
