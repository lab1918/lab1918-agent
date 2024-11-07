import io
import time
import paramiko

from functools import cache
from lab1918_agent.logger import logger


class SSHCommandError(Exception):
    pass


class SSHClient:
    def __init__(
        self,
        host,
        username,
        key,
        ssh_port=22,
    ):
        self.host = host
        self.username = username
        self.key = key
        self.ssh_port = ssh_port
        self.logger = logger
        self.stdout = None
        self.stderr = None
        self.exit_status = None
        self.__ssh_client = None
        self._open_ssh_session()

    def __str__(self):
        return f"{self.username}@{self.host}:{self.ssh_port}"

    def _open_ssh_session(self):
        self.__ssh_client = paramiko.SSHClient()
        self.__ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.logger.info(f"connecting to: {self.username}@{self.host}:{self.ssh_port}")
        pkey = paramiko.RSAKey.from_private_key(io.StringIO(self.key))
        self.__ssh_client.connect(
            self.host,
            username=self.username,
            pkey=pkey,
            timeout=5.0,
            port=self.ssh_port,
        )
        transport = self.__ssh_client.get_transport()
        transport.set_keepalive(30)
        self.logger.info(f"connected to {self.username}@{self.host}:{self.ssh_port}")

    def _exec_ssh_command(
        self,
        command,
        expected_exit_statuses=None,
    ):
        self.logger.info(f"host: {self.username}@{self.host}:{self.ssh_port}")
        self.logger.info(f"exec command: {command}")
        if not (
            self.__ssh_client.get_transport()
            and self.__ssh_client.get_transport().is_active()
        ):
            self.logger.info(
                f"SSH Connection {self.host}:{self.ssh_port} is inactive, wating 10s and re open ..."
            )
            time.sleep(10)
            self.logger.info(f"re open to {self.host}:{self.ssh_port}")
            self._open_ssh_session()

        _, stdout, stderr = self.__ssh_client.exec_command(command)
        self.stdout = [line.strip() for line in stdout.readlines()]
        self.stderr = [line.strip() for line in stderr.readlines()]
        self.logger.info(f"stdout: {'/n'.join(self.stdout)}")
        self.logger.info(f"stderr: {'/n'.join(self.stderr)}")
        self.exit_status = stdout.channel.recv_exit_status()
        self.logger.info(f"exit status: {self.exit_status}")

        if (
            expected_exit_statuses is not None
            and self.exit_status not in expected_exit_statuses
        ):
            message = f"Unexpected exit status, got {self.exit_status}, expected {expected_exit_statuses}, command: {command}, stderr:  {self.stderr}"
            raise SSHCommandError(message)

    def _close_ssh_session(self):
        self.__ssh_client.close()

    def __del__(self):
        self._close_ssh_session()
        self.logger.info(f"closed paramiko session to {self.host}")

    def run(self, command, expected_exit_statuses=None):
        self._exec_ssh_command(command, expected_exit_statuses)
