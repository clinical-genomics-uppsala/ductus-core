import os
import sys
import time
import logging

class AddressChecker:
    def __init__(self, address, verbose=False):
        self.address = address
        self.logger = logging.getLogger(self.__class__.__name__)
        self.verbose = verbose
        self.logger.debug("creating instance")

    def __generate_ping_command(self):
        verbose = " "
        if self.verbose:
            verbose = " -v "
        command = "ping -W 5 -c 1" + verbose + self.address + " > /dev/null"
        self.logger.debug("creating command: " + command)
        return command

    def execute(self):
        command = self.__generate_ping_command()
        self.logger.info("checking access to %s", self.address)
        result = os.system(command)
        if result != 0:
            self.logger.error("unable to access address " + self.address)
            raise AddressException()
        return result

class PortChecker:
    def __init__(self, address, port, verbose=False, timeout=5, repeat=5):
        self.address = address
        self.port = port
        self.timeout = timeout
        self.repeat = repeat
        self.verbose = verbose
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug("creating instance")

    def __generate_port_check_command(self):
        verbose_flag = " "
        if self.verbose:
            verbose_flag = " -v"
        command = "echo 'QUIT' | nc -w " + str(self.timeout) + verbose_flag + self.address + " " + str(self.port) + " > /dev/null"
        self.logger.debug("creating command: " + command)
        return command

    def execute(self):
        command = self.__generate_port_check_command()
        counter = self.repeat
        result = None
        while True:
            self.logger.info("checking access to %s:%s, attempt %s", self.address, self.port, self.repeat - counter)
            result = os.system(command)
            if result != 0:
                counter -= 1
                if counter < 0:
                    self.logger.error("port %s at address %s isn't accessible!", self.port, self.address)
                    raise PortInaccessibleException()
                self.logger.info("Unable to access port %s at address %s, sleeping for 10 seconds", self.port,
                                 self.address)
                time.sleep(10)
            else:
                break
        return result

class Rsync:
    PULL = 1
    PUSH = 2

    def __init__(self, from_path, to_path, remote_address, user=None, push_or_pull=1, repeat=1, identity_file=None,
                 checksum_validate=False, preserve_permissions=True, verbose=False, ignore_ping=False):
        self.to_path = to_path
        self.from_path = from_path
        self.remote_address = remote_address
        self.user = user
        self.identity_file = identity_file
        self.push_or_pull = push_or_pull
        self.checksum_validate = checksum_validate
        self.repeat = repeat
        self.preserve_permissions = preserve_permissions
        self.verbose = verbose
        self.logger = logging.getLogger(self.__class__.__name__)
        self.ignore_ping = ignore_ping
        self.logger.debug("creating instance")

    def __get_from_path(self):
        command = ""
        if self.push_or_pull == Rsync.PULL:
            if self.user:
                command += self.user + "@" + self.remote_address + ":"
            else:
                command += self.remote_address + ":"
        return command + self.from_path

    def __get_to_path(self):
        command = ""
        if self.push_or_pull == Rsync.PUSH:
            if self.user:
                command += self.user + "@" + self.remote_address + ":"
            else:
                command += self.remote_address + ":"
        return command + self.to_path

    def __create_sync_command(self):
        command = 'rsync'
        flags = " -zP"
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
        command += flags + " " + self.__get_from_path() + " " + self.__get_to_path()
        self.logger.debug("creating command: '" + command + "'")
        return command

    def __create_ssh_access_command(self):
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
        if not self.ignore_ping:
            ping = AddressChecker(self.remote_address, self.verbose)
            ping.execute()
        port_checker = PortChecker(self.remote_address, 22, self.verbose)
        port_checker.execute()

        self.logger.debug("checking ssh access")
        if os.system(self.__create_ssh_access_command()) != 0:
            self.logger.error("unable to access server using ssh key, it may be password protected.")
            raise SshAccessException()

        command = self.__create_sync_command()
        result = None
        counter = self.repeat
        while True:
            self.logger.info("rsyncing data from %s to %s, attempt %s", self.__get_from_path(), self.__get_to_path(),
                             (self.repeat - counter))
            result = os.system(command)
            if result != 0:
                if counter == 0:
                    self.logger.error("Unable to sync data, error code: %s", os.WEXITSTATUS(result))
                    raise RsyncException()
            else:
                break
            counter -= 1
            self.logger.info("Unable to sync data from %s to %s, sleeping for 60 seconds", self.__get_from_path(),
                             self.__get_to_path())
            time.sleep(5)
            port_checker.execute()
        return result

class PortInaccessibleException(Exception):
    pass

class SshAccessException(Exception):
    pass

class AddressException(Exception):
    pass

class RsyncException(Exception):
    pass