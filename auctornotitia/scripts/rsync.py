import sys
import logging

from optparse import OptionParser

from auctornotitia.tools.wrappers import Rsync
from auctornotitia.tools.wrappers import AddressException, PortInaccessibleException, SshAccessException, RsyncException

parser = OptionParser()
parser.add_option("-f", "--from_path", dest="from_path",
                  help="Path to the folder/files that will be moved.")
parser.add_option("-t", "--to_path", dest="to_path",
                  help="Path to where folder/files that will be moved.")
parser.add_option("-r", "--remote_address", dest="remote_address",
                  help="The ip address to the remote host from where data will be pulled from or sent to.")
parser.add_option("-u", "--user", dest="user",
                  help="he user name that will be used to move data, not required if the executing user is the one that will move the data.")
parser.add_option("-p", "--push_or_pull", dest="push_or_pull",
                  help="Default is to pull data, this can be setting push_or_pull to 2.", default="1")
parser.add_option("-i", "--identity_file", dest="identity_file",
                  help="Path to the location of the identity_file that will be used to authenticate the user.")
parser.add_option("-c", "--checksum_validate", dest="checksum_validate",
                  help="Rsync command will use checksum to validate transfered files when this parameters is set to true.")
parser.add_option("-P", "--preserve_permissions", dest="preserve_permissions",
                  help="Rsync command will preserve permissions and ownership.")
parser.add_option("-R", "--repeat", dest="repeat",
                  help="Number of times rsync command should be repeated, when it fails, default is 10 and -1 is forever.",default=10)

(options, args) = parser.parse_args()

if options.from_path is None:
    parser.error("Missing argument from_path")
if options.to_path is None:
    parser.error("Missing argument to_path")
if options.remote_address is None:
    parser.error("Missing argument remote_address")
if options.user is None:
    parser.error("Missing argument user")
if options.identity_file is None:
    parser.error("Missing argument identity_file")

print(options.from_path,
      options.to_path,
      options.remote_address,
      options.user,
      int(options.push_or_pull),
      int(options.repeat),
      options.identity_file,
      not options.checksum_validate is None,
      not options.preserve_permissions is None)
try:
    rsync=Rsync(
      options.from_path,
      options.to_path,
      options.remote_address,
      options.user,
      int(options.push_or_pull),
      int(options.repeat),
      options.identity_file,
      not options.checksum_validate is None,
      not options.preserve_permissions is None)
    rsync.execute()
except AddressException as err:
    logging.error("Access error, can't reach the provided address: %s", options.remote_address)
    sys.exit(1)
except PortInaccessibleException as err:
    logging.error("Port access error, can't access port %s at address %s", 22, options.remote_address)
    sys.exit(2)
except SshAccessException as err:
    logging.error("Unable login at %s using with ssh, user %s and identity_file %s",options.remote_address, options.user, options.identity_file)
    sys.exit(3)
except RsyncException as err:
    logging.error("Unable to sync data between hosts, from: %s, to %s",rsync.__get_from_path(),rsync.get_to_path())
    sys.exit(4)
sys.exit(0)