#!/usr/bin/env bash

cd ~

# Install Java 8 and other tools
sudo apt-get update -y
sudo apt-get install -y software-properties-common python-software-properties
sudo add-apt-repository -y ppa:webupd8team/java
sudo apt-get update -y
sudo apt-get install -y oracle-java8-installer
sudo apt-get install -y ant
sudo apt-get install -y mavenls