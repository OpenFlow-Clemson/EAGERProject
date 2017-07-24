import shutil
import subprocess
from os import chdir
from os import makedirs
from os import path
from os import listdir
from subprocess import check_output

import jprops
import mininet.log as log
from mininet.moduledeps import pathCheck
from mininet.node import Controller
# from pick import pick

import httplib
import json


class Floodlight(Controller):
    # Port numbers used to run Floodlight. These must be unique for every instance.
    # Static class variables are used to keep track of which ports have been used already.
    sync_manager_port = 6009
    openflow_port = 6653
    http_port = 8080
    https_port = 8081

    # Number of Floodlight instances created. Used for naming purposes.
    controller_number = 0

    def listdir_fullpath(d):
        return [path.join(d, f) for f in listdir(d)]

    # Check TARN folder path
    # try:
    #     fl_options = check_output('sudo find /home/ -type d -name TARN', shell=True)
    #     # Check to make sure only one TARN folder
    #     if (fl_options == ''):
    #         user_title = 'Choose a directory to install Floodlight in: '
    #         user_options = listdir_fullpath('/home/')
    #         root_dir, index = pick(user_options, user_title)
    #         fl_root_dir = root_dir + '/TARN'
    #         installFloodlight()
    #     else:
    #         fl_title = 'Choose which instance of Floodlight you want to run: '
    #         fl_options = fl_options.split('\n')
    #         fl_root_dir, index = pick(fl_options, fl_title)
    # except subprocess.CalledProcessError:
    #     print 'Something went wrong when looking for Floodlight!'
    #     exit()

    fl_root_dir = '/home/mininet/EAGERProject/EAGERFloodlight'

    def __init__(self, name,
                 command='java -jar ' + fl_root_dir + '/target/floodlight.jar',
                 cargs='',
                 ip='127.0.0.1',
                 **kwargs):

        # Increment the number of controller instances for naming purposes.
        Floodlight.controller_number += 1

        # Initialize attributes
        self.name = name
        self.properties_path = ''
        self.properties_file = ''

        self.createUniqueFloodlightPropertiesFile()
        self.port = self.openflow_port

        # Create the command that will start Floodlight, including the path to the unique properties file.
        self.command = command + ' -cf ' + self.properties_path + self.properties_file

        # Initialize the parent class.
        Controller.__init__(self, name, cdir=self.fl_root_dir,
                            command=self.command,
                            cargs=cargs, port=self.openflow_port, ip=ip, **kwargs)

    def start(self):
        """Start <controller> <args> on controller.
           Log to /tmp/cN.log"""
        log.info('Starting controller...\n')
        pathCheck(self.command)
        cout = '/tmp/' + self.name + '.log'
        chdir(self.fl_root_dir)
        self.cmd(self.command + ' ' + self.cargs +
                 ' 1>' + cout + ' 2>' + cout + '&')
        self.execed = False

    def stop(self):
        log.debug('Removing ' + self.name + ' properties file...')
        subprocess.call('rm ' + self.properties_path + self.properties_file, shell=True)

        print ">>>>> print command"
        print self.command

        print ">>>>> print floodlight string representation"
        print self.__repr__()
        super(Floodlight, self).stop()

    def setRandomizeTo(self, randomize):
        data = {
            "randomize": str(randomize)
        }
        ret = self.rest_call('/wm/randomizer/config/json', data, 'POST')
        return ret[0] == 200

    def enableRandomizer(self):
        data = {}
        ret = self.rest_call('/wm/randomizer/module/enable/json', data, 'POST')
        return ret[0] == 200

    def disableRandomizer(self):
        data = {}
        ret = self.rest_call('/wm/randomizer/module/disable/json', data, 'POST')
        return ret[0] == 200

    def addServer(self, server):
        data = {
            "server": server
        }
        ret = self.rest_call('/wm/randomizer/server/add/json', data, 'POST')
        return ret[0] == 200

    def removeServer(self, server):
        data = {
            "server": server
        }
        ret = self.rest_call('/wm/randomizer/server/remove/json', data, 'POST')
        return ret[0] == 200

    def addPrefix(self, ip, mask, server):
        data = {
            "ip-address": ip,
            "mask": mask,
            "server": server
        }
        ret = self.rest_call('/wm/randomizer/prefix/add/json', data, 'POST')
        return ret[0] == 200

    def removePrefix(self, ip, mask, server):
        data = {
            "ip-address": ip,
            "mask": mask,
            "server": server
        }
        ret = self.rest_call('/wm/randomizer/prefix/remove/json', data, 'POST')
        return ret[0] == 200

    def setLanPort(self, port):
        data = {
            "localport": str(port)
        }
        ret = self.rest_call('/wm/randomizer/config/json', data, 'POST')
        return ret[0] == 200

    def setWanPort(self, port):
        data = {
            "wanport": str(port)
        }
        ret = self.rest_call('/wm/randomizer/config/json', data, 'POST')
        return ret[0] == 200

    def createUniqueFloodlightPropertiesFile(self):
        """
        Creates a unique properties file for the particular Floodlight instance.
        Each file is put in the 'properties' folder in the floodlight directory.
        Static class attributes keep track of the current port number to use.
        :return: None
        """

        # The path to the properties file to be copied and the name of the file
        old_path = Floodlight.fl_root_dir + '/src/main/resources/'
        old_file = 'floodlightdefault.properties'

        # The path where the new properties file will be located and the name of the file
        new_path = Floodlight.fl_root_dir + 'properties/'
        new_file = 'floodlight' + str(Floodlight.controller_number) + '.properties'

        # Set the instance attributes so that the instance can know where its associated properties file is
        self.properties_path = new_path
        self.properties_file = new_file

        # Check if the new path already exists. If not, then create it
        if not path.exists(new_path):
            makedirs(new_path)

        # Copy the old properties file to the new location with the new name
        shutil.copy(old_path + old_file,
                    new_path + new_file)

        # Open the new properties file and scan it for the ports that need to be changed
        with open(new_path + new_file) as fp:
            properties = jprops.load_properties(fp)

            http = [key for key, value in properties.items() if key.endswith('httpPort')][0]
            https = [key for key, value in properties.items() if key.endswith('httpsPort')][0]
            openflow = [key for key, value in properties.items() if key.endswith('openFlowPort')][0]
            syncmanager = [key for key, value in properties.items() if key.endswith('SyncManager.port')][0]

            properties[http] = str(Floodlight.http_port + 10)
            properties[https] = str(Floodlight.https_port + 10)
            properties[openflow] = str(Floodlight.openflow_port + 10)
            properties[syncmanager] = str(Floodlight.sync_manager_port + 10)

            # Update the class attributes so that everyone knows what ports are available now
            Floodlight.http_port += 10
            Floodlight.https_port += 10
            Floodlight.openflow_port += 10
            Floodlight.sync_manager_port += 10

            self.openflow_port = Floodlight.openflow_port

            log.debug('Ports being used in controller ' + self.name + ' property file...\n')
            log.debug(http + ' = ' + properties[http] + '\n')
            log.debug(https + ' = ' + properties[https] + '\n')
            log.debug(openflow + ' = ' + properties[openflow] + '\n')
            log.debug(syncmanager + ' = ' + properties[syncmanager] + '\n')

        # Write the updated ports to the new properties file
        with open(new_path + new_file, 'w') as fp:
            # print 'Writing to file ' + new_file
            jprops.store_properties(fp, properties)

    def rest_call(self, path, data, action):
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
        }
        body = json.dumps(data)
        conn = httplib.HTTPConnection('127.0.0.1', self.http_port)
        conn.request(action, path, body, headers)
        response = conn.getresponse()
        ret = (response.status, response.reason, response.read())
        print ret
        conn.close()
        return ret


def isFloodlightInstalled():
    """
    This is a helper function to determine whether floodlight has been installed.
    :return: true or false
    """
    if not path.isdir(Floodlight.fl_root_dir):
        log.debug('Floodlight is not installed.\n')
        return False
    else:
        log.debug('Floodlight has been installed.\n')
        return True


def installFloodlight():
    """
    Installs floodlight in the parent of the current directory.
    :return: none
    """
    log.info('Installing Floodlight...\n')
    # Install the EAGER version of Floodlight
    subprocess.call('git clone http://github.com/geddings/TARN ' + Floodlight.fl_root_dir, shell=True)
    chdir(Floodlight.fl_root_dir)
    subprocess.call('sudo ant', shell=True)
    chdir(path.abspath(path.pardir))


if __name__ == "__main__":
    log.setLogLevel('debug')