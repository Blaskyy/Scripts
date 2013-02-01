#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-
"""%prog [options] arg

Simple script to use KDEs clipboard from the command line.

Copyright (C) 2005-2010 by Armin Straub, http://arminstraub.com
"""

"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
"""

"""
The attached python script clip.py makes it easy to use the KDE clipboard on the command line.

Basic usage

For the following examples it is assumed that the script is available in the search path as clip.

clip
gives the content of the clipboard. You can use the switch -i 2 to obtain historic contents, here item number 2, of the clipboard (note that -i 0 refers to the current content).
clip "some text"
Put "some text" into the clipboard.
ps | clip -
Put the output of some program, here ps, into the clipboard.
Some examples

ssh $(clip)
Connect to the server whose hostname is contained in the clipboard.
clip long_file_name
Use the autocompletion of the shell to copy filenames conveniently to the clipboard.
cat todo | clip -
Copy the content of files, here todo, to the clipboard.
"""

def main():
    """Main program (invoked automatically, when executed)"""
    from optparse import OptionParser
    parser = OptionParser(__doc__, version="0.2.0")

    parser.add_option("-i", "--item", type="int", default=0,
            help="get the Nth item in clipboard history", metavar="N")
    parser.add_option("--strip", action="store_true", default=True,
            help="strip leading or trailing whitespace (default)")
    parser.add_option("-n", "--no-strip", action="store_false", dest="strip",
            help="don't strip leading or trailing whitespace")
    parser.add_option("-x", "--clear", action="store_true", default=False,
            help="clear the clipboard history")

    (options, args) = parser.parse_args()

    if options.clear:
        klipper(["clearClipboardHistory"])
    elif len(args) == 0:
        content = klipper(["getClipboardHistoryItem", options.item])
        if options.strip:
            content = content.strip()
        print content
    else:
        content = " ".join(args)
        if content == "-":
            import sys
            content = sys.stdin.read()
        if options.strip:
            content = content.strip()
        klipper(["setClipboardContents", content])


def klipper(args):
    # if simplycode is available:    
    # from simplycode import run
    # return run("dcop klipper klipper", args, getoutput=True)
    import os, commands
    args = " ".join([commands.mkarg(str(arg)) for arg in args])
    # For KDE3 which uses dcop instead of dbus:
    # s, o = commands.getstatusoutput("dcop klipper klipper " + args)
    s, o = commands.getstatusoutput("qdbus org.kde.klipper /klipper " + args)
    if s == 0:
        return o
    return ""


if __name__ == "__main__":
    main()
