import shlex
import subprocess

import requests
from requests.adapters import HTTPAdapter, Retry


session = requests.Session()
Retry.DEFAULT_BACKOFF_MAX = 0.03
retry = Retry(total=100, backoff_factor=0.03)
adapter = HTTPAdapter(max_retries=retry)
session.mount("http://", adapter)
session.mount("https://", adapter)
session.verify = False


class ReindexerServer:

    def __init__(self, http_port=9088, rpc_port=6534, https_port=None, rpcs_port=None,
                 storage="/tmp/reindex_test", auth=False, user=None, password=None,
                 ssl_cert="", ssl_key=""):
        self.http_port = http_port
        self.rpc_port = rpc_port
        self.https_port = https_port
        self.rpcs_port = rpcs_port
        self.httpaddr = f"127.0.0.1:{http_port}"
        self.rpcaddr = f"127.0.0.1:{rpc_port}"
        self.httpsaddr = f"127.0.0.1:{https_port}" if self.https_port else None
        self.rpcsaddr = f"127.0.0.1:{rpcs_port}" if self.rpcs_port else None

        self.storage = storage

        self.auth = auth
        self.user = user
        self.password = password

        self.ssl_cert = ssl_cert
        self.ssl_key = ssl_key

        self.proc = None

        self.__cmd = f"reindexer_server --db {self.storage} --httpaddr={self.httpaddr} --rpcaddr={self.rpcaddr} " \
                     f"--httpsaddr={self.httpsaddr} --rpcsaddr={self.rpcsaddr}"
        if self.auth:
            self.__cmd += " --security"
        if self.https_port and self.rpcs_port:
            self.__cmd += f" --ssl-cert {self.ssl_cert} --ssl-key {self.ssl_key}"

    def run(self, *args):
        command = shlex.split(self.__cmd) + list(args)
        self.proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                     universal_newlines=True, bufsize=1)
        self.is_running()

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
