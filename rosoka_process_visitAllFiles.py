'''
VERSION: 0.2

Purpose: A utility to perform extraction on a directory of files using the visitAllFiles() Rosoka SDK API method

FEATURES:
  This utility:
  -) takes a single parameter, a directory path, and creates a corresponding Rosoka RFO output file;

PREREQUISITES:
  1) Python JPype1 library installed (this is a prerequisite for any use of the RosokaSDK Python API)
  2) Copy the /LxBase and /conf directories from the RosokaSDK to locally where this script will be executed
       Note the related 'Tweak' notes below below

USAGE:
  <python> rosoka.py inputdir

Note: This utility uses the PythonAPI for the RosokaSDK. 

TWEAKS THAT MAY BE NECESSARY TO RUN THIS IN YOUR ENVIRONMENT
  1) You may need to point to the appropriate copy of the RosokaSDK RosokaAPI.jar. This file can be kept local to this utility OR you can reference the one that comes with your installation of the RosokaSDK.
     RESOLUTION:
       Edit the code at 'cpopt="-Djava.class.path=%s" % ("./RosokaAPI.jar")'  as appropirate

  2) You may need to point to the appropriate copy of the Rosoka SDK 'conf' directory. This directory can be kept local to this utility OR you can reference the one that comes with your installation of the RosokaSDK.
     RESOLUTION:
       Edit the code at 'ROSOKA_HOME="/Users/jasonjames/apps/RosokaSDK_7401/conf"' as appropriate

  3) You may want to include additional document types. Modify the global variable 'TEXT_FILE_EXTENSIONS' as appropriate
  
  4) You may want to redefine the default 'input' and 'output' directories
       Edit the code at 'DEFAULT_OUTPUT_DIRECTORY' and 'DEFAULT_INPUT_DIRECTORY'

NOTES:
  - created mid-December 2021 as a variant of 'rosoka.py' (version 0.9) to help a Rosoka partner process a directory of documents for a sales presentation demonstration.

'''




from jpype import *
import sys

'''
GLOBAL VARIABLES
'''
DEBUG_FLAG                        = False
DEFAULT_INPUT_DIRECTORY           = "inputdir"




'''
'''
def display_usage():
    print("\nUsage: <python> rosoka.py <directory name or path of files to process>")


'''
'''
def clean_quit(event=None):
    shutdownJVM()








'''
================================================================================================================================================
================================================================================================================================================
================================================================================================================================================
================================================================================================================================================
================================================================================================================================================
================================================================================================================================================
================================================================================================================================================
'''




if __name__ == "__main__":

    if (len(sys.argv) == 2):
        if (sys.argv[1]):
            if ( len(sys.argv[1]) > 1 ):
                input = sys.argv[1]
                if DEBUG_FLAG: print("input       = " + input)
            else:
                clean_quit
                display_usage()
                msg = "It does not appear that an input directory was provided\n"
                sys.exit(msg)
    else:
        input = DEFAULT_INPUT_DIRECTORY
    
    '''
      Set the classpath options (location of the RosokaAPI.jar file)
      The path can be explicitly set or set relative the the python file.
    '''
    cpopt="-Djava.class.path=%s" % ("./RosokaAPI.jar")
    #cpopt="-Djava.class.path=%s" % ("/Users/jasonjames/apps/RosokaSDK_7401/PythonAPI/lib/RosokaAPI.jar")
    
    '''
      Start the Java Virtual Machine (JVM) using the defualt path to java
      The jvm path may also be explicitly set to use other JVM's than the system's
      The java version must be java 1.8 or newer.
    '''
    startJVM(getDefaultJVMPath(),"-ea",cpopt , convertStrings=False)
    
    '''
      Set the ROSOKA_HOME location (folder location containing the licencekey.xml and RosokaProperties.xml properties files)
      And initialize the engine so it is ready to process.
      This step is performed once (outside any loops of threading)
      The path can be explicitly set or relative to the python file
    '''
    #ROSOKA_HOME="./conf"
    ROSOKA_HOME="/Users/jasonjames/apps/RosokaSDK_7401/conf"
    rosokahome=JClass('com.imt.RosokaAPI.Rosoka')(ROSOKA_HOME)

    Rosoka = JClass('com.imt.RosokaAPI.Rosoka')()
    file=JClass('java.io.File')(input)
    Rosoka.visitAllFiles(file)
    
    clean_quit()


