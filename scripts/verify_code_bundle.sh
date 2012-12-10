#!/bin/bash

script=$(readlink -f $0)
basedir=`dirname $script`

rm -rf ${basedir}/../dist/

python setup.py sdist

cd ${basedir}/../dist/
tar -xzvf *.tar.gz

# Make sure cacert.pem is included
if [ ! -f ${basedir}/../dist/service-registry-cli-*/service_registry_cli/data/cacert.pem ]; then
    echo "cacert.pem doesn't exist"
    exit 1
fi

echo "All the necessary files are present"
exit 0
