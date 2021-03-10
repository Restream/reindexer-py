#!/usr/bin/env bash

ver1=0
ver2=0
ver3=0
for x in $1
do
	v1=$(echo $x | sed "/[^0-9]*\([0-9]*\)\..*/s//\1/")
	v2=$(echo $x | sed "/[^\.]*\.\([0-9]*\)\..*/s//\1/")
	v3=$(echo $x | sed "/[^\.]*\.[0-9]*\.\([0-9]\)[^0-9].*/s//\1/")
	if [[ $v1 -gt $ver1 || ( $v1 -eq $ver1 && ( $v2 -gt $ver2 || ( $v2 -eq $ver2 && $v3 -gt $ver3 ) ) ) ]]
	then
		ver1=$v1
		ver2=$v2
		ver3=$v3
		filename=$x
	fi
done

echo $filename
