#!/usr/bin/env python

# import the necessary modules
import os

# define the paths
amass_src_path = "/opt/"

# download the latest version of amass
os.system("wget https://github.com/OWASP/Amass/releases/latest/download/amass_linux_arm64.zip")

# unzip the downloaded file
os.system("unzip amass_linux_arm64.zip")

# move the binary file to the bin directory
os.system("mv ./amass_linux_arm64/amass  /opt/amass")

# set the executable permission
os.system("chmod +x " + amass_src_path + "amass")

# install is complete
print("Amass is installed successfully.")