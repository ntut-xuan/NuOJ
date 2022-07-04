# -*- coding: utf-8 -*-
"""
The Isolate toolbox by Uriah Xuan for developing NuOJ System.
Due to isolate is a command-execute program, so you can use this tool if you want :D
"""

import subprocess
import os
from sandbox_enum import CodeType, Language


def init_sandbox(box_id=0):
    '''
    Initialize the specific ID of the sandbox.

        Args:
            box_id: The specific ID of the sandbox
    
    '''
    subprocess.call("isolate --box-id=%d --init" % (box_id), shell=True)


def touch_text_file(text, type: CodeType, language: Language, box_id=0) -> tuple:
    '''
    Create a new text file and write text.

        Parameters:
            text: The text you want to write
            type: The type of code, reference CodeType class.
            langauge: The language of code, reference Langauge class.
            box_id: The ID of sandbox you want to create text file.

        Return:
            The Tuple object.
            The first element is the file's path that should create.
            The second element is the status, True for success, False otherwise.
    
    '''
    path = "/var/local/lib/isolate/%d/box/%s%s" % (box_id, type, language)
    print("create file at", path)
    with open(path, "w") as code_file:
        code_file.write(text)
    if not os.path.exists(path):
        return (path, False)
    return (path, True)

def touch_text_file_by_file_name(text, filename, box_id=0) -> tuple:
    '''
    Create a new text file with specific file name and write text.

        Parameters:
            text: The text you want to write
            filename: The name of file.
            box_id: The ID of sandbox you want to create text file.

        Return:
            The Tuple object.
            The first element is the file's path that should create.
            The second element is the status, True for success, False otherwise.
    '''
    path = "/var/local/lib/isolate/%d/box/%s" % (box_id, filename)
    print("create file at", path)
    with open(path, "w") as code_file:
        code_file.write(text)
    if not os.path.exists(path):
        return (path, False)
    return (path, True)

def read_meta(box_id=0) -> str:
    '''
    Return the meta file of text, the result after the Isolate run.

        Parameters:
            box_id: The ID of the sandbox you want to read the text of meta file.

        Return:
            A string, the text of meta file on the specific ID of the sandbox.
    
    '''
    meta_path = "/var/local/lib/isolate/%d/box/meta" % (box_id)
    with open(meta_path, "r") as code_file:
        return code_file.read()

def read_output(output_index, type, box_id=0) -> str:
    '''
    Return the output file of text, the result after the Isolate run.

        Parameters:
            output_index: The index of the output file you want to read the text.
            box_id: The ID of the sandbox you want to read the text of meta file.

        Return:
            A string, the text of output file on the specific ID of the sandbox.
    
    '''
    output_file = "%d.out" % (output_index) if type == CodeType.SOLUTION.value else "%d.ans" % (output_index)
    output_path = ("/var/local/lib/isolate/%d/box/" + output_file) % (box_id)
    with open(output_path, "r") as code_file:
        return code_file.read()

def cleanup_sandbox(box_id=0):
    '''
    Cleanup the sandbox of the specific ID.

        Parameters:
            box_id: The ID of the sandbox you want to cleanup.
    
    '''
    subprocess.call("isolate --box-id=%d --cleanup" % (box_id), shell=True)


def compile(type, language, box_id=0) -> str:
    '''
    Compile the program on the specific ID of the sandbox.

        Parameters:
            type: The type of code, reference CodeType class.
            langauge: The language of code, reference Langauge class.
            box_id: The ID of the sandbox you want to compile the program.

        Return:
            A string of results on the meta file after finished compiled.
    
    '''
    code_path = "%s%s" % (type, language)
    code_output = "%s%s" % (type, ".o")
    meta_path = "/var/local/lib/isolate/%d/box/meta" % (box_id)
    touch_text_file("init", CodeType.META.value, Language.NONE.value, box_id)
    subprocess.call("isolate --time=4 -p --full-env --meta='%s' --run -- /usr/bin/g++ %s -o %s" % (meta_path, code_path, code_output), shell=True)
    return read_meta(box_id)

def execute(type, test_case_count, box_id=0) -> str:
    '''
    Execute the program on the specific ID of the sandbox.

        Parameters:
            type: The type of code, reference CodeType class.
            test_case_count: The count of testcase.
            box_id: The ID of the sandbox you want to compile the program.

        Return:
            A string of results on the meta file after finished execute.
    
    '''
    code_output = "%s%s" % (type, ".o")
    meta_path = "/var/local/lib/isolate/%d/box/meta" % (box_id)
    output = []
    touch_text_file("init", CodeType.META.value, Language.NONE.value, box_id)
    for i in range(test_case_count):
        output_file = "%d.out" % (i+1) if type == CodeType.SOLUTION.value else "%d.ans" % (i+1)
        command = "isolate --time=4 --wall-time=4 -p --full-env --stdin='%d.in' --stdout='%s' --meta='%s' --run -- %s" % (i+1, output_file, meta_path, code_output)
        touch_text_file_by_file_name("", output_file, box_id)
        print("Execute testcase %d" % (i+1))
        subprocess.call(command, shell=True)
        meta = read_meta(box_id)
        stdout_text = read_output(i+1, type, box_id)
        output.append((meta, stdout_text))
    return output

def checker(test_case_count, box_id):
    '''
    Execute the checker program on the specific ID of the sandbox.

        Parameters:
            test_case_count: The count of testcase.
            box_id: The ID of the sandbox you want to compile the program.

        Return:
            A string of results on the meta file after finished check.
    
    '''
    code_output = "%s%s" % (CodeType.CHECKER.value, ".o")
    meta_path = "/var/local/lib/isolate/%d/box/meta" % (box_id)
    output = []
    touch_text_file("init", CodeType.META.value, Language.NONE.value, box_id)
    for i in range(test_case_count):
        command = "isolate --time=4 --wall-time=4 -p --full-env --meta='%s' --run -- %s %d.in %d.out %d.ans" % (meta_path, code_output, i+1, i+1, i+1)
        subprocess.call(command, shell=True)
        meta = read_meta(box_id)
        output.append(meta)
    return output