# Ductus core #

### What is this repository for? ###

Contain wrappers for common linux tools and is mainly used with the Ductus project.

### How do I get set up? ###

To run the code make sure that the following softwares are  installed:
* python (3.10 or later)
* netcat
* ping
* rsync

### Development and unittesting
To be able to run the unittests in ductus-core/tests a virtual environment needs to be created and ducuts-core needs to be installed.

#### Create virtual environment in ductus-core.
- apt install python3.12-venv
- python3 -m venv venv
- source venv/bin/activate

#### Install ductus-core and additional dependencies
- pip3 install -e .
- pip3 install -r requirements.txt

#### Run the tests
The tests must be run from the repository root, the test fixtures are referenced by relative path.
- pytest

This runs the unittests in ductus-core/tests and the doctest examples in the ductus/ docstrings.
