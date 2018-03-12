SublimeLinter-contrib-avr-arduino
================================

[![Build Status](https://travis-ci.org/ChisholmKyle/SublimeLinter-contrib-avr-arduino.svg?branch=master)](https://travis-ci.org/ChisholmKyle/SublimeLinter-contrib-avr-arduino)

This linter plugin for [SublimeLinter](https://github.com/SublimeLinter/SublimeLinter) provides an interface to [avr-gcc](http://www.atmel.com/webdoc/AVRLibcReferenceManual/overview_1overview_gcc.html) with compiler options for Arduino boards. It will be used with files that have the “C/C++” syntax. This linter is based on [SublimeLinter-contrib-avr-gcc](https://packagecontrol.io/packages/SublimeLinter-contrib-avr-gcc).

## Installation

SublimeLinter must be installed in order to use this plugin.

Please use [Package Control](https://packagecontrol.io) to install the linter plugin.

### Install `avr-gcc`

Before using this plugin, you must ensure that `avr-gcc` is installed on your system. To install `avr-gcc`, do can do the following:

#### Linux

1. Install `avr-gcc` with your distro's package manager. On Ubuntu, for example, type the following in a terminal:

    sudo apt-get install git gcc-avr

#### Mac

1. Install and update [Macports](https://www.macports.org/)
2. Type the following in a terminal:

    sudo port install avr-gcc

#### Windows

1. Download and extract the [Amtel AVR Toolchain for Windows](http://www.atmel.com/tools/atmelavrtoolchainforwindows.aspx).

### Configure PATH

In order for `avr-gcc` to be executed by SublimeLinter, you must ensure that its path is available to SublimeLinter. The docs cover [troubleshooting PATH configuration](http://sublimelinter.readthedocs.io/en/latest/troubleshooting.html#finding-a-linter-executable).

## Settings

- SublimeLinter settings: http://sublimelinter.readthedocs.org/en/latest/settings.html
- Linter settings: http://sublimelinter.readthedocs.org/en/latest/linter_settings.html

Additional SublimeLinter-contrib-avr-gcc settings:

|Setting|Description|
|:------|:----------|
|arduino_root|Root installation directory for Arduino.|
|include_dirs|A list of directories to be added to the header search paths (-I is not needed).|
|extra_flags|A string with extra flags to pass to avr-arduino. These should be used carefully, as they may cause linting to fail.|
|arduino-root|Root Arduino directory.|
|arduino-libs|List of core Arduino libraries.|
|board|Arduino board name to lint.|

In project-specific settings, '${project_folder}' can be used to specify a relative path. Here is an example of project settings for development on an Arduino Mini Pro 5V:

```
"SublimeLinter":
{
    "linters":
    {
        "avrgcc": {
            "include_dirs": [
                "${project_folder}/include"
            ],
            "extra_flags": "-pedantic -Wextra",
            "extra_cflags": "-std=gnu99",
            "extra_cxxflags": "-std=gnu++14",
            "arduino-root": "/Applications/Arduino.app/Contents/Java",
            "board": "Uno",
            "arduino-libs": ["Wire", "EEPROM"]
        }
    }
},
```

## Contributing
If you would like to contribute enhancements or fixes, please do the following:

1. Fork the plugin repository.
1. Hack on a separate topic branch created from the latest `master`.
1. Commit and push the topic branch.
1. Make a pull request.
1. Be patient.  ;-)

Please note that modifications should follow these coding guidelines:

- Indent is 4 spaces.
- Code should pass flake8 and pep257 linters.
- Vertical whitespace helps readability, don’t be afraid to use it.
- Please use descriptive variable names, no abbreviations unless they are very well known.

Thank you for helping out!
