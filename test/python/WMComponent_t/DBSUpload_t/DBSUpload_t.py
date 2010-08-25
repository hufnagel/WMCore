#!/usr/bin/env python
#pylint: disable-msg=E1101,C0103,R0902
"""
DBSUpload test TestDBSUpload module and the harness
"""

__revision__ = "$Id $"
__version__ = "$Revision: 1.11 $"
__author__ = "anzar@fnal.gov"

import commands
import logging
import os
import threading
import time
import unittest

from WMComponent.DBSUpload.DBSUpload import DBSUpload

from WMCore.Agent.Configuration import loadConfigurationFile
from WMCore.Database.DBFactory import DBFactory
from WMCore.Database.Transaction import Transaction
from WMCore.WMFactory import WMFactory

class DBSUploadTest(unittest.TestCase):
    """
    TestCase for DBSUpload module 
    """

    _setup_done = False
    _teardown = False
    _maxMessage = 10

    def setUp(self):
        """
        setup for test.
        """

	if not DBSUploadTest._setup_done:
		logging.basicConfig(level=logging.NOTSET,
                	format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                	datefmt='%m-%d %H:%M',
                	filename='%s.log' % __file__,
                	filemode='w')

            	myThread = threading.currentThread()
            	myThread.logger = logging.getLogger('DBSUploadTest')

                if not os.getenv("DIALECT") == None:
                    myThread.dialect = os.getenv("DIALECT")
                else:
                    myThread.dialect = 'MySQL'

            	options = {}
                if not os.getenv("DBSOCK") == None:
                    options['unix_socket'] = os.getenv("DBSOCK")
            	dbFactory = DBFactory(myThread.logger, os.getenv("DATABASE"), \
                	options)




            	myThread.dbi = dbFactory.connect()
            	myThread.transaction = Transaction(myThread.dbi)
                myThread.transaction.begin()
                myThread.transaction.commit()
                DBSUploadTest._setup_done = True

    def tearDown(self):
        """
        Database deletion
        """
        """
        Database deletion
        """
        
        return True # I do not want to remove my database
        
        myThread = threading.currentThread()
        if DBSUploadTest._teardown and myThread.dialect == 'MySQL':
            # call the script we use for cleaning:
            command = os.getenv('WMCOREBASE')+ '/standards/./cleanup_mysql.sh'
            result = commands.getstatusoutput(command)
            for entry in result:
                print(str(entry))

        DBSUploadTest._teardown = False

    def testA(self):
        
        """
        Mimics creation of component and handles come messages.
        """
        
        #return True
        
        # read the default config first.
        config = loadConfigurationFile(os.path.join(os.getenv('WMCOREBASE'), \
            'src/python/WMComponent/DBSUpload/DefaultConfig.py'))

        # some general settings that would come from the general default 
        # config file
        config.Agent.contact = "anzar@fnal.gov"
        config.Agent.teamName = "DBS"
        config.Agent.agentName = "DBS Upload"

        config.section_("General")
        
        if not os.getenv("TESTDIR") == None:
            config.General.workDir = os.getenv("TESTDIR")
        else:
            config.General.workDir = os.getcwd()
        
        config.section_("CoreDatabase")
        if not os.getenv("DIALECT") == None:
            config.CoreDatabase.dialect = os.getenv("DIALECT").lower()
        #config.CoreDatabase.socket = os.getenv("DBSOCK")
        if not os.getenv("DBUSER") == None:
            config.CoreDatabase.user = os.getenv("DBUSER")
        else:
            config.CoreDatabase.user = os.getenv("USER")
        if not os.getenv("DBHOST") == None:
            config.CoreDatabase.hostname = os.getenv("DBHOST")
        else:
            config.CoreDatabase.hostname = os.getenv("HOSTNAME")
        config.CoreDatabase.passwd = os.getenv("DBPASS")
        if not os.getenv("DBNAME") == None:
            config.CoreDatabase.name = os.getenv("DBNAME")
        else:
            config.CoreDatabase.name = os.getenv("DATABASE")
        if not os.getenv("DATABASE") == None:
            config.CoreDatabase.connectUrl = os.getenv("DATABASE")

        testDBSUpload = DBSUpload(config)
        testDBSUpload.prepareToStart()

        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # for testing purposes we use this method instead of the 
        # StartComponent one.

        testDBSUpload.handleMessage('BufferSuccess', \
				'NoPayLoad')

        #I don't know what this does so I commented it
        #Especially since it breaks things
        #for i in xrange(0, DBSUploadTest._maxMessage):
        #    testDBSUpload.handleMessage('BufferSuccess', \
        #        'YourMessageHere'+str(i))

        while threading.activeCount() > 1:
            print('Currently: '+str(threading.activeCount())+\
                ' Threads. Wait until all our threads have finished')
            time.sleep(1)

        DBSUploadTest._teardown = True

    def runTest(self):
        self.testA()

if __name__ == '__main__':
    unittest.main()

