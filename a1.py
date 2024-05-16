#A1 - 4010
#Huda Nadeem
#1143941

import configparser
import os
import sys
import boto3
import cmd
import subprocess
import platform

# Reading my config file to get access key 
config = configparser.ConfigParser()
config.read("S5-S3.conf")
aws_access_key_id = config['default']['aws_access_key_id']
aws_secret_access_key = config['default']['aws_secret_access_key']

# Getting connction for AWS 
try:
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    s3 = session.client('s3')
    s3_res = session.resource('s3')
    #FIRST TASK
    #if successful then this will appear
    print("Welcome to the AWS S3 Storage Shell (S5)\nYou are now connected to your S3 storage")
except Exception as e:
    #FIRST TASK
    #if unsuccessful then this will appear
    print("Welcome to the AWS S3 Storage Shell (S5)\nYou could not be connected to your S3 storage\nPlease review procedures for authenticating your account on AWS S3")
    sys.exit(1)

class S5Shell(cmd.Cmd):

    #TASK 2 
    #promting the shell to start like this
    prompt = 'S5> '

    #ACCESS local directories inside shell
    def default(self, line):
        '''Execute non-S3 commands in the local system's shell, adjusting for OS differences'''
        if platform.system() == "Windows":
            #adjusting commands for Windows so that ican use proper terms
            line = line.replace("ls", "dir").replace("pwd", "cd")
        try:
            #printing out the output
            output = subprocess.run(line, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(output.stdout)
        except subprocess.CalledProcessError as e:
            #if it doesnt work then a error message will print from the system (stderr)
            print(f"Command failed: {e.stderr}")

    def __init__(self):
        #making the shell with default bucket and path
        super().__init__()
        self.current_bucket = None  # making the current bucket as None to start off
        self.current_path = ''      # making the current path as an empty string to start off

    #TASK 3 local filef functions 
    def do_locs3cp(self, arg):
        'Copy a local file to an S3 bucket: locs3cp <local_file> <s3_destination>'
        if self.current_bucket is None:
            print("Please change to an S3 bucket before executing this command.")
            return

        args = arg.split()
        if len(args) != 2:
            print("Usage: locs3cp <local_file> <s3_destination>")
            return
        
        #error handling...

        #checking for wrong information provided
        local_file, s3_destination = args
        if '/' not in s3_destination:
            print("Invalid S3 destination. Format: /<bucket_name>/<path>")
            return
        #checking for wrong information provided
        bucket_name, s3_path = s3_destination.split('/', 2)[1:]
        if not s3_path:
            print("Invalid S3 path.")
            return
        #checking for wrong information provided
        if not os.path.isfile(local_file):
            print(f"Local file '{local_file}' not found.")
            return

        try:
            #Uploading the file user has provided to make sure it gets copeid to the desitination
            s3.upload_file(local_file, bucket_name, s3_path)
            print(f"File '{local_file}' successfully copied to '{s3_destination}'")
        except Exception as e:
            print(f"Unsuccessful copy: {e}")
    #TASK 4 A)
    def do_create_bucket(self, arg):
        'Create a new S3 bucket: create_bucket /<bucket_name>'
        if not arg.startswith('/'):
            print("Usage: create_bucket /<bucket_name>")
            return

        bucket_name = arg[1:]  # changes the input to remove the '/' at the frot
        try:
            #creating the new buclet with the name provided
            s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': 'ca-central-1'})
        except Exception as e:
            #error messahe if bucket doesn't get made properly
            print(f"Cannot create bucket: {e}")
    #TASK 4 B) change location/change directory
    def do_chlocn(self, arg):
        'Change the current S3 location: chlocn /<bucket_name> or chlocn /<bucket_name>/<path>'
        bucket_name = self.current_bucket  # staring with the current bucket

        if arg.startswith('/'):
            parts = arg[1:].split('/', 1)
            bucket_name = parts[0]
            s3_path = parts[1] if len(parts) > 1 else ''
        elif arg == '..':
            # getting to the bucket root
            s3_path = ''
        else:
            #error checking
            print("Invalid command or path.")
            return

        try:
            if bucket_name:
                # Checking to see if the bucket is there/exits
                s3.head_bucket(Bucket=bucket_name)
                self.current_bucket = bucket_name
                self.current_path = s3_path
                print(f"Current location changed to: /{self.current_bucket}/{self.current_path}")
            else:
                print("Bucket not specified or does not exist.")
        except Exception as e:
            print(f"Cannot change folder: {e}")
    #TASK 4 C) checking the current location/directory
    def do_cwlocn(self, arg):
        'Displays the current working location in S3 space: cwlocn'
        try:
            #checking is bucket has been chosen
            if self.current_bucket:
                #checking to see if theres a path inside the bucket
                current_location = f"{self.current_bucket}:{self.current_path}" if self.current_path else f"{self.current_bucket}:"
                print(current_location)
            else:
                #if no bucket got selected then dipsplay where the user is in S3 root
                print("/")
        except Exception as e:
            #error handling is location cant be accessed
            print("Cannot access location in S3 space")
    #TASK 4 D)
    def do_list(self, arg):
        'List the contents of the current working directory or a specified S3 location: list'
        try:
            if self.current_bucket:
                # if there is a path inside the bucket then use the prefix
                prefix = self.current_path if self.current_path else ""
                if prefix and not prefix.endswith('/'):
                    #making sure that prefix always ends with a '/'
                    prefix += '/' 

                #query of S3 to list objcts with the proper prefix
                response = s3.list_objects_v2(Bucket=self.current_bucket, Prefix=prefix, Delimiter='/')


                #checking for objects in responce
                if 'Contents' in response:
                    for item in response['Contents']:
                        # printign object names without prefix
                        print(item['Key'][len(prefix):])  
                if 'CommonPrefixes' in response:
                    for item in response['CommonPrefixes']:
                        # printing folder names (inside objects)
                        print(item['Prefix'][len(prefix):])  
                elif 'Contents' not in response and 'CommonPrefixes' not in response:
                    print("No objects or folders found in the current location.")
            else:
                #if not bucket got selected, then print all list at the root
                response = s3.list_buckets()
                for bucket in response['Buckets']:
                    print(bucket['Name'])
        except Exception as e:
            #printing if an error occurred
            print(f"Cannot list contents of this S3 location: {e}")

    #EXITING & QUITTING shell
    def do_exit(self, arg):
        'Exit the S5 shell: exit'
        print("Sucessfully Exited!")
        return True

    def do_quit(self, arg):
        'Quit the S5 shell: quit'
        print("Sucessfully quit!!")
        return True

if __name__ == '__main__':
    S5Shell().cmdloop()
