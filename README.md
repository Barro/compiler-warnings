# C/C++ compiler warning flags collection and parser

This project includes tools and lists to figure out all warning flags
that [clang compiler](http://clang.llvm.org/) and
[GNU Compiler Collection](https://gcc.gnu.org/) have. This also shows
all aliases and warning flags that a certain flag enables (prefixed
with "#" character) so that you can easily see which flag is enabled
by what.

The purpose of these collections is to make it more easy to use the
static code analysis tools that compilers provide.

## Clang warning flags

* [clang 3.2 warnings](warnings-clang-3.2.txt)
* [clang 3.3 warnings](warnings-clang-3.3.txt)
* [clang 3.4 warnings](warnings-clang-3.4.txt)
* [clang 3.5 warnings](warnings-clang-3.5.txt)
* [clang 3.6 warnings](warnings-clang-3.6.txt)
* [clang 3.7 warnings](warnings-clang-3.7.txt)

## GCC warning flags

If you need a full list of
[GCC warning options](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html),
for a specific version of GCC that you have, you can run GCC with `gcc
--help=warnings` to get that list. Otherwise some plain (currently
incomplete in edge cases) GCC warning options lists are available
below:

* [GCC 3.4 warnings](warnings-gcc-3.4.txt) (first GCC with domain
  specific language options file)
* [GCC 4.0 warnings](warnings-gcc-4.0.txt)
* [GCC 4.1 warnings](warnings-gcc-4.1.txt)
* [GCC 4.2 warnings](warnings-gcc-4.2.txt)
* [GCC 4.3 warnings](warnings-gcc-4.3.txt)
* [GCC 4.4 warnings](warnings-gcc-4.4.txt)
* [GCC 4.5 warnings](warnings-gcc-4.5.txt)
* [GCC 4.6 warnings](warnings-gcc-4.6.txt)
* [GCC 4.7 warnings](warnings-gcc-4.7.txt)
* [GCC 4.8 warnings](warnings-gcc-4.8.txt)
* [GCC 4.9 warnings](warnings-gcc-4.9.txt)
* [GCC 5.1 warnings](warnings-gcc-5.1.txt) (first 5.x series GCC)
* [GCC 5.2 warnings](warnings-gcc-5.2.txt)
* [GCC 5.3 warnings](warnings-gcc-5.3.txt)

# Requirements

This uses [ANTLR](http://www.antlr.org/) as a parser generator with
some supporting Python code to parse warning flags from actual
compiler option data files. Other requirements are following (plus
their dependencies):

* [make](http://www.gnu.org/software/make/)
* [ANTLR4](http://www.antlr.org/)
* [Python 2.7](https://www.python.org/)
* [antlr4-python2-runtime](https://pypi.python.org/pypi/antlr4-python2-runtime/)

# Usage

After you have installed all the requirements and are able to run
ANTLR with `antlr4` command, just use following commands:

    make
    ./parse-clang-diagnostic-groups.py <path-to-clang-source>/include/clang/Basic/DiagnosticGroups.td
    ./parse-gcc-warning-options.py <path-to-gcc-source>/gcc/gcc/c-family/c.opt

And you'll get the list of all individual warning flags and their
dependencies that are in the requested compiler version.

