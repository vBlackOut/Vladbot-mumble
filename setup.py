#!/usr/bin/env python2

from distutils.core import setup
from sftbot import VERSION
from sys import version_info
from os import path

if version_info[0] != 2:
    print("use python2 to install vladbot")
    exit(1)

pb_filename = path.join(path.dirname(__file__),
                        "vladbot/protobuf/Mumble_pb2.py")
if not path.isfile(pb_filename):
    print("Mumble_pb2.py has not been generated yet.\nrun make first.")
    exit(1)

setup(
    name="vladbot",
    version=VERSION,
    description="Mumble text bridge",
    long_description="Mumble channel. Buil to be easily extendable to more " +
                     "protocols and uses.\n" +
                     "Repo: https://github.com/SFTtech/vladbot",
    author="Vladimir Souchet (see COPYING for contributors)",
    author_email="vladimir.souchet@cuby-hebergs.com",
    url="https://github.com/SFTtech/vladbot",
    license="GPLv3+",
    packages=["vladbot", "vladbot/protobuf"],
    scripts=["bin/vladbot"],
    classifiers=[
        "Environment :: Console",
        "License :: OSI Approved :: " +
        "GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Topic :: Communications :: Chat :: Internet Relay Chat",
        "Topic :: Communications :: Telephony",
    ],
)
