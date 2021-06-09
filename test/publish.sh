#!/usr/bin/bash

blog_post=$1
blog_folder=$(date -u +"%d%^b%Y")

mkdir $blog_folder
cp $blog_post $blog_folder

scp -i ~/vpn/key -r $blog_folder root@bnsmcx.com:/home/ben/bnsmcx.com/static/content/blog

rm -rf $blog_folder
