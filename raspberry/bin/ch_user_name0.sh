#!/bin/sh
useradd -M tmp
gpasswd -a tmp sudo
sudo passwd tmp
