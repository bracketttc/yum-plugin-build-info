# DNF/Yum Build Info plugin

A plugin for DNF and Yum that can be used to track installed packages in build-info JSON files.

## Manual installation

Copy the `build-info.conf` file into the Yum/DNF plugin configuration directory.
Copy the `yum-build-info.conf` or `dnf-build-info.conf` file into the plugin directory as `build-info.py`.
See the table below for examples of what those directories are.

| OS  | Plugin path | Config path |
|-----|-------------|-------------|
| RHEL < 8 | `/usr/lib/python/site-packages/yum-plugins/` | `/etc/yum/pluginconf.d/` |
| Fedora 20, 21 | `/usr/lib/python2.7/site-pacakges/yum-plugins/` | `/etc/yum/pluginconf.d/` |
| Fedora 22 | `/usr/lib/python2.7/site-packages/dnf-plugins/` | `/etc/dnf/plugins/` |
| Fedora 23 | `/usr/lib/python3.4/site-packages/dnf-plugins/` | `/etc/dnf/plugins/` |
| Fedora 24 - 25 | `/usr/lib/python3.5/site-packages/dnf-plugins/` | `/etc/dnf/plugins/` |
| RHEL 8, Fedora 26 - 28 | `/usr/lib/python3.6/site-packages/dnf-plugins/` | `/etc/dnf/plugins/` |
| Fedora 29 - 31 | `/usr/lib/python3.7/site-packages/dnf-plugins/` | `/etc/dnf/plugins/` |
| Fedora 32 | `/usr/lib/python3.8/site-packages/dnf-plugins/` | `/etc/dnf/plugins/` |
| RHEL 9, Fedora 33 - 34 | `/usr/lib/python3.9/site-packages/dnf-plugins/` | `/etc/dnf/plugins/` |
| Fedora 35 - | `/usr/lib/python3.10/site-packages/dnf-plugins/` | `/etc/dnf/plugins/` |

## RPM creation

For DNF-based systems, you need to have `python3-rpm-macros` installed.
Running `make` should be sufficient to create the RPM for your current platform.

## Usage

```sh
$ dnf install vim --build-info build-info.json
...
Build info written to build-info.json

Installed:
  ...

Complete!
$
```

### Example output

```json
{
  "dependencies": [
    {
      "id": "vim-common-8.2.2637-16.el9_0.3.x86_64.rpm",
      "md5": "982ca52a23fa81cc7670a6acadc3d4b7",
      "requested_by": [
        "vim-enhanced-8.2.2637-16.el9_0.3.x86_64.rpm"
      ],
      "sha1": "8b62406bbaf6de48981e63c47d6852bfe79be4c7",
      "sha256": "6e7d98f4d84500871ad227a9b0ef481900c379f7076119e0ac4a14309bf44a3a",
      "type": "rpm"
    },
    {
      "id": "vim-enhanced-8.2.2637-16.el9_0.3.x86_64.rpm",
      "md5": "b0ab9e0572fedd508d8fb85524bdafcf",
      "sha1": "2fccd4d842c2b9a73fa0176d4b12366879d05ab8",
      "sha256": "610568f0135cb3de20c80a3d6dd671f97d3d38fe1f2bbf35a6b1a1d4a4de5e92",
      "type": "rpm"
    },
    {
      "id": "vim-filesystem-8.2.2637-16.el9_0.3.noarch.rpm",
      "md5": "112c4a0c6b32edbb8b8f65e683d21910",
      "requested_by": [
        "vim-common-8.2.2637-16.el9_0.3.x86_64.rpm"
      ],
      "sha1": "baaeccf212791956656d52a0d618af79f77b90ed",
      "sha256": "43bfae850409114cbd80a335be00c998deb3140cb958e77c09575afca712ad18",
      "type": "rpm"
    }
  ]
}
```

### Merging into an existing build-info file

TODO