#!/bin/sh

#
# Create a RPM from last stable version or other if setted
# This script need have installed git, sed, rpmdevtools and curl
#
# Author: Rodrigo Ramírez Norambuena <a@rodrigoramirez.com>
#

# config
BRANCH=stable
REPO="https://github.com/roramirez/qpanel.git"
URL_STABLE_VERSION="https://raw.githubusercontent.com/roramirez/qpanel/$BRANCH/VERSION"

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


VERSION_STABLE=$(curl $URL_STABLE_VERSION)
CLONE_DIR="/tmp/qpanel-$VERSION_STABLE"
FILE_TAR="qpanel-$VERSION_STABLE.tar.gz"
if [ -d "$CLONE_DIR" ]; then
  cd $CLONE_DIR
  git pull
else
  git clone -b $BRANCH $REPO $CLONE_DIR
fi

cd $CLONE_DIR
git submodule init
git submodule update
pybabel compile -d translations

cd /tmp
tar  cvfz $FILE_TAR qpanel-$VERSION_STABLE

rpmdev-setuptree
cd
cp /tmp/$FILE_TAR rpmbuild/SOURCES
cd rpmbuild
cp $CLONE_DIR/samples/elastix/elastix-qpanel.spec elastix-qpanel.spec
sed -i s/"Version: *.*.*"/"Version: $VERSION_STABLE"/g  elastix-qpanel.spec
rpmbuild -v -bb elastix-qpanel.spec
