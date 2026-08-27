"""

Contain wrapper classes used to execute different linux tools.
- AddessChecker
- PortChecker
- Rsync

  NOTE: Internet netcat and ping has to be installed.
"""

import os
import time
import logging
from subprocess import Popen


class AddressChecker:
    """ This class is supposed to be used when determining if a
        address is accessible via the network, using ping.
    """
    def __init__(self, address, verbose=False):
        """
        :param address: network address that will be checked, ex 192.168.0.1
        :param verbose: turn on the verbose flag for ping
        """
        self.address = address
        self.logger = logging.getLogger(self.__class__.__name__)
        self.verbose = verbose
        self.logger.debug("creating instance")

    def __generate_ping_command(self):
        """
        Function used to generate a ping command, should not be used directly.
        :return: the command that will be executed

        >>> AddressChecker("127.0.0.1")._AddressChecker__generate_ping_command()
        'ping -W 5 -c 1 127.0.0.1 > /dev/null'
        >>> AddressChecker("127.0.0.1", True)._AddressChecker__generate_ping_command()
        'ping -W 5 -c 1 -v 127.0.0.1 > /dev/null'
        """
        verbose = " "
        if self.verbose:
            verbose = " -v "
        command = "ping -W 5 -c 1" + verbose + self.address + " > /dev/null"
        self.logger.debug("creating command: " + command)
        return command

    def execute(self):
        """
        Function that will execute the generated command, if the address isn't
        accessible an Error will be thrown (i.e if return value of command isn't 0)
        :return: return value of the command, will always be 1

        Needs a live network, so these are documentation rather than executed tests:

        >>> AddressChecker("127.0.0.1").execute()  # doctest: +SKIP
        0
        >>> AddressChecker("10.10.10.10").execute()  # doctest: +SKIP
        Traceback (most recent call last):
         ...
        ductus.tools.wrappers.AddressException
        """
        command = self.__generate_ping_command()
        self.logger.info("checking access to %s", self.address)
        result = os.system(command)
        if result != 0:
            self.logger.error("unable to access address " + self.address)
            raise AddressException()
        return result


class PortChecker:
    """ This class is supposed to be used when determining if a
        network port is open, using nc.
    """
    def __init__(self, address, port, verbose=False, timeout=5, repeat=5):
        """
        :param address: network address, ex 192.168.0.1
        :param port: network port that will be checked
        :param verbose: turn on verbose flag for nc
        :param timeout: number of seconds nc should wait, before canceling the command.
        :param repeat: number of times that the command should be repeated, if it's not successful.
        """
        self.address = address
        self.port = port
        self.timeout = timeout
        self.repeat = repeat
        self.verbose = verbose
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug("creating instance")

    def __generate_port_check_command(self):
        """
        Function used to generate a nc command, should not be used directly.
        :return: the command that will be executed

        Note that timeout and repeat affect execute(), not the generated command:

        >>> PortChecker("127.0.0.1", 8080)._PortChecker__generate_port_check_command()
        "echo 'QUIT' | nc 127.0.0.1 8080"
        >>> PortChecker("127.0.0.1", 8080, False, 10, 15)._PortChecker__generate_port_check_command()
        "echo 'QUIT' | nc 127.0.0.1 8080"
        >>> PortChecker("127.0.0.1", 8080, True, 10, 15)._PortChecker__generate_port_check_command()
        "echo 'QUIT' | nc -v 127.0.0.1 8080"
        """
        verbose = " "
        if self.verbose:
            verbose = " -v "
        command = "echo 'QUIT' | nc" + verbose + self.address + " " + str(self.port)
        self.logger.debug("creating command: " + command)
        return command

    def execute(self, testing=False):
        """ Function that will execute the generated nc command, if the port isn't
            accessible an error will be thrown (i.e if return value of command isn't 0)

            the port check command will be repeated self.repeat number of times, if
            execution isn't successful. The execution will wait for at most self.timeout
            seconds before determining that the execution failed.
            :return: return value of the command, will always be 1

            Needs a live listener, so these are documentation rather than executed tests:

            >>> PortChecker("127.0.0.1", 8080).execute()  # doctest: +SKIP
            0
            >>> PortChecker("127.0.0.1", 8081, False, 0, 0).execute()  # doctest: +SKIP
            Traceback (most recent call last):
             ...
            ductus.tools.wrappers.PortInaccessibleException
        """
        command = self.__generate_port_check_command()
        counter = self.repeat
        result = None
        # Repeat loop until port has been accessed or until self.repeat number of attempts have
        # been performed.
        while True:
            self.logger.info("checking access to %s:%s, attempt %s", self.address, self.port, self.repeat - counter)
            proc = None
            if self.verbose:
                proc = Popen(command, shell=True)
            else:
                # Pipe the stdout and stderr to /dev/null if verbose haven't been set.
                proc = Popen(command, shell=True, stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))
            # Perform command until timeout setting is met.
            timeout_counter = self.timeout
            while result is None:
                time.sleep(1)  # Sleep for one second
                result = proc.poll()
                timeout_counter -= 1
                if timeout_counter < 0:
                    break
            # Validate if port has been accessed
            if result is None or result != 0:
                counter -= 1
                if counter < 0:
                    self.logger.error("port %s at address %s isn't accessible!", self.port, self.address)
                    raise PortInaccessibleException()
                self.logger.info("Unable to access port %s at address %s, sleeping for 10 seconds %s",
                                 self.port, self.address, result)
                time.sleep(10)
            else:
                break
        return result


class Rsync:
    FROM_IS_REMOTE = 1
    TO_IS_REMOTE = 2

    def __init__(self, from_path, to_path, remote_address=None, user=None, from_is_remote=1, repeat=1, identity_file=None,
                 checksum_validate=False, preserve_permissions=True, verbose=False, ignore_ping=False, local_sync=False,
                 timeout=0):
        """ :param from_path: where data should be transferred from
            :param to_path: where data should be transferred to
            :param remote_address: server address that should be used
            :param user: user that will perform the transfer
            :param from_is_remote: 1 if "from" is located on a other server, 2 if "to" is located on a other server, default 1
            :param repeat: how many times the rsync command should be repeated, it it fails
            :param identity_file: identity file that will be used
            :param checksum_validate: perform checksum validation of transferred files
            :param preserve_permissions: preserve ownership and permission of transferred files.
            :param verbose: run rsync with verbose
            :param ignore_ping: don't check if address is accessible
            :param local_sync: perform sync between folders on the same local computer
            :param timeout: timeout used to detect stalled sync

            >>> Rsync("/home/test", "/home/test2")
            Traceback (most recent call last):
             ...
            ductus.tools.wrappers.IncorrectInputException
            >>> Rsync("/home/test", "/home/test2", "127.0.0.1", local_sync=True)
            Traceback (most recent call last):
             ...
            ductus.tools.wrappers.IncorrectInputException
        """
        self.to_path = to_path
        self.from_path = from_path
        self.remote_address = remote_address
        self.user = user
        self.identity_file = identity_file
        self.from_is_remote = from_is_remote
        self.checksum_validate = checksum_validate
        self.repeat = repeat
        self.preserve_permissions = preserve_permissions
        self.verbose = verbose
        self.logger = logging.getLogger(self.__class__.__name__)
        self.ignore_ping = ignore_ping
        self.local_sync = local_sync
        self.timeout = timeout
        if not self.local_sync and remote_address is None:
            self.logger.error("Sync between host cannot be performed without a remote address!")
            raise IncorrectInputException
        if self.local_sync and remote_address is not None:
            self.logger.error("Remote address and local_sync cannot both be set")
            raise IncorrectInputException
        self.logger.debug("creating instance")

    def __get_from_path(self):
        """ Function used to generate a path where data will be synced from
            :return: from path

            from_is_remote defaults to FROM_IS_REMOTE, so the remote address is prefixed:

            >>> Rsync("/home/test", "/home/test2", local_sync=True)._Rsync__get_from_path()
            '/home/test'
            >>> Rsync("/home/test", "/home/test2", "127.0.0.1")._Rsync__get_from_path()
            '127.0.0.1:/home/test'
            >>> Rsync("/home/test", "/home/test2", "127.0.0.1", "test",
            ...       Rsync.TO_IS_REMOTE)._Rsync__get_from_path()
            '/home/test'
        """
        command = ""
        if not self.local_sync:
            if self.from_is_remote == Rsync.FROM_IS_REMOTE:
                if self.user:
                    command += self.user + "@" + self.remote_address + ":"
                else:
                    command += self.remote_address + ":"
        return command + self.from_path

    def __get_to_path(self):
        """ Function used to generate a path where data will be synced to
            :return: to path

            >>> Rsync("/home/test", "/home/test2", local_sync=True)._Rsync__get_to_path()
            '/home/test2'
            >>> Rsync("/home/test", "/home/test2", "127.0.0.1")._Rsync__get_to_path()
            '/home/test2'
            >>> Rsync("/home/test", "/home/test2", "127.0.0.1", "test",
            ...       Rsync.TO_IS_REMOTE)._Rsync__get_to_path()
            'test@127.0.0.1:/home/test2'
        """
        command = ""
        if not self.local_sync:
            if self.from_is_remote == Rsync.TO_IS_REMOTE:
                if self.user:
                    command += self.user + "@" + self.remote_address + ":"
                else:
                    command += self.remote_address + ":"
        return command + self.to_path

    def __create_sync_command(self):
        """ Function used to generate a rsync command, should not be used directly.
            :return: the command that will be executed

            >>> Rsync("/home/test", "/home/test2", local_sync=True)._Rsync__create_sync_command()
            'rsync -zPa /home/test /home/test2 --timeout=0'

            preserve_permissions swaps the archive flag for a plain recursive one, and
            timeout is passed through to rsync:

            >>> Rsync("/home/test", "/home/test2", local_sync=True,
            ...       preserve_permissions=False)._Rsync__create_sync_command()
            'rsync -zPr /home/test /home/test2 --timeout=0'
            >>> Rsync("/home/test", "/home/test2", local_sync=True,
            ...       timeout=1200)._Rsync__create_sync_command()
            'rsync -zPa /home/test /home/test2 --timeout=1200'

            A remote sync wraps ssh, and checksum_validate/verbose add flags:

            >>> Rsync("/home/test", "/home/test2",
            ...       "127.0.0.1")._Rsync__create_sync_command()  # doctest: +NORMALIZE_WHITESPACE
            'rsync -e "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"
             -zPa 127.0.0.1:/home/test /home/test2 --timeout=0'
            >>> Rsync("/home/test", "/home/test2", "127.0.0.1", "test", Rsync.TO_IS_REMOTE, 2,
            ...       "identity_test", True, True,
            ...       True)._Rsync__create_sync_command()  # doctest: +NORMALIZE_WHITESPACE
            'rsync -e "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i identity_test"
             -zPcva /home/test test@127.0.0.1:/home/test2 --timeout=0'
        """
        command = 'rsync'
        flags = " -zP"
        if not self.local_sync:
            if self.identity_file:
                command += ' -e "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i ' + self.identity_file + '"'
            else:
                command += ' -e "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"'
        if self.checksum_validate:
            flags += "c"
        if self.verbose:
            flags += "v"
        if self.preserve_permissions:
            flags += "a"
        else:
            flags += "r"
        command += flags + " " + self.__get_from_path() + " " + self.__get_to_path() + " --timeout=" + str(self.timeout)
        self.logger.debug("creating command: '" + command + "'")
        return command

    def __create_ssh_access_command(self):
        """ Function used to generate a ssh test command, should not be used directly.
            :return: the command that will be executed

            Only called for remote syncs, execute() skips it when local_sync is set:

            >>> Rsync("/home/test", "/home/test2", "127.0.0.1")._Rsync__create_ssh_access_command()
            'ssh -oBatchMode=yes 127.0.0.1 exit 0 > /dev/null'
            >>> Rsync("/home/test", "/home/test2", "127.0.0.1", "test", Rsync.TO_IS_REMOTE, 2,
            ...       "identity_test", True, True, True)._Rsync__create_ssh_access_command()
            'ssh -oBatchMode=yes -v -i identity_test test@127.0.0.1 exit 0 > /dev/null'
        """
        command = "ssh -oBatchMode=yes"
        if self.verbose:
            command += " -v"
        if self.identity_file:
            command += " -i " + self.identity_file
        if self.user:
            command += " " + self.user + "@" + self.remote_address
        else:
            command += " " + self.remote_address
        command += " exit 0 > /dev/null"
        self.logger.debug("creating command: " + command)
        return command

    def execute(self):
        """ Function that will execute the generated rsync command.

            the rsync check command will be repeated self.repeat number of times, if
            execution isn't successful.
            :return: return value of the command
        """
        if not self.local_sync and not self.ignore_ping:
            # Validate that the provided address is accessible
            ping = AddressChecker(self.remote_address, self.verbose)
            ping.execute()
        if not self.local_sync:
            # Validate that the 22 is open
            port_checker = PortChecker(self.remote_address, 22, self.verbose)
            port_checker.execute()
            # Test if a ssh connection can be established
            self.logger.debug("checking ssh access")
            if os.system(self.__create_ssh_access_command()) != 0:
                self.logger.error("unable to access server using ssh key, it may be password protected.")
                raise SshAccessException()

        command = self.__create_sync_command()
        result = None
        # Repeat the rsync comamand self.repeat number of times, if it fails.
        counter = self.repeat
        while True:
            self.logger.info("rsyncing data from %s to %s, attempt %s", self.__get_from_path(), self.__get_to_path(),
                             (self.repeat - counter))
            result = os.system(command)
            # Break if the sync exited with 0, i.e successfully. Else retry until success or until
            # the command has been repeat self.repeat number of times.
            if result != 0:
                if counter == 0:
                    self.logger.error("Unable to sync data, error code: %s", os.WEXITSTATUS(result))
                    raise RsyncException()
                else:
                    self.logger.info("Rsync failed with exit code: %s", os.WEXITSTATUS(result))
            else:
                break
            counter -= 1
            self.logger.info("Unable to sync data from %s to %s, sleeping for 60 seconds",
                             self.__get_from_path(), self.__get_to_path())
            time.sleep(60)
        return result


class PortInaccessibleException(Exception):
    """ Exception thrown when a port can't be accessed. """
    pass


class SshAccessException(Exception):
    """ Exception thrown when ssh access can't be established. """
    pass


class AddressException(Exception):
    """ Exception thrown when address isn't accessible via the network. """
    pass


class RsyncException(Exception):
    """ Exception thrown when rsync transfer cannot be performed. """
    pass


class IncorrectInputException(Exception):
    """ Exception thrown when incorrect input has been provided. """
    pass
