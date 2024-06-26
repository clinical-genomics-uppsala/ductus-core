# Ductus core #

### What is this repository for? ###

Contain wrappers for common linux tools and is mainly used with the Ductus project.

### How do I get set up? ###

To run the code make sure that the following softwares are  installed:
* python
* netcat
* ping
* rsync

### Development and unittesting
To be able to run the unittests in ductus-core/tests a virtual environment needs to be created and ducuts-core needs to be installed.

#### Create virtual environment in ductus-core.
- apt install python3.10-venv
- python3 -m venv venv
- source venv/bin/activate

For Ubuntu also use the following commands to install dependencies before installing ductus-core with pip3:
- sudo apt-get install gcc
- sudo apt-get install g++ 
- sudo apt-get install python3-dev

#### Install ductus-core and additional dependencies
- pip3 install -e .
- pip install freezegun
