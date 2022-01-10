'''
VERSION: 0.2

Purpose: A utility to perform extraction on a directory of files

FEATURES:
  This utility:
  -) takes a single parameter, a directory path, and creates a corresponding Rosoka RFO output file;
  -) attempts to mirror the directory structure of the input directory when writing RFO output to the output directory structure

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
import os
import os.path
import sys
import time

'''
GLOBAL VARIABLES
'''
DEBUG_FLAG                        = False
DEFAULT_INPUT_DIRECTORY           = "inputdir"
DEFAULT_OUTPUT_DIRECTORY          = "outdir"


'''
'''
def pad_counter(count, max):
    # count and max are integers. If passed (2,99), should "pad" the 2 with a leading 0 .. ala 2 ==> "02"
    maxStr       = str(max)
    maxStrLen    = len(maxStr)
    countStr     = str(count)
    tempCountStr = countStr
    tempCountLen = len(tempCountStr)

    if (tempCountLen >= maxStrLen):
        return tempCountStr
    elif (tempCountLen < maxStrLen):
        while (tempCountLen < maxStrLen):
            tempCountStr = "0" + tempCountStr
            tempCountLen = len(tempCountStr)
        return tempCountStr


'''
'''
def traverse(targetDir, files_list):
    LOCAL_DEBUG_FLAG = False
    currentDir = targetDir
    dirs       = os.listdir(targetDir)
    for entry in dirs:
        if os.path.isdir(os.path.join(currentDir,entry)):
            if LOCAL_DEBUG_FLAG: print("Traversing .. " + os.path.join(targetDir,entry))
            traverse(os.path.join(targetDir,entry), files_list)
        else:
            if os.path.isfile(os.path.join(targetDir,entry)):
                temp_filename = os.path.join(currentDir,entry)

                if LOCAL_DEBUG_FLAG: print("\tLooking at" + " " + os.path.join(currentDir,entry))
                
                files_list.append(temp_filename)
                LOCAL_DEBUG_FLAG: print("\tAdded " + " " + temp_filename)
            else:
                LOCAL_DEBUG_FLAG: print("Not file: " + entry)
    if LOCAL_DEBUG_FLAG: print("\n")
    return files_list


'''
'''
def generate_new_output_path(input_filename):

    global DEFAULT_INPUT_DIRECTORY
    LOCAL_DEBUG_FLAG = False

    new_output_filename  = input_filename.replace(DEFAULT_INPUT_DIRECTORY, DEFAULT_OUTPUT_DIRECTORY)

    if LOCAL_DEBUG_FLAG: print("[generate_new_output_path] new_output_filename = " + new_output_filename)

    return new_output_filename


'''
'''
def persist_rosoka_extraction(input_file_name, input_file_object):
    LOCAL_DEBUG_FLAG = False

    ReadWriteRFO = JClass('com.rosoka.ReadWriteRFO')()
    #Process a file
    Rosoka = JClass('com.imt.RosokaAPI.Rosoka')()
    rfo = Rosoka.processFileRosokaFullObject(input_file_object)
    
    output_rfo_file = ""
    output_rfo_file = generate_new_output_path(input_file_name + "_RFO.json")

    if LOCAL_DEBUG_FLAG: print("output_rfo_file = " + output_rfo_file)

    out_dir = os.path.dirname(output_rfo_file)
    if not(out_dir):
        out_dir = DEFAULT_OUTPUT_DIRECTORY
        output_rfo_file = os.path.join(DEFAULT_OUTPUT_DIRECTORY, output_rfo_file)

    itExists = os.path.exists(os.path.dirname(output_rfo_file))
    if not itExists:
        os.makedirs(os.path.dirname(output_rfo_file))

    ReadWriteRFO.writeRfoToJsonFile(output_rfo_file, rfo)
    print("\t\tOutput written to " + output_rfo_file)


'''
'''
def display_usage():
    print("\nUsage: <python> rosoka.py <directory name or path of files to process>")




'''
  input = a list of files to process
'''
def process_directory(extraction_input):
    number_of_files_to_process = len(extraction_input)
    file_counter = 1
    print("\nFILES TO PROCESS FOR EXTRACTION ..")
    for a_file in extraction_input:
        padded_file_counter = pad_counter(file_counter, number_of_files_to_process)
        print("\t" + padded_file_counter + " of " + str(number_of_files_to_process) + " : " + a_file)
        file_object = JClass('java.io.File')(a_file)
        persist_rosoka_extraction(a_file, file_object)
        file_counter = file_counter + 1


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
    #print("\n\nROSOKA_HOME => ",rosokahome.getRosokaHome())
    
    
    '''
      determine what kind of "thing" the input is
    '''
    files_to_interrogate = list()
    if (os.path.isdir(input)):
        files_to_interrogate = traverse(input, files_to_interrogate)
        if DEBUG_FLAG:
            print(input + " object is DIRECTORY\n")
        process_directory(files_to_interrogate)
    else:
        clean_quit
        display_usage()
        msg = "It does not appear that a valid input directory was provided\n"
        sys.exit(msg)
    
    clean_quit()


