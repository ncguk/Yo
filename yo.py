#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random
import shutil
import string
import sys
import argparse

# Allow the user to specify settings from the command line
parser = argparse.ArgumentParser(prog='Yo',
                                 description='A Python script to create a \
                                 number of randomly named, empty or non-empty \
                                 files')
parser.add_argument('-p',
                    '--path',
                    action='store',
                    dest='path',
                    default=os.getcwd(),
                    help='The base path where the randomly named folder will \
                    be created (e.g. /home/user/). If no path is given, the \
                    current working directory will be used')
parser.add_argument('-f',
                    '--files',
                    action='store',
                    dest='files',
                    default='50',
                    type=str,
                    help='Create N files, where N is a number between 1 and \
                    1,000,000. If no argument is given, Yo will create a \
                    folder with a default of 50 files')
parser.add_argument('-n',
                    '--name',
                    action='store',
                    dest='name',
                    metavar='NAME LENGTH',
                    default=8,
                    type=int,
                    help='Number of characters you would like in the \
                    randomly created file names, between 1 and 220. If no \
                    argument is given, Yo will use an 8 character file name')
parser.add_argument('-s',
                    '--suffix',
                    action='store',
                    dest='suffix',
                    metavar='SUFFIX LENGTH',
                    default=3,
                    type=int,
                    help='Number of characters you would like in the \
                    randomly created file name suffix, between 1 and 20. If \
                    no argument is given, Yo will use a 3 character suffix')
parser.add_argument('-d',
                    '--data',
                    action='store_true',
                    dest='data',
                    help='Using this option will fill the randomly generated \
                    files with between 0 and 10240 bytes of random data')
parser.add_argument('-r',
                    '--remove',
                    action='store_true',
                    dest='remove',
                    help='Using this option will remove the folder and files \
                    after they have been created')
parser.add_argument('-v',
                    '--version',
                    action='version',
                    version='%(prog)s 1.3.0',
                    help="Print the program's version number and exit")
args = parser.parse_args()

# Accept the user's command line input

# Take the number of files requested and strip out anything that isn't a digit
args.files = int(''.join(i for i in args.files if i.isdigit()))

# Check the number of files requested is between 1 and 1,000,000
if 1 <= args.files <= 1000000:
    number_of_files = args.files
else:
    sys.exit('Number of files: Please enter a number between 1 and 1,000,000')


# Create the random character strings
def name(name_chars=string.ascii_lowercase + string.digits,
         name_length=args.name):
    # Check the file name is between 1 and 220 characters long
    if 1 <= args.name <= 220:
        return ''.join(random.choice(name_chars)
                       for _ in range(name_length))
    else:
        sys.exit('File name: Please enter a number between 1 and 220')


def suffix(suffix_chars=string.ascii_lowercase + string.digits,
           suffix_length=args.suffix):
    # Check the file suffix is between 1 and 20 characters long
    if 1 <= args.suffix <= 20:
        return ''.join(random.choice(suffix_chars)
                       for _ in range(suffix_length))
    else:
        sys.exit('File name suffix: Please enter a number between 1 and 20')


# Take the path supplied and, if there is one, strip off the trailing slash
base_directory = args.path.rstrip("/")

# Set the random container directory name in stone so we can cd into it
dirname = name()

# Combine the base directory and randomly named directory
fullpath = os.path.join(base_directory, dirname)

# Generate the randomly named folder and the files to go inside it
try:
    # Change to the base directory
    try:
        os.chdir(base_directory)
    except OSError:
        sys.exit('The base directory path is incorrect or does not exist. \
Please amend the path setting or create the directory path in your OS')

    # Create the container directory
    try:
        if not os.path.exists(fullpath):
            os.mkdir(fullpath)
            os.chdir(fullpath)
    except IOError:
        sys.exit('The directory Yo has tried to create already exists. \
Running Yo again should fix this problem')

    # Create the files inside the container directory
    try:
        # Create the files with random amount of random data inside
        if args.data is True:
            for i in range(number_of_files):
                with open('{}.{}'.format(name(), suffix()), 'w') as fout:
                    length = random.randrange(0, 10240, 1)
                    chars = string.ascii_letters + string.digits
                    data = ''.join(random.choice(chars) for _ in range(length))
                    fout.write(data)
                    fout.close()
        # Or create empty files
        else:
            for i in range(number_of_files):
                open('{}.{}'.format(name(), suffix()), 'w').close()
    except IOError:
        sys.exit('Error creating files. Please try again')

    # If the -r flag is specified, delete the folder and files we just created
    try:
        if args.remove is True:
            shutil.rmtree(fullpath)
    except OSError:
        sys.exit('The folder and files Yo created could not be deleted. \
Please delete them manually')

except KeyboardInterrupt:
    sys.exit('Operation cancelled by user')
