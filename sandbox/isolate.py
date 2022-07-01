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
    touch_text_file("init", CodeType.META.value, Language.NONE.value, box_id=0)
    subprocess.call("isolate --time=2 -p --full-env --meta='%s' --run -- /usr/bin/g++ %s -o %s" % (meta_path, code_path, code_output), shell=True)
    return read_meta(box_id)