import os
import sys
import subprocess
import multiprocessing
import itertools, time
import argparse


"""
Structure:
    - input of targets: read file -> list -- DONE
    - #TODO: super function: create cloud instance -> run script -> get output -> delete cloud instance
    - #TODO: function to get only unique subdomains from all the files
    [
        - module: Category: subdomain enumeration
            Summary: input list <-> output file 
            - tool 1 function -> output: list of subdomains -> write to file # amass -- DONE
            - tool 2 function -> output: list of subdomains -> write to file # subfinder -- DONE
            - tool 3 function -> output: list of subdomains -> write to file # assetfinder -- DONE
            - tool 4 function -> output: list of subdomains -> write to file # sublist3r -- DONE
    ]
 
"""

def targetToList(targets):
    '''
    Function to convert a target file to a list.
    '''
    with open(targets, 'r') as f:
        my_list = [line.strip() for line in f]

    return my_list

def fancyBar(msg, secs):
    a = 1
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if a > secs:
            sys.stdout.write("\x1b[1;32m\r [" + "+" + f'] {msg}' +"\x1b[0m")
            print()
            break
        sys.stdout.write("\x1b[1;32m\r [" + c + f'] {msg}' +"\x1b[0m")
        sys.stdout.flush()
        time.sleep(0.1)
        a += 1

def amass(target):
    '''
    Function to run amass and return a list of subdomains.
    '''
    fancyBar("Running amass on target: " + target, 4)
    output = subprocess.Popen(f"amass enum -passive -d {target} -o amass_output-{target}.txt >/dev/null", shell=True, stderr=subprocess.PIPE)
    output.wait()
    fancyBar("Amass finished on target: " + target, 4)
    os.system("echo Amass finished on target: " + target )
    os.system("echo Total subdomains found: " + str(len(targetToList(f'amass_output-{target}.txt'))))
    listOfSubdomainFiles.append(f'amass_output-{target}.txt')

def subfinder(target):
    '''
    Function to run subfinder and return a list of subdomains.
    '''
    fancyBar("Running subfinder on target: " + target, 4)
    output = subprocess.Popen(f"subfinder -d {target} -o subfinder_output-{target}.txt >/dev/null", shell=True, stderr=subprocess.PIPE)
    output.wait()
    fancyBar("Subfinder finished on target: " + target, 4)
    os.system("echo Subfinder finished on target: " + target )
    os.system("echo Total subdomains found: " + str(len(targetToList(f'subfinder_output-{target}.txt'))))
    listOfSubdomainFiles.append(f'subfinder_output-{target}.txt')

def assetfinder(target):
    '''
    Function to run assetfinder and return a list of subdomains.
    '''
    fancyBar("Running assetfinder on target: " + target, 4)
    output = subprocess.Popen(f"assetfinder --subs-only {target} > assetfinder_output-{target}.txt", shell=True, stderr=subprocess.PIPE)
    output.wait()
    fancyBar("Assetfinder finished on target: " + target, 4)
    os.system("echo Assetfinder finished on target: " + target )
    os.system("echo Total subdomains found: " + str(len(targetToList(f'assetfinder_output-{target}.txt'))))
    listOfSubdomainFiles.append(f'assetfinder_output-{target}.txt')

def parse_args():
    parser = argparse.ArgumentParser(description="This script takes arguments to pass to a function")
    parser.add_argument("--target", required=True, help="List of Targets to enumerate")
    parser.add_argument("--targetName", required=True, help="Name of the target")
    parser.print_help()
    return parser

def main():
    
    if len(sys.argv)==1:
        print("No arguments passed. Syntax: python3 test.py <target_file> <target_name>")
        sys.exit(1)
    targetFile = sys.argv[1]
    targetName = sys.argv[2]
    # make a directory for the target name and change location of the output files to that directory
    os.system(f"mkdir -p {targetName}")

    fancyBar("Reading from file and initiating first tool.", 4)
    targets = targetToList(targetFile)
    print("Total targets found:", len(targets))
    fancyBar("Starting pool of processes.", 4)

    pool = multiprocessing.Pool(3)

    
    # Subdomain enumeration

    # Calling amass function for each target
    pool.map(amass, targets)
    # Calling subfinder function for each target
    pool.map(subfinder, targets)
    # Calling assetfinder function for each target
    pool.map(assetfinder, targets)

    pool.join()
    pool.close()


listOfSubdomainFiles = []

main()