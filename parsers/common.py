def add_common_parser_options(parser):
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--top-level", action='store_true', help="""\
Show only top level switches. These filter out all switches that are enabled
by some other switch and that way remove duplicate instances from the output.
""")
    group.add_argument("--unique", action='store_true', help="""\
Show only unique switches.""")
    return parser
