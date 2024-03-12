"""Documentation about the kunefe module.

Returns:
    _type_: _description_
"""

import atexit
import getpass
import os
import subprocess
import time
from shutil import which
from stat import S_ISDIR
from stat import S_ISREG
import jinja2
import paramiko

# setup logging
DEFAULT_LOG_FILENAME = "kunefe.log"
paramiko.util.log_to_file(DEFAULT_LOG_FILENAME)


class Kunefe:
    """Submit jobs to SLURM cluster.

    Args:
        username:
        hostname:
        port:

    Attributes:
        username (str):
        hostname (str):
        port (int):
    """

    def __init__(self, username: str, hostname: str, port: int) -> None:
        """_summary_.

        Args:
            username (str): _description_
            hostname (str): _description_
            port (int): _description_
        """
        self.username = username
        self.hostname = hostname
        self.port = port
        self.password = None
        self.transport = None
        self.ssh_client = None
        self.sftp_client = None
        atexit.register(self.cleanup)

    def set_password(self) -> str:
        """Sets user password."""
        password = getpass.getpass(
            f"password for {self.username}@{self.hostname}: "
        )
        return password

    def set_transport(self) -> paramiko.Transport:
        """Creates an paramiko transport."""
        transport = paramiko.Transport((self.hostname, self.port))
        return transport

    def set_ssh_client(self) -> paramiko.SSHClient:
        """Creates an SSH client and connects to remote server."""
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        return ssh_client

    def set_clients(self) -> None:
        """Set the ssh and sftp clients."""
        # self.transport = self.set_transport()
        self.ssh_client = self.set_ssh_client()

    def connect_remote(self) -> None:
        """Connect to the remote host."""
        self.set_clients()
        self.password = self.set_password()
        self.ssh_client.connect(
            hostname=self.hostname,
            port=self.port,
            username=self.username,
            password=self.password,
        )
        self.sftp_client = self.ssh_client.open_sftp()

    def create_remote_folder(self, remote_folder: str) -> None:
        """Create a folder in the remote server.

        Args:
            remote_folder (str): _description_
        """
        try:
            self.sftp_client.mkdir(remote_folder)
        except IOError:
            print(f"(assuming {remote_folder}/ already exists)")

    def get_files(self, remote_folder: str, local_folder: str = "./") -> None:
        """Get files from the remote server.

        Args:
            remote_folder (str): _description_
            local_folder (str, optional): _description_. Defaults to "./".
        """
        if not os.path.exists(local_folder):
            os.mkdir(local_folder)

        for entry in self.sftp_client.listdir_attr(remote_folder):
            remote_path = remote_folder + "/" + entry.filename
            local_path = os.path.join(local_folder, entry.filename)
            mode = entry.st_mode
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

    def put_files(
        self,
        remote_folder: str = "~",
        local_folder: str = "./",
        verbose: bool = False,
    ) -> None:
        """Copy files to the remote server.

        Args:
            remote_folder (str): Path on a remote system to copy the files or folders
            local_folder (str): File or a folder name to copy
            verbose (bool):Show verbose info.

        Returns:
            None

        Raises:
            TODO: ValueError: If `name` is equal to `nobody`

        Example:
            This function can be called with `Jane Smith` as argument using

            # >>> from kunefe.my_module import kunefe
            # >>> put_files(remote_folder="/home/xenon/", local_folder="./test_folder")
        """
        if remote_folder == "~":
            remote_folder = os.path.expanduser("~")

        local_folder_dirname = os.path.dirname(local_folder)
        local_folder_basename = os.path.basename(local_folder)

        if verbose:
            print(f"local_folder_dirname: {local_folder_dirname}")
            print(f"local_folder_basename: {local_folder_basename}")

        for dirpath, dirnames, filenames in os.walk(local_folder):
            file_dirpath = dirpath[len(local_folder) + 1 :]
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

    def submit_job(self, job_file: str) -> None:
        """Submit job to SLURM cluster.

        Args:
            job_file (str): _description_

        Returns:
            _type_: _description_
        """
        stdin, stdout, stderr = self.ssh_client.exec_command(
            f"sbatch {job_file}"
        )
        job_id = int(stdout.read().decode().split()[-1])
        print(f"Submitted job with id: {job_id}")
        return job_id, stdin, stdout, stderr

    def build_apptainer_image(self, docker_image: str, sif_file_name: str = 'app.sif') -> bool:
        """Builds an apptainer image from a Docker image.

        Args:
            docker_image (str): _description_
            sif_file_name (str, optional): _description_. Defaults to 'app.sif'.

        Returns:
            bool: _description_
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

    def check_local_command_exists(self, command: str) -> bool:
        """Check whether `command` is on PATH and marked as executable.

        Args:
            command (str): _description_

        Returns:
            bool: _description_
        """
        return which(command) is not None

    def check_required_tools(self, command_list: list[str]) -> bool:
        """Check whether all required commands are available.

        Args:
            command_list (list[str]): _description_

        Returns:
            bool: _description_
        """
        # TODO: also check the required versions
        if all(self.check_local_command_exists(command) for command in command_list):
            print("Have all the required external tools.")
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
        """Generate batch script file for job submission.

        Args:
            job_name (str): _description_
            sif_file_path (str): _description_
            command (str): _description_
            env_vars (str): _description_
            job_time (str): _description_
            job_file_path (str, optional): _description_. Defaults to './'.
            template_name (str, optional): _description_. Defaults to 'generic'.
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

    def run_remote_command(
        self, command: str, timeout: int = 5, flush: bool = False
    ) -> None:
        """Run a command on a remote system.

        Args:
            command (str): _description_
            timeout (int, optional): _description_. Defaults to 5.
            flush (bool, optional): _description_. Defaults to False.

        Returns:
            _type_: _description_
        """
        # transport = self.ssh_client.get_transport()
        # channel = transport.open_session()
        # channel.get_pty()
        # channel.settimeout(timeout)
        # channel.set_combine_stderr(True)
        # stdout = channel.makefile()
        self.ssh_client.invoke_shell()
        stdin, stdout, stderr = self.ssh_client.exec_command(
            command=command,
            timeout=timeout
        )

        # stdout_lines = stdout.readlines()
        # for line in stdout_lines:
        #     if flush:
        #         print(line, end="", flush=True)
        #     else:
        #         print(line, end="")

        # # https://stackoverflow.com/a/11474509
        # if flush:
        #     sys.stdout.write(
        #         "\033[F" * len(stdout_lines)
        #     )  # Cursor up for X number of lines

        # stdout_string = stdout.read().decode('ascii').strip("\n")

        return [stdin.read().decode('ascii') if stdin.readable() else '',
                stdout.read().decode('ascii') if stdout.readable() else '',
                stderr.read().decode('ascii') if stderr.readable() else '']

    def watch_slurm_queue(self, sleep_time: float = 5.0) -> None:  # pragma: no cover
        """Watches the SLURM job queue.

        Args:
            sleep_time (float, optional): _description_. Defaults to 5.0.
        """
        command = 'squeue --all'
        while True:
            self.run_remote_command(command=command, timeout=5, flush=True)
            time.sleep(sleep_time)

    def cleanup(self) -> None:  # pragma: no cover
        """Destructor method to clean things up."""
        print("Running cleanup...")
