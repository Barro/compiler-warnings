#!/usr/bin/env python2

from __future__ import print_function

import argparse
import antlr4
import sys
import GccOptionsLexer
import GccOptionsListener
import GccOptionsParser

STATE_COMMENT = 1
STATE_OPTION_NAME = 2
STATE_OPTION_ATTRIBUTES = 3
STATE_OPTION_DESCRIPTION = 4
STATE_NEWLINE = 5

BORING_OPTIONS = set(["Variable", "Enum", "EnumValue"])


def parse_warning_blocks(fp):
    blocks = []
    state = STATE_COMMENT
    for line in fp:
        line = line.rstrip("\n")
        if state == STATE_OPTION_DESCRIPTION and line != "":
            continue

        if state == STATE_OPTION_DESCRIPTION and line == "":
            state = STATE_NEWLINE
            continue

        if state == STATE_NEWLINE:
            if line.startswith(";"):
                state == STATE_COMMENT
                continue
            if line == "":
                continue
            option_name = line
            state = STATE_OPTION_NAME
            continue

        if state == STATE_COMMENT:
            if line.startswith(";"):
                continue
            if line == "":
                state = STATE_NEWLINE
                continue

        if state == STATE_OPTION_NAME:
            state = STATE_OPTION_DESCRIPTION
            if option_name in BORING_OPTIONS:
                continue
            # if not option_name.startswith("W"):
            #     continue
            option_attributes = line
            blocks.append((option_name, option_attributes))
            continue
    return blocks


def apply_listener(string_value, listener):
    string_input = antlr4.InputStream(string_value)
    lexer = GccOptionsLexer.GccOptionsLexer(string_input)
    stream = antlr4.CommonTokenStream(lexer)
    parser = GccOptionsParser.GccOptionsParser(stream)
    tree = parser.optionAttributes()
    walker = antlr4.ParseTreeWalker()
    walker.walk(listener, tree)


class VariableAssignmentListener(GccOptionsListener.GccOptionsListener):
    """
    >>> listener = VariableAssignmentListener()
    >>> apply_listener("Var(varname)", listener)
    >>> listener.variable_name
    u'varname'
    """

    def __init__(self):
        self.variable_name = None
        self._last_name = None

    def enterVariableName(self, ctx):
        self._last_name = ctx.getText()

    def enterAtom(self, ctx):
        if self._last_name == "Var":
            self.variable_name = ctx.getText()

    def exitTrailer(self, ctx):
        self._last_name = None


class AliasAssignmentListener(GccOptionsListener.GccOptionsListener):
    """
    >>> listener = AliasAssignmentListener()
    >>> apply_listener("Alias(Wall)", listener)
    >>> listener.alias_name
    u'Wall'
    >>> listener = AliasAssignmentListener()
    >>> apply_listener("Alias(Wformat=,1,0)", listener)
    >>> listener.alias_name
    u'Wformat=1'
    """

    def __init__(self):
        self.alias_name = None
        self._last_name = None
        self._argument_id = 0

    def enterVariableName(self, ctx):
        self._last_name = ctx.getText()
        self._argument_id = 0

    def enterArgument(self, ctx):
        self._argument_id += 1

    def enterAtom(self, ctx):
        if self._last_name == "Alias" and self._argument_id == 1:
            self.alias_name = ctx.getText()
        if self._last_name == "Alias" and self._argument_id == 2:
            self.alias_name += ctx.getText()

    def exitTrailer(self, ctx):
        self._last_name = None


class LanguagesEnabledListener(GccOptionsListener.GccOptionsListener):
    """
    Listens to LangEnabledBy(languagelist,warningflags) function calls

    "warningflags" are the most interesting ones, as it means that this warning
    is enabled by another flag.

    >>> listener = LanguagesEnabledListener()
    >>> apply_listener("LangEnabledBy(C C++,Wall,0,1)", listener)
    >>> listener.flags
    [u'Wall']

    >>> listener = LanguagesEnabledListener()
    >>> apply_listener("LangEnabledBy(C C++,Wall99,0,1)", listener)
    >>> listener.flags
    [u'Wall99']

    >>> listener = LanguagesEnabledListener()
    >>> apply_listener("LangEnabledBy(C C++,Wall || Wc++-compat)", listener)
    >>> listener.flags
    [u'Wall', u'Wc++-compat']
    """

    def __init__(self):
        self._last_name = None
        self._argument_id = 0
        self.flags = []

    def enterVariableName(self, ctx):
        if ctx.getText() == "LangEnabledBy":
            self._last_name = "LangEnabledBy"
            self._argument_id = 0

    def enterArgument(self, ctx):
        self._argument_id += 1

    def enterAtom(self, ctx):
        if self._last_name == "LangEnabledBy" and self._argument_id == 2:
            flag_name = ctx.getText()
            self.flags.append(flag_name)

    def exitTrailer(self, ctx):
        self._last_name = None


class EnabledByListener(GccOptionsListener.GccOptionsListener):
    """
    Listens to EnabledBy(warningflag) function calls

    >>> listener = EnabledByListener()
    >>> apply_listener("EnabledBy(Wextra)", listener)
    >>> listener.enabled_by
    u'Wextra'
    """

    def __init__(self):
        self._last_name = None
        self.enabled_by = None

    def enterVariableName(self, ctx):
        if ctx.getText() == "EnabledBy":
            self._last_name = "EnabledBy"

    def enterAtom(self, ctx):
        if self._last_name == "EnabledBy":
            self.enabled_by = ctx.getText()

    def exitTrailer(self, ctx):
        self._last_name = None


class WarningOptionListener(GccOptionsListener.GccOptionsListener):
    """
    Searches for Warning attributes.

    >>> listener = WarningOptionListener()
    >>> apply_listener("C C++ Warning", listener)
    >>> listener.is_warning
    True
    """

    def __init__(self):
        self.is_warning = False

    def enterVariableName(self, ctx):
        if ctx.getText() == "Warning":
            self.is_warning = True


def print_enabled_options(references, option_name, level=1):
    for reference in sorted(references.get(option_name, [])):
        print("# " + "  " * level, "-" + reference)
        if reference in references:
            print_enabled_options(references, reference, level + 1)


def parse_options_file(filename, parsing_options={}):
    blocks = parse_warning_blocks(open(filename))

    references = {}
    aliases = {}

    for option_name, option_arguments in blocks:
        # TODO older GCC versions don't have this Warning attribute in
        # their options. Make this conditional and use some heuristics to
        # determine warning options.
        warning_option = WarningOptionListener()
        apply_listener(option_arguments, warning_option)

        if not warning_option.is_warning:
            continue

        if option_name not in references:
            references[option_name] = []

        language_enablers = LanguagesEnabledListener()
        apply_listener(option_arguments, language_enablers)
        for flag in language_enablers.flags:
            if flag not in references:
                references[flag] = []
            references[flag].append(option_name)

        flag_enablers = EnabledByListener()
        apply_listener(option_arguments, flag_enablers)
        if flag_enablers.enabled_by:
            flag = flag_enablers.enabled_by
            if flag not in references:
                references[flag] = []
            references[flag].append(option_name)

        alias_enablers = AliasAssignmentListener()
        apply_listener(option_arguments, alias_enablers)
        if alias_enablers.alias_name is not None:
            aliases[option_name] = alias_enablers.alias_name

    return references, aliases


def print_warning_flags(references, aliases):
    for option_name in sorted(references.keys()):
        if option_name in aliases:
            print("-" + option_name, "=", "-" + aliases[option_name])
        else:
            print("-" + option_name)
        print_enabled_options(references, option_name)


def main(argv):
    parser = argparse.ArgumentParser(description="""\
Parses GCC option files for warning options.""")
    parser.add_argument("option_file", metavar="option-file", nargs="+")
    args = parser.parse_args(argv[1:])

    all_references = {}
    all_aliases = {}

    for filename in args.option_file:
        file_references, file_aliases = parse_options_file(filename)
        for flag, reference in file_references.items():
            references = all_references.get(flag, set([]))
            all_references[flag] = references.union(reference)
        for flag, alias in file_aliases.items():
            if flag in all_aliases:
                assert(all_aliases[flag] == alias)
            all_aliases[flag] = alias

    print_warning_flags(all_references, all_aliases)

if __name__ == "__main__":
    main(sys.argv)
