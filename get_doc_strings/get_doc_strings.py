#!/usr/bin/python3
import os
import argparse
import logging
import sys
import importlib.util
import typing
import inspect

"""
Recursivley browse a directory and return all of the classes in all python files, with the doc string for that class.
Currently classes only, no function docstrings.
"""

def module_from_string(path : str):

    #Get <name> from /a/b/<name>.py
    name = path.split("/")[-1].split(".")[0]
    logging.debug("Importing {} as {}".format(path, name))

    #Get the module
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    
    #Execute the module (so the classes get defined) and return it
    try:
        spec.loader.exec_module(mod)
    except Exception as e:
        logging.error("ERROR in {} : {}".format(name, str(e)))

    return mod

def get_doc_strings(rootdir):

    results = {}

    #Recursively search from rootdir
    for root, directories, filenames in os.walk(rootdir):
        
        #Filter only python files
        filenames = filter(lambda f : f.endswith(".py"), filenames)

        #For every python file
        for filename in filenames:
            logging.debug("----------------------------------")       
            logging.debug("Found module: {} at {}".format(filename, root))
            
            #Turn it into a module
            absroot = os.path.abspath(root)
            module = module_from_string(absroot + "/" + filename)

            #Get all the classes from that module
            classmembers = inspect.getmembers(module, inspect.isclass)
            logging.debug("Found {} classes".format(len(classmembers)))
            classmembers = list(filter(lambda x : inspect.getdoc(x[1]) is not None, classmembers))
            logging.debug("{} Have doc strings".format(len(classmembers)))

            #Get docstring and add to results
            for name, obj in classmembers:
                doc = inspect.getdoc(obj)
                results[name] = str(doc)
    
    return results

def dir_path(string):
    """
    Used by argparse to ensure dir argument is a dir_path
    """
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--dir", help="The directory to recursivley search from",
        required=True, type=dir_path)

    parser.add_argument("-v", "--verbose", help="Print debug messages",
        action="store_true")

    args = parser.parse_args()

    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.INFO,
        format='%(message)s')

    docstrings = get_doc_strings(args.dir)

    for key in docstrings:
        logging.info("")
        logging.info("Class : {}".format(key))
        logging.info("'{}'".format(docstrings[key]))


