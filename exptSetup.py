#! /usr/bin/python2

import os
import sys
import time
import lxml.etree

def check_exists(directory):
    """If directory does not exist, create it."""
    if not os.path.isdir(directory):
        os.mkdir(directory)
    else:
        sys.stderr.write("Directory %s exists.\n" % directory)

def create_analysis_directories():
    """Builds directory tree with analysis, bin and data folders."""
    sys.stderr.write("Creating directories...\n")
    check_exists("analysis")
    check_exists("analysis/figs")
    check_exists("analysis/tables")
    check_exists("bin")
    check_exists("data")

def create_control_script(script_name):
    """Creates initial analysis control shell script."""
    sys.stderr.write("Creating %s...\n" % script_name)
    f = open(script_name, "w")
    f.write("#!/bin/bash\n\n")
    f.write("# Analysis control script for %s\n" % os.path.abspath("."))
    f.write("# Created on %s\n\n" % time.asctime())
    f.write("BIN=%s\n" % os.path.join(os.path.abspath("."), "bin"))
    f.write("DATA=%s\n" % os.path.join(os.path.abspath("."), "data"))
    f.write("ANALYSIS=%s\n\n" % os.path.join(os.path.abspath("."), "analysis"))
    f.write("###DATA PROCESSING BLOCK###\n\n")
    f.write("###DATA ANALYSIS BLOCK###\n\n")
    f.write("echo 'Done.'\n")
    f.close()
    os.system("chmod +x %s" % os.path.join(os.path.abspath("."), script_name))


def create_template_script(setupXML):
    """Builds template scripts from XML files"""
    tree = lxml.etree.parse(open(setupXML))
    template_dict = dict([(i.tag, i.text) for i in tree.iterfind("/")])
    template_file = open(os.path.join("bin/", template_dict["filename"] + template_dict["filetag"]), "w")
    template_file.write("#!" + template_dict["path"] + "\n\n")
    template_file.write("# Template script for %s\n" % os.path.abspath("."))
    template_file.write("# Created on %s\n\n" % time.asctime())
    if template_dict["imports"]:
        template_file.writelines([imp+"\n" for imp in template_dict["imports"].split(",")])
    if template_dict["body"]:
        template_file.write("\n" + template_dict["body"] + "\n")
    template_file.close()
    if template_dict["make_executable"] == "yes":
        os.system("chmod +x %s" % os.path.join(os.path.abspath("."), "bin", 
                                template_dict["filename"] + template_dict["filetag"]))
        
def build_all_templates(template_dir):
    sys.stderr.write("Creating template scripts...\n")
    for template in os.listdir(template_dir):
        create_template_script(os.path.join(template_dir, template))
        

class Git:
    """Access git commands from Python"""
    @staticmethod
    def initialise():
        os.system("git init")
    
    @staticmethod
    def add(files = "."):
        sys.stderr.write("Adding files to git repository...\n")
        os.system("git add " + files)
    
    @staticmethod
    def commit(message):
        sys.stderr.write("Committing: %s...\n" % message)
        os.system("git commit -m '" + message + "'")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        template_dir = sys.argv[1]
    else:
        sys.stderr.write("Please include template directory location.\n")
        sys.exit(0)

    create_analysis_directories()
    create_control_script("control.sh")
    build_all_templates(template_dir)

    Git.initialise()
    Git.add()
    Git.commit("First commit: directory setup")
