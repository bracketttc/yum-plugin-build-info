"""
Dnf plugin for generating build-info.

This plugin generates or updates a build-info JSON file with the installed
packages as dependencies.
"""

# Copyright 2022 Timothy Brackett

import dnf
import hashlib
import json
import logging
import os
import sys

logger = logging.getLogger("dnf")


class BuildInfoAction(dnf.Plugin):
    name = "build-info"

    def __init__(self, base, cli):
        super(BuildInfoAction, self).__init__(base, cli)

        cli.optparser.add_argument(
            "--build-info",
            dest="bi_file",
            action="store",
            default="build-info.json",
            help="File to store build info data",
        )

        self.myopts, _ = cli.optparser.parse_known_args(sys.argv[1:])
        self.base = base

    def transaction(self):
        hash_algos = ["md5", "sha1", "sha256"]

        ts_info = [
            tsi
            for tsi in self.cli.base.transaction
            if tsi.action in dnf.transaction.FORWARD_ACTIONS
        ]
        # Would it make sense to remove entries from the build-info if we're erasing them?

        build_info = {}

        build_info_file = self.myopts.bi_file

        if os.path.exists(build_info_file):
            with open(build_info_file, "r") as f:
                build_info = json.load(f)
        else:
            build_info = {"dependencies": []}

        # Add all installed packages to JSON
        for tsi in ts_info:
            pkg_id = os.path.basename(tsi.pkg.localPkg())
            already_present = True in (
                dep["id"] == pkg_id for dep in build_info["dependencies"]
            )
            if not already_present:

                package = {"id": pkg_id, "type": "rpm"}

                hashes = [(algo, hashlib.new(algo)) for algo in hash_algos]
                with open(tsi.pkg.localPkg(), mode="rb") as f:
                    buff = f.read(8192)
                    while buff:
                        for _, hasher in hashes:
                            hasher.update(buff)
                        buff = f.read(8192)

                        # add hash value to JSON
                        for algo, hasher in hashes:
                            package[algo] = hasher.hexdigest()

                build_info["dependencies"].append(package)

        # Add dependency information to JSON
        for tsi in ts_info:
            pkg_id = os.path.basename(tsi.pkg.localPkg())
            
            # dedup list
            reqs = set(tsi.pkg.requires)
            deps = []
            for req in reqs:
                for ts in ts_info:
                    if req in ts.pkg.provides or str(req) == ts.pkg.name:
                        deps.append(os.path.basename(ts.pkg.localPkg()))
                        deps.sort()

            for bi_pkg in build_info["dependencies"]:
                if bi_pkg["id"] in deps:
                    if (
                        "requested_by" in bi_pkg
                        and pkg_id not in bi_pkg["requested_by"]
                    ):
                        bi_pkg["requested_by"].append(pkg_id)
                        bi_pkg["requested_by"].sort()
                    else:
                        bi_pkg["requested_by"] = [pkg_id]

        build_info["dependencies"].sort(key=lambda x: x["id"])

        with open(build_info_file, "w") as f:
            json.dump(build_info, f, indent=4, sort_keys=True)

        logger.info("Build info written to {}".format(build_info_file))
