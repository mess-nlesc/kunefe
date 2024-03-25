"""Documentation about the kunefe module.

Returns:
    _type_: _description_
"""

import atexit
import getpass
import os
import subprocess
import sys
import time
from shutil import which
from stat import S_ISDIR
from stat import S_ISREG
from typing import Tuple
import jinja2
import paramiko

# setup logging
DEFAULT_LOG_FILENAME = "kunefe.log"
paramiko.util.log_to_file(DEFAULT_LOG_FILENAME)


class Kunefe:
    """Submit jobs to SLURM cluster.

    Attributes:
        username (str): login name of the user.
        hostname (str): hostname or the IP address of the remote system.
        port (int): SSH port to be used by the clients.
        password (int): password to connect to the remote.
        ssh_client: ssh client to connect and run commands on the remote system.
        sftp_client: sftp client to copy files from and to a remote system.
    """

    def __init__(self, username: str, hostname: str, port: int) -> None:
        """Initialize Kunefe class with username, hostname and port.

        Args:
            username (str): login name of the user.
            hostname (str): hostname or the IP address of the remote system.
            port (int): SSH port to be used by the clients.

        Returns:
            None
        """
        self.username = username
        self.hostname = hostname
        self.port = port
        self.password: str
        self.ssh_client: paramiko.SSHClient
        self.sftp_client: paramiko.SFTPClient
        atexit.register(self.cleanup)
        return None

    def set_password(self) -> str:
        """Sets user password. The password is not echoed.

        Returns:
            password (str): password of the user
        """
        password = getpass.getpass(
            f"password for {self.username}@{self.hostname}: "
        )
        return password

    def set_ssh_client(self) -> paramiko.SSHClient:
        """Creates an SSH client and connects to remote system.

        Returns:
            ssh_client (paramiko.SSHClient): ssh client
        """
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        return ssh_client

    def connect_remote(self) -> None:
        """Creates an ssh and sftp clients, prompts for user password and connects to the remote host.

        Returns:
            None
        """
        self.ssh_client = self.set_ssh_client()
        self.password = self.set_password()
        self.ssh_client.connect(
            hostname=self.hostname,
            port=self.port,
            username=self.username,
            password=self.password,
        )
        self.sftp_client = self.ssh_client.open_sftp()
        return None

    def create_remote_folder(self, remote_folder: str) -> None:
        """Create a folder in the remote system.

        Args:
            remote_folder (str): path of the folder to be created on the remote system.

        Returns:
            None
        """
        try:
            self.sftp_client.mkdir(remote_folder)
        except IOError:
            print(f"(assuming {remote_folder}/ already exists)")
        return None

    def get_files(self, remote_folder: str, local_folder: str = "./") -> None:
        """Get files from the remote system.

        Args:
            remote_folder (str): path of the remote folder to copy the files from.
            local_folder (str, optional): path of the host folder to copy the files to. Defaults to "./".

        Returns:
            None
        """
        if not os.path.exists(local_folder):
            os.mkdir(local_folder)

        for entry in self.sftp_client.listdir_attr(remote_folder):
            remote_path = remote_folder + "/" + entry.filename
            local_path = os.path.join(local_folder, entry.filename)
            mode = entry.st_mode
            if mode is None:
                # TODO: throw an exception here
                print("Path type is None")
            else:
                if S_ISDIR(mode):
                    try:
                        os.mkdir(local_path)
                    except OSError:
                        pass
                    self.get_files(remote_path, local_path)
                elif S_ISREG(mode):
                    self.sftp_client.get(remote_path, local_path)
                else:
                    # TODO: throw an exception here
                    print("Unknown type encountered when running get_files method")
        return None

    def put_files(
        self,
        remote_folder: str = "~",
        local_folder: str = "./",
        verbose: bool = False,
    ) -> None:
        """Copy files to the remote system.

        Args:
            remote_folder (str): path on a remote system to copy the files to.
            local_folder (str): path to copy the files from.
            verbose (bool): show verbose info when copying.

        Returns:
            None
        """
        if remote_folder == "~":
            remote_folder = os.path.expanduser("~")

        local_folder_dirname = os.path.dirname(local_folder)
        local_folder_basename = os.path.basename(local_folder)

        if verbose:
            print(f"local_folder_dirname: {local_folder_dirname}")
            print(f"local_folder_basename: {local_folder_basename}")

        for dirpath, dirnames, filenames in os.walk(local_folder):
            file_dirpath = dirpath[len(local_folder) + 1:]
            remote_path = os.path.join(
                remote_folder, local_folder_basename, file_dirpath
            )
            if verbose:
                print("\n" + "-" * 20 + "\n")
                print(f"dirpath: {dirpath}")
                print(f"dirnames: {dirnames}")
                print(f"remote_path: {remote_path}")
                print(f"file_dirpath: {file_dirpath}")

            try:
                self.sftp_client.listdir(remote_path)
            except IOError:
                self.sftp_client.mkdir(remote_path)

            for filename in filenames:
                from_path = os.path.join(dirpath, filename)
                to_path = os.path.join(remote_path, filename)
                self.sftp_client.put(from_path, to_path)
                if verbose:
                    print(
                        f"\ncopying: {filename}\n  from: {from_path}\n  to: {to_path}"
                    )
        return None

    def submit_job(self, job_file: str, verbose: bool = False) -> Tuple[int, str, str, str]:
        """Submit job to SLURM cluster.

        Args:
            job_file (str): full path of the job script to be submitted.
            verbose (bool): run in verbose mode.

        Returns:
            tuple(int, str, str, str): job_id, stdin, stdout, stderr
        """
        stdin, stdout, stderr = self.ssh_client.exec_command(
            f"sbatch {job_file}"
        )
        job_id = int(stdout.read().decode().split()[-1])
        if verbose:
            print(f"Submitted job with id: {job_id}")
        return (job_id, stdin.read().decode(), stdout.read().decode(), stderr.read().decode())

    def build_apptainer_image(self, docker_image: str, sif_file_name: str = 'app.sif') -> bool:
        """Builds an Apptainer image from a Docker image.

        Args:
            docker_image (str): docker image name to be used to build an apptainer image.
            sif_file_name (str, optional): name of the apptainer image (sif) to be built. Defaults to 'app.sif'.

        Returns:
            bool: True if the apptainer image was successfully built. Otherwise, returns False.
        """
        build_command = f"apptainer pull {sif_file_name} docker://{docker_image}"

        process = subprocess.Popen(build_command, shell=True)
        process.wait()

        # TODO: handle process status mor carefully: what happens if the file exists?
        if os.path.isfile(sif_file_name):
            print(f"Generated {sif_file_name}")
            # print(process.stdout)
            return True
        else:
            print("Image generation has failed.")
            print(process.stderr)
            return False

    def install_apptainer_on_remote(self, install_path: str = "~") -> bool:
        """Installs Apptainer on a remote system in unprivileged mode.

        Args:
            install_path (str): path to install apptainer binary.

        Returns:
            bool: True if the apptainer installation was successful. Otherwise, returns False.
        """
        if install_path == "~":
            install_path = os.path.expanduser("~")

        print(f"installing apptainer at {install_path}")

        install_script_url = "https://raw.githubusercontent.com/apptainer/apptainer/main/tools/install-unprivileged.sh"
        exe_path = f"{install_path}/bin/apptainer"

        install_command = f"curl -s {install_script_url} | bash -s - {install_path}"
        # print(f"running: {install_command}")
        _, _, stderr_install = self.run_remote_command(
            command=install_command, timeout=30, flush=False, show_stdout=True)

        check_install_command = f"file {exe_path}"
        # print(f"running: {check_install_command}")
        _, _, stderr_check = self.run_remote_command(
            command=check_install_command, timeout=30, flush=False, show_stdout=True)

        # TODO: add the exectable to $PATH and check the executable on the remote system: command -v apptainer
        if stderr_install == "" or stderr_check == "":
            print(f"Installed at {exe_path}")
            return True
        else:
            print("Apptainer installation has failed.")
            print(f"installation error: {stderr_install}")
            print(f"installation check error:{stderr_check}")
            return False

    def check_local_command_exists(self, command: str) -> bool:
        """Check whether `command` is on PATH and marked as executable.

        Args:
            command (str): a command to be checked.

        Returns:
            bool: True if command exists. Otherwise False.

        Examples:
            >>> from kunefe import Kunefe
            >>> kunefe = Kunefe(username="xenon", hostname="localhost", port=10022)
            >>> kunefe.check_local_command_exists(command='ls')
            True
            >>> kunefe.check_local_command_exists(command='thisdoesnotexist')
            False
        """
        return which(command) is not None

    def check_required_tools(self, command_list: list[str]) -> bool:
        """Check whether all required commands are available.

        Args:
            command_list (list[str]): a list of tools to be checked.

        Returns:
            bool: True if all the tools exist. Otherwise False.

        Examples:
            >>> from kunefe import Kunefe
            >>> kunefe = Kunefe(username="xenon", hostname="localhost", port=10022)
            >>> kunefe.check_required_tools(['ls', 'rsync', 'cp'])
            True
            >>> kunefe.check_required_tools(['docker', 'rsync', 'bsxcommand'])
            False
        """
        # TODO: also check the required versions
        if all(self.check_local_command_exists(command) for command in command_list):
            return True
        else:
            return False

    def generate_job_script(
        self,
        job_name: str,
        sif_file_path: str,
        command: str,
        env_vars: str,
        job_time: str,
        job_file_path: str = './',
        template_name: str = 'generic'
    ) -> None:
        """Generate a batch script file for job submission.

        Args:
            job_name (str): name of the job to be used when submitting.
            sif_file_path (str): path of the Apptainer image.
            command (str): a command to be executed using Apptainer image.
            env_vars (str): environment variables to be used when submitting the job.
            job_time (str): time limit for the job.
            job_file_path (str, optional): path to save the generated batch job script. Defaults to './'.
            template_name (str, optional): name of the template to be used. Defaults to 'generic'.

        Returns:
            None
        """
        parent_dir = os.path.dirname(__file__)
        templates_folder = os.path.join(parent_dir, "templates")
        environment = jinja2.Environment(
            loader=jinja2.FileSystemLoader(templates_folder)
        )
        template = environment.get_template(f"{template_name}_job.jinja")

        filename = f"{job_file_path}/{job_name}.sh"
        content = template.render(
            job_name=job_name,
            sif_file_path=sif_file_path,
            job_time=job_time,
            command=command,
            env_vars=env_vars
        )

        with open(filename, mode="w", encoding="utf-8") as message:
            message.write(content)
            print(f"Batch job file was saved as {filename}")
        return None

    def run_remote_command(
        self, command: str, timeout: int = 5, flush: bool = False, show_stdout: bool = False
    ) -> list[str]:
        """Run a command on a remote system.

        Args:
            command (str): command to be executed on the remote system.
            timeout (int, optional): time to wait before considering the command as failed. Defaults to 5.
            flush (bool, optional): flush the output. Defaults to False.
            show_stdout (bool, optional): prints the stdout. Defaults to False.

        Returns:
            list[str]: stdin, stdout, stderr
        """
        self.ssh_client.invoke_shell()
        stdin, stdout, stderr = self.ssh_client.exec_command(
            command=command,
            timeout=timeout
        )

        if show_stdout:
            stdout_lines = stdout.readlines()
            for line in stdout_lines:
                if flush:
                    print(line, end="", flush=True)
                else:
                    print(line, end="")

            # https://stackoverflow.com/a/11474509
            if flush:
                sys.stdout.write(
                    "\033[F" * len(stdout_lines)
                )  # Cursor up for X number of lines

        return [stdin.read().decode('ascii') if stdin.readable() else '',
                stdout.read().decode('ascii') if stdout.readable() else '',
                stderr.read().decode('ascii') if stderr.readable() else '']

    def watch_slurm_queue(self, sleep_time: float = 5.0) -> None:  # pragma: no cover
        """Watches the SLURM job queue.

        Args:
            sleep_time (float, optional): time to wait before refreshing the queue status. Defaults to 5.0.

        Returns:
            None
        """
        command = 'squeue --all'
        while True:
            _, _, stderr = self.run_remote_command(command=command, timeout=5, flush=True, show_stdout=True)
            if stderr != '':
                break
            time.sleep(sleep_time)
        return None

    def cleanup(self) -> None:  # pragma: no cover
        """Destructor method to clean things up.

        Returns:
            None
        """
        print("Running cleanup...")
        return None
