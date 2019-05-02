#!/bin/sh -e
rm -rf dist deb_dist yaml?expander?*
python3 setup.py --no-user-cfg --command-packages=stdeb.command sdist_dsc --debian-version=dbc$BUILD_NUMBER --verbose --copyright-file copyright.txt -z stable
rm -f deb_dist/*.changes
cd deb_dist/*/

unexpand >>debian/rules <<EOT

override_dh_python3:
        dh_python3 -O--buildsystem=pybuild
        sed -i 's/^\(python3:Depends=.*\)/\1, python3-yaml/' debian/python3-yaml-expander.substvars
        cat debian/python3-yaml-expander.substvars
EOT

debuild -us -uc -b
