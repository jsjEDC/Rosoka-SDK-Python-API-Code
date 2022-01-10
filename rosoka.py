'''
VERSION: 0.9

Purpose: A utility to perform extraction on a (1) directory of text files; (2) single text file; or (3) string of text.

FEATURES:
  This utility:
  -) in ways mimics the 'rosoka.sh/bat' script that comes OOTB with RosokaSDK;
  -) takes a single parameter, a directory path, file path, or a string of text (enclosed in double-quotes) and creates a Rosoka RFO output file;
  -) attempts to discern if the user has provided a directory, file, or a string of text to process through the RosokaSDK;
  -) attempts to mirror the directory structure of the input directory when writing RFO output to the output directory structure
  -) will use a date/timestamp to name the output file if provided an input string of text. E.g., USER_PROVIDED_TEXT_20211027-1311_RFO.json

PREREQUISITES:
  1) Python JPype1 library installed (this is a prerequisite for any use of the RosokaSDK Python API)
  2) Copy the /LxBase and /conf directories from the RosokaSDK to locally where this script will be executed
       Note the related 'Tweak' notes below below

USAGE:
  <python> rosoka.py irgcpraise.text
  <python> rosoka.py ./test/article.txt
  <python> rosoka.py inputdir
  <python> rosoka.py "Harry Morgan played Colonel Potter in the television show 'M.A.S.H.' on CBS"

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

  5) You may want to redefine the minimal contents of a file or text string to be judged viable for extraction.
       Edit the code at 'MINIMAL_VIABLE_TEXT_STRING_LENGTH'
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
MINIMAL_VIABLE_TEXT_STRING_LENGTH = 12
TEXT_FILE_EXTENSIONS              = [".txt", ".text", ".htm", ".html"]
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
        # do nothing
        return tempCountStr
    elif (tempCountLen < maxStrLen):
        while (tempCountLen < maxStrLen):
            tempCountStr = "0" + tempCountStr
            tempCountLen = len(tempCountStr)
        return tempCountStr


'''
'''
def gen_time_stamp():
    the_date = str(time.strftime("%Y%m%d"))
    the_time = str(time.strftime("%H%M"))
    time_stamp = ""
    time_stamp = the_date + "-" + the_time
    return time_stamp


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
                '''
                ADD ONLY FILES ENDING WITH *.txt
                '''
                file_extension = os.path.splitext(temp_filename)[1]
                if (file_extension in TEXT_FILE_EXTENSIONS):
                    files_list.append(temp_filename)
                    LOCAL_DEBUG_FLAG: print("\tAdded " + " " + temp_filename)
            else:
                LOCAL_DEBUG_FLAG: print("Not file: " + entry)
    if LOCAL_DEBUG_FLAG: print("\n")
    return files_list


'''
'''
def could_be_text_string(extraction_input):
    global MINIMAL_VIABLE_TEXT_STRING_LENGTH
    if ( len(extraction_input) > MINIMAL_VIABLE_TEXT_STRING_LENGTH ):
        return True
    else:
        return False


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
def persist_rosoka_extraction(rosoka_extraction_object, content_type, input_file_name):
    LOCAL_DEBUG_FLAG = False

    ReadWriteRFO = JClass('com.rosoka.ReadWriteRFO')()
    #Process a file contents
    Rosoka = JClass('com.imt.RosokaAPI.Rosoka')()
    rfo = Rosoka.processStringRosokaFullObject(rosoka_extraction_object)
    
    output_rfo_file = ""

    if (content_type == "text_string"):
        base_path = os.getcwd()
        base_path_name = os.path.join(base_path, DEFAULT_OUTPUT_DIRECTORY, '')
        base_file_name = "USER_PROVIDED_TEXT_" +  gen_time_stamp() + "_RFO.json"
        output_rfo_file = base_path_name + base_file_name

    elif (content_type == "file"):
        if (input_file_name):
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
    print("\nUsage: <python> rosoka.py [input object]\n\tInput object = \n\t(1) filepath to file to process; \n\t(2) directory path of files to process\n\t(3) a string of text to process")


'''
  input = a single file to process
  Parameters
    1) input             : name of the file to be processed
    2) input_object_type : key to how RFO output is written to disk 
    3) input_file_name   : name of the file to be processed
'''
def process_file(extraction_input, input_object_type, input_file_name):
    '''
    check validity of file .. all we know so far is that the file exists
    '''
    global MINIMAL_VIABLE_TEXT_STRING_LENGTH
    try:
        src_FH = open(extraction_input, 'r')
    except:
        display_usage()
        msg = "The input file: " + extraction_input + " .. does not appear to be readable. Please check file and parent directory permissions.\n"
        sys.exit(msg)

    # read file into a string
    source_text = src_FH.read()
    if len(source_text) >= MINIMAL_VIABLE_TEXT_STRING_LENGTH:
        persist_rosoka_extraction(source_text, input_object_type, input_file_name)
    else:
        print("\t\tFILE IGNORED as it does not meet the minimum viable text standard.")


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
        input_object_type = "file"
        process_file(a_file, input_object_type, a_file)
        file_counter = file_counter + 1


'''
  input = a string of text
  Parameters
    1) input             : a single file
    2) input_object_type : key to how RFO output is written to disk
'''
def process_text_string(extraction_input, input_object_type):
    if extraction_input:
        rosoka_json_results = persist_rosoka_extraction(extraction_input, input_object_type, "")


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
                msg = "It does not appear that an input filename|directory|text string was provided\n"
                sys.exit(msg)
    else:
        clean_quit
        display_usage()
        msg = "It does not appear that an input filename|directory|text string was provided\n"
        sys.exit(msg)
    
    input_object_type = ""
    files_to_interrogate = list()
    
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
    if (os.path.isdir(input)):
        files_to_interrogate = traverse(input, files_to_interrogate)
        if DEBUG_FLAG:
            print(input + " object is DIRECTORY\n")
        process_directory(files_to_interrogate)
    elif (os.path.isfile(input)):
        input_object_type = "file"
        if DEBUG_FLAG:
            print(input + " object is FILE\n")
        print("\n")
        process_file(input, input_object_type, input)
    elif (could_be_text_string(input)):
        input_object_type = "text_string"
        if DEBUG_FLAG:
            print("object is TEXT_STRING\n")
        process_text_string(input, input_object_type)
    #elif .. could it be a URL
    else:
        clean_quit
        display_usage()
        msg = "It does not appear that a valid input filename|directory|text string was provided\n"
        sys.exit(msg)
    
    clean_quit()


