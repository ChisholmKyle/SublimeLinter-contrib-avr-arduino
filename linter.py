#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by Kyle Chisholm
# Copyright (c) 2016 Kyle Chisholm
#
# License: MIT
#

"""This module exports the AvrGcc plugin class."""

import shlex
from SublimeLinter.lint import Linter, util, persist
import sublime
import os
import string


def arduino_flags(board):
    extra_flags = ' -Os -DARDUINO_ARCH_AVR '
    if board == 'Uno':
        extra_flags += '-mmcu=atmega328p -DF_CPU=16000000L -DARDUINO_AVR_UNO '
    elif  board == 'ProMini5V328':
        extra_flags += '-mmcu=atmega328p -DF_CPU=16000000L -DARDUINO_AVR_PRO '
    elif  board == 'ProMini5V168':
        extra_flags += '-mmcu=atmega168 -DF_CPU=16000000L -DARDUINO_AVR_PRO '
    elif  board == 'ProMini3V328':
        extra_flags += '-mmcu=atmega328p -DF_CPU=8000000L -DARDUINO_AVR_PRO '
    elif  board == 'ProMini3V168':
        extra_flags += '-mmcu=atmega168 -DF_CPU=8000000L -DARDUINO_AVR_PRO '
    elif board == 'Mega1280':
        extra_flags += '-mmcu=atmega1280 -DF_CPU=16000000L -DARDUINO_AVR_MEGA '
    elif board == 'Mega2560':
        extra_flags += '-mmcu=atmega2560 -DF_CPU=16000000L -DARDUINO_AVR_MEGA2560 '
    return extra_flags


def arduino_include(root, board, corelibs):
    include_dirs = [root + '/hardware/arduino/avr/cores/arduino']
    # boards (variant)
    if board == 'Uno':
        include_dirs.extend([
            root + '/hardware/arduino/avr/variants/standard'
        ])
    elif board == 'ProMini5V328' or \
         board == 'ProMini5V168' or \
         board == 'ProMini3V328' or \
         board == 'ProMini3V168':
        include_dirs.extend([
            root + '/hardware/arduino/avr/variants/eightanaloginputs'
        ])
    elif board == 'Mega1280' or \
         board == 'Mega2560':
        include_dirs.extend([
            root + '/hardware/arduino/avr/variants/mega'
        ])
    # core libraries
    for corelib in corelibs:
        if corelib == 'Wire':
            include_dirs.extend([
                root + '/hardware/arduino/avr/libraries/Wire/src',
                root + '/hardware/arduino/avr/libraries/Wire/src/utility'
            ])
        elif corelib == 'SPI':
            include_dirs.extend([
                root + '/hardware/arduino/avr/libraries/SPI/src'
            ])
        elif corelib == 'EEPROM':
            include_dirs.extend([
                root + '/hardware/arduino/avr/libraries/EEPROM/src'
            ])
    return include_dirs


def get_project_folder():
    """Return the project folder path."""
    proj_file = sublime.active_window().project_file_name()
    if proj_file:
        return os.path.dirname(proj_file)
    # Use current file's folder when no project file is opened.
    proj_file = sublime.active_window().active_view().file_name()
    if proj_file:
        return os.path.dirname(proj_file)
    return '.'


def apply_template(s):
    """Replace "project_folder" string with the project folder path."""
    mapping = {
        "project_folder": get_project_folder()
    }
    templ = string.Template(s)
    return templ.safe_substitute(mapping)


class AvrArduino(Linter):
    """Provides an interface to avr-gcc."""

    syntax = ('c', 'c++', 'c++11')
    executable = 'avr-arduino'

    version_args = '--version'
    version_re = r'(?P<version>\d+\.\d+\.\d+)'
    version_requirement = '>= 4.0'

    # 1. column number, colon and space are only applicable for single line messages
    # 2. several lines of anything followed by
    #    either error/warning/note or newline (= irrelevant backtrace content)
    #    (lazy quantifiers so we don’t skip what we seek)
    # 3. match the remaining content of the current line for output
    regex = (r'<stdin>:(?P<line>\d+):'
             r'((?P<col>\d*): )?'
             r'(.*?((?P<error>error)|(?P<warning>warning|note)|\r?\n))+?'
             r': (?P<message>.+)')

    multiline = True

    defaults = {
        'arduino_root': "",
        'board': 'Uno',
        'arduino_libs': [],
        'include_dirs': [],
        'extra_flags': "",
        'extra_cflags': "",
        'extra_cxxflags': ""
    }

    base_cmd = 'avr-gcc -fsyntax-only -Wall '

    # line_col_base = (1, 1)
    # selectors = {}
    error_stream = util.STREAM_BOTH
    tempfile_suffix = None
    word_re = None
    inline_settings = None
    inline_overrides = None
    comment_re = None

    def cmd(self):
        """
        Return the command line to execute.

        We override this method, so we can add extra flags and include paths
        based on the 'include_dirs' and 'extra_flags' settings.

        """
        settings = self.get_view_settings()

        # setttings
        include_dirs = settings.get('include_dirs', [])
        extra_flags = settings.get('extra_flags', "")

        # arduino settings
        arduino_root = settings.get('arduino_root', "")
        arduino_board = settings.get('board', "")
        arduino_libs = settings.get('arduino_libs', [])

        # arduino
        extra_flags += arduino_flags(arduino_board)
        include_dirs.extend(arduino_include(arduino_root, arduino_board, arduino_libs))

        # append to base command
        result = self.base_cmd
        if persist.get_syntax(self.view) in ['c', 'c improved']:
            result += ' -x c ' + settings.get('extra_cflags', '') + ' '
        elif persist.get_syntax(self.view) in ['c++', 'c++11']:
            result += ' -x c++ ' + settings.get('extra_cxxflags', '') + ' '
        result += apply_template(extra_flags)
        if include_dirs:
            result += apply_template(' '.join([' -I ' + shlex.quote(include) for include in include_dirs]))

        return result + ' -'
