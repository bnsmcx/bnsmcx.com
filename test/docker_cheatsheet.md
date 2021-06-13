# Docker Cheatsheet

## Simple commands for each use case, all pointing at a common shared folder

## Parrot shell
sudo docker run -it --network host -v $PWD/share:/share parrotsec/security

## OpenVAS
sudo docker run --network host -d -p 443:443 -v $PWD/share:/share -e OV_PASSWORD=admin --name openvas mikesplain/openvas
sudo docker run -it --network host -v $PWD/share:/share -d -p 443:443 --name openvas mikesplain/openvas

## Rustscan
sudo docker run -it --network host -v $PWD/parrot:/work cmnatic/rustscan:debian-buster

