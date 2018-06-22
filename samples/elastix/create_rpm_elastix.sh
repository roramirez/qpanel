#!/bin/sh

#
# Create a RPM from last stable version or other if setted
# This script need have installed git, sed, rpmdevtools and curl
#
# Author: Rodrigo Ramírez Norambuena <a@rodrigoramirez.com>
#

# config
BRANCH=stable
SPEC_FILE=elastix4-qpanel.spec
REPO="https://github.com/roramirez/qpanel.git"
URL_STABLE_VERSION="https://rodrigoramirez.com/qpanel/version/$BRANCH"

if ! [ -x "$(command -v git)" ]; then
  echo "Please install git"
  exit 1
fi

if ! [ -x "$(command -v rpmdev-setuptree)" ]; then
  echo "Please install rpm-build and rpmdevtools"
  exit 1
fi

if ! [ -x "$(command -v curl)" ]; then
  echo "Please install curl"
  exit 1
fi

if ! [ -x "$(command -v npm)" ]; then
  echo "Please install npm"
  exit 1
fi

VERSION_STABLE=$(curl -L $URL_STABLE_VERSION)
CLONE_DIR="/tmp/qpanel-$VERSION_STABLE"
FILE_TAR="qpanel-$VERSION_STABLE.tar.gz"
if [ -d "$CLONE_DIR" ]; then
  cd $CLONE_DIR
  git pull
else
  git clone -b $BRANCH $REPO $CLONE_DIR
fi

cd $CLONE_DIR
pybabel compile -d translations
# Bower
cd $CLONE_DIR
npm install
sudo $CLONE_DIR/node_modules/bower/bin/bower --allow-root install

cd /tmp
tar cvfz $FILE_TAR --exclude=node_modules qpanel-$VERSION_STABLE

rpmdev-setuptree
cd
cp /tmp/$FILE_TAR rpmbuild/SOURCES
cd rpmbuild
cp $CLONE_DIR/samples/elastix/$SPEC_FILE $SPEC_FILE
sed -i s/"Version: *.*.*"/"Version: $VERSION_STABLE"/g  $SPEC_FILE
rpmbuild -v -bb $SPEC_FILE
