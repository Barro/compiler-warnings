#!/usr/bin/env python3

import antlr4
import argparse
import common
import sys

import TableGenLexer
import TableGenListener
import TableGenParser


class ClangDiagnosticGroupsListener(TableGenListener.TableGenListener):
    def __init__(self):
        self.currentDefinitionName = None
        self.currentSwitchName = None
        self.currentClassDefinitionName = None
        self.currentReferences = None
        self.switchClassesReferences = {}
        self.switchNames = {}
        self.switchClasses = {}
        self.parentClasses = {}
        self.parentSwitches = {}

    def enterEmptySwitchName(self, ctx):
        if self.currentClassDefinitionName == "DiagGroup":
            self.currentSwitchName = ""

    def enterSwitchText(self, ctx):
        if self.currentClassDefinitionName == "DiagGroup":
            self.currentSwitchName = ctx.getText()

    def enterDefinitionName(self, ctx):
        self.currentDefinitionName = ctx.getText()

    def exitSwitchDefinition(self, ctx):
        self.currentDefinitionName = None

    def exitClassDefinition(self, ctx):
        if self.currentClassDefinitionName == "DiagGroup":
            if self.currentSwitchName is not None:
                self.switchNames[self.currentSwitchName] = (
                    self.currentDefinitionName)
                self.switchClassesReferences[self.currentSwitchName] = (
                    self.currentReferences)
                for reference in self.currentReferences:
                    parents = self.parentClasses.get(reference, [])
                    parents.append(self.currentSwitchName)
                    self.parentSwitches[reference] = parents
            if self.currentDefinitionName:
                self.switchClasses[self.currentDefinitionName] = (
                    self.currentSwitchName)
                for reference in self.currentReferences:
                    parents = self.parentClasses.get(reference, [])
                    parents.append(self.currentDefinitionName)
                    self.parentClasses[reference] = parents
        self.currentSwitchName = None
        self.currentClassDefinitionName = None
        self.currentReferences = None

    def enterClassDefinitionName(self, ctx):
        self.currentClassDefinitionName = ctx.getText()
        if self.currentClassDefinitionName == "DiagGroup":
            self.currentReferences = []

    def enterIdentifierReference(self, ctx):
        self.currentReferences.append(ctx.getText())


def is_dummy_switch(diagnostics, switch_name):
    """Determines if a switch does nothing

    Dummy switch is such switch that has no children and does not
    belong to any class. It should therefore do nothing."""

    class_name = diagnostics.switchNames[switch_name]
    has_class = class_name is not None
    references = diagnostics.switchClassesReferences.get(switch_name, [])
    has_reference = len(references) > 0
    return not (has_class or has_reference)


def create_dummy_text(diagnostics, switch_name):
    if is_dummy_switch(diagnostics, switch_name):
        return " # DUMMY switch"
    return ""


def print_references(diagnostics, switch_name, level):
    references = diagnostics.switchClassesReferences.get(switch_name, [])
    reference_switches = []
    for reference_class_name in references:
        reference_switch_name = diagnostics.switchClasses[reference_class_name]
        reference_switches.append(reference_switch_name)
    for reference_switch_name in sorted(
            reference_switches, key=lambda x: x.lower()):
        dummy_string = create_dummy_text(diagnostics, reference_switch_name)
        print("# %s-W%s%s" % (
            "  " * level, reference_switch_name, dummy_string))
        print_references(diagnostics, reference_switch_name, level + 1)


def is_root_class(diagnostics, switch_name):
    # Root class is something that has parents in neither switches nor classes:
    class_name = diagnostics.switchNames[switch_name]
    has_parent_switch = class_name in diagnostics.parentSwitches
    has_parent_class = class_name in diagnostics.parentClasses
    return not has_parent_switch and not has_parent_class


def main(argv):
    parser = argparse.ArgumentParser(
        description="Clang diagnostics group parser")
    common.add_common_parser_options(parser)
    parser.add_argument("groups_file", metavar="groups-file", help="""\
The path of clang diagnostic groups file.
""")
    args = parser.parse_args(argv[1:])

    string_input = antlr4.FileStream(args.groups_file)
    lexer = TableGenLexer.TableGenLexer(string_input)
    stream = antlr4.CommonTokenStream(lexer)
    parser = TableGenParser.TableGenParser(stream)
    tree = parser.expression()

    diagnostics = ClangDiagnosticGroupsListener()
    walker = antlr4.ParseTreeWalker()
    walker.walk(diagnostics, tree)

    for name in sorted(
            diagnostics.switchNames.keys(), key=lambda x: x.lower()):
        if args.top_level and not is_root_class(diagnostics, name):
            continue
        dummy_string = create_dummy_text(diagnostics, name)
        print("-W%s%s" % (name, dummy_string))
        if args.unique:
            continue
        print_references(diagnostics, name, 1)


if __name__ == "__main__":
    main(sys.argv)
