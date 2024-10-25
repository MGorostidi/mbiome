#!/usr/bin/env bash
b=`dirname $0`
basedir=`readlink -f $b`
export PATH=$basedir/mgpp.dist:$PATH
$basedir/mgpp.dist/mgpp $*
