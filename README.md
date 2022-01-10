# Rosoka-SDK-Python-API-Code
Python code that leverages the Rosoka SDK Python API to perform entity&amp;relationship extraction, sentiment analysis, and content gisting

The Rosoka SDK is natively provides a Java API. Rosoka has wrapped that Java API with Python, via Python JPype, to expose their text analytic capabilities via Python. 

Rosoka provides some Java and Python examples, but here are some that I've created and routinely use. 

1) rosoka.py -- attempts to mimic the capabilities of the OOTB rosoka.sh script. It takes a single command line parameter and will process it. That parameter could be a file name, a directory path, or a string of text (enveloped by double quotes .. or whatever your shell uses to isolate the text string as a single parameter). 2) rosoka_process.py -- simplified version of 'rosoka.py' that takes a single directory path as a command line parameter. Script will iterate through the directory of files and submit each to the Rosoka SDK for processing. It will mirror the directory structure of the source/input directory path when the output is written. 
3) rosoka_process_vistAllFiles.py -- a variation of 'rosoka_process.py' that accepts a single directory path as a command line parameter. The script will invoke the Rosoka SDK visitAllFiles() method to process each file in the source/input directory. The visitAllFiles() method makes no attempt to mirror the directory structure of the input directory when output is written. 

