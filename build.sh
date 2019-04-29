#!/bin/sh -e
rm -rf dist deb_dist yaml?expander?*
python3 setup.py --no-user-cfg --command-packages=stdeb.command sdist_dsc --debian-version=000 --verbose --copyright-file copyright.txt -z stable
rm -f deb_dist/*.changes
cd deb_dist/*/
debuild -us -uc -b
