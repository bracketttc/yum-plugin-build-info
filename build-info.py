"""
Yum plugin for generating build-info.

This plugin generates or updates a build-info JSON file with the installed
packages as dependencies.
"""

# Copyright 2022 Timothy Brackett

import hashlib
import json
import os

from yum import config
from yum.plugins import TYPE_CORE

requires_api_version = "2.3"
plugin_type = TYPE_CORE

build_info_file = None

def config_hook(conduit):
    # Add a 'collect_build_info' boolean setting to yum.conf [main]
    config.YumConf.collect_build_info = config.BoolOption(False)

    parser = conduit.getOptParser()
    parser.add_option(
        "",
        "--build-info",
        dest="bi_file",
        action="store",
        default="build-info.json",
        help="File to store build info data"
    )

    parser.add_option(
        "",
        "--module",
        dest="bi_module",
        action="store",
        help=""
    )


def pretrans_hook(conduit):
    hash_algos = ["md5", "sha1", "sha256"]

    opts, _ = conduit.getCmdLine()
    global build_info_file
    build_info_file = opts.bi_file

    ts_info = conduit.getTsInfo()

    build_info = {}

    if os.path.exists( build_info_file ):
        with open( build_info_file, 'r' ) as f:
            build_info = json.load( f )
    else:
        build_info = {"dependencies": []}

    # Add all installed packages to JSON
    for key, (pkg,) in ts_info.pkgdict.iteritems():
        package = {"id": os.path.basename(pkg.po.localpath), "type": "rpm"}

        for algo, hashsum, _ in pkg.po.checksums:
            if algo in hash_algos:
                package[algo] = hashsum

        # Hash file
        missing_hashes = [
            (algo, hashlib.new(algo))
            for algo in hash_algos
            if algo not in package.keys()
        ]
        if missing_hashes:
            with open(pkg.po.localpath, mode="rb") as f:
                buff = f.read(8192)
                while buff:
                    for _, hasher in missing_hashes:
                        hasher.update(buff)
                    buff = f.read(8192)

                # add hash value to JSON
                for algo, hasher in missing_hashes:
                    package[algo] = hasher.hexdigest()

        build_info["dependencies"].append(package)

    # Add dependency information to JSON
    for key, (pkg,) in ts_info.pkgdict.iteritems():
        if len(pkg.depends_on) > 0:
            pkg_id = os.path.basename(pkg.po.localpath)
            # dedup list
            deps = set(pkg.depends_on)
            deps = [os.path.basename(dep.localpath) for dep in deps]
            for dep in deps:
                for bi_pkg in build_info["dependencies"]:
                    if bi_pkg["id"] == pkg_id:
                        if bi_pkg.has_key("requested_by"):
                            bi_pkg["requested_by"].append(dep)
                            bi_pkg["requested_by"].sort()
                        else:
                            bi_pkg["requested_by"] = [dep]

    build_info["dependencies"].sort(key=lambda x: x["id"])

    with open( build_info_file, 'w' ) as f:
        json.dump( build_info, f, indent=4, sort_keys=True)

def close_hook(conduit):
    global build_info_file
    if build_info_file:
        conduit.info( 2 , "Build info written to {}".format( build_info_file ) )