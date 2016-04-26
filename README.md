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

* clang 3.2 [all](clang/warnings-clang-3.2.txt)
  [top level](clang/warnings-clang-top-level-3.2.txt)
  [unique](clang/warnings-clang-unique-3.2.txt)
* clang 3.3 [all](clang/warnings-clang-3.3.txt)
  [top level](clang/warnings-clang-top-level-3.3.txt)
  [unique](clang/warnings-clang-unique-3.3.txt)
  [diff](clang/warnings-clang-diff-3.2-3.3.txt)
* clang 3.4 [all](clang/warnings-clang-3.4.txt)
  [top level](clang/warnings-clang-top-level-3.4.txt)
  [unique](clang/warnings-clang-unique-3.4.txt)
  [diff](clang/warnings-clang-diff-3.3-3.4.txt)
* clang 3.5 [all](clang/warnings-clang-3.5.txt)
  [top level](clang/warnings-clang-top-level-3.5.txt)
  [unique](clang/warnings-clang-unique-3.5.txt)
  [diff](clang/warnings-clang-diff-3.4-3.5.txt)
* clang 3.6 [all](clang/warnings-clang-3.6.txt)
  [top level](clang/warnings-clang-top-level-3.6.txt)
  [unique](clang/warnings-clang-unique-3.6.txt)
  [diff](clang/warnings-clang-diff-3.5-3.6.txt)
* clang 3.7 [all](clang/warnings-clang-3.7.txt)
  [top level](clang/warnings-clang-top-level-3.7.txt)
  [unique](clang/warnings-clang-unique-3.7.txt)
  [diff](clang/warnings-clang-diff-3.6-3.7.txt)
* clang 3.8 [all](clang/warnings-clang-3.8.txt)
  [top level](clang/warnings-clang-top-level-3.8.txt)
  [unique](clang/warnings-clang-unique-3.8.txt)
  [diff](clang/warnings-clang-diff-3.7-3.8.txt)

## GCC warning flags

If you need a full list of
[GCC warning options](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html),
for a specific version of GCC that you have, you can run GCC with `gcc
--help=warnings` to get that list. Otherwise some plain (currently
incomplete in edge cases) GCC warning options lists are available
below:

* [GCC 3.4 warnings](gcc/warnings-gcc-3.4.txt) (first GCC with domain
  specific language options file)
* [GCC 4.0 warnings](gcc/warnings-gcc-4.0.txt)
* [GCC 4.1 warnings](gcc/warnings-gcc-4.1.txt)
* [GCC 4.2 warnings](gcc/warnings-gcc-4.2.txt)
* [GCC 4.3 warnings](gcc/warnings-gcc-4.3.txt)
* [GCC 4.4 warnings](gcc/warnings-gcc-4.4.txt)
* [GCC 4.5 warnings](gcc/warnings-gcc-4.5.txt)
* [GCC 4.6 warnings](gcc/warnings-gcc-4.6.txt)
* [GCC 4.7 warnings](gcc/warnings-gcc-4.7.txt)
* [GCC 4.8 warnings](gcc/warnings-gcc-4.8.txt)
* [GCC 4.9 warnings](gcc/warnings-gcc-4.9.txt)
* [GCC 5.x warnings](gcc/warnings-gcc-5.txt) (covers GCC 5.1, 5.2, 5.3)

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

