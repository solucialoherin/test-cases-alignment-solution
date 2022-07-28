from libraries import csv, configuration
from pathlib import Path
from os import listdir, path, rename
from datetime import datetime
import re
import hashlib


def stdout_log(message):
    print(f"{datetime.now()} INFO {message}.")


def compose_filename_from(issue_key):
    return '_'.join(issue_key.split('-'))


def align_filename_of(item):
    pattern = re.compile(item.split('.')[0])
    target_name = test_cases_name_delta.get(item.split('.')[0])
    aligned_filename = re.sub(pattern, target_name, item)
    return aligned_filename


def child_is_in_naming_delta(child):
    if child.split('.')[0] in test_cases_name_delta.keys():
        return True
    else:
        return False


def align_content_of(abs_path_to_the_child):
    alignment = False
    try:
        with open(abs_path_to_the_child, 'r') as child:
            cached_child = child.read()
            cached_child_hexdigest = int(hashlib.sha512(bytes(cached_child, encoding='utf-8')).hexdigest(), 16)
        cached_aligned_child = cached_child
        for key, value in test_cases_name_delta.items():
            if key != '':
                pattern_split = key.split('_')
                pattern = f"\\b{pattern_split[0]}[-_]{pattern_split[1]}\\b"
                if re.search(pattern, cached_aligned_child) is not None:
                    stdout_log(pattern)
                    cached_aligned_child = re.sub(pattern, value, cached_aligned_child)
                else:
                    cached_aligned_child = cached_aligned_child
        if cached_child_hexdigest != int(hashlib.sha512(bytes(cached_aligned_child, encoding='utf-8')).hexdigest(), 16) and cached_aligned_child != '':
            stdout_log(f"content coincidence detected. {abs_path_to_the_child} will be re-written.")
            with open(abs_path_to_the_child, 'w') as output:
                output.write(cached_aligned_child)
            alignment = True
            return alignment
        else:
            stdout_log(f"content coincidence is not detected. {abs_path_to_the_child} stays untouched")
            return alignment
    except UnicodeDecodeError as codec_error:
        stdout_log(f"can't read {abs_path_to_the_child}. {codec_error}")


def path_walker(cwd):
    """
    Recursive pathfinder.

    Searches for *.py inside child sub-dirs of ../this-repo.git.
    """
    for child in listdir(cwd):
        try:
            if path.isdir(path.join(cwd, child)) and child == DEFAULT_SECTION['RepoName']:
                continue
            elif path.isdir(path.join(cwd, child)) and child != DEFAULT_SECTION['RepoName']:
                path_walker(path.join(cwd, child))
            elif path.isfile(path.join(cwd, child)) and child.endswith('.py') and child.startswith('$') is False:
                stdout_log(f"processing {path.join(cwd, child)}. looking inside")
                align_content_of(path.abspath(path.join(cwd, child)))
                stdout_log(f"filename analysis: {path.join(cwd, child)}")
                if child_is_in_naming_delta(child) is True:
                    # Trying to rename test case, i.e. QAP_123.py --> QAP_T456.py
                    aligned_child_filename = align_filename_of(child)
                    stdout_log(f"filename coincidence detected. trying to rename {child} --> {aligned_child_filename}")
                    rename(path.join(cwd, child), path.join(cwd, align_filename_of(child)))
                else:
                    stdout_log(f"filename coincidence is not detected")
        except PermissionError:
            stdout_log(f"can't reach {path.join(cwd, child)} or rename {child}. lack of permission")


if __name__ == "__main__":
    _csv = csv.CSVHandlers(__file__)
    _config_handler = configuration.ConfigurationHandler(__file__)
    DEFAULT_SECTION = _config_handler.read_section_by('DEFAULT')
    issue_keys_delta = _csv.key_pair_build()
    test_cases_name_delta = {}
    for key, value in issue_keys_delta.items():
        test_cases_name_delta[compose_filename_from(key)] = compose_filename_from(value)
    path_walker(Path.cwd().parent)
