[reSRC.io](http://resrc.io)
========

Indexing and gathering all freely available learning resources.


Installing and running the project
----------------------------------

### Dependencies
* Git
* Python >=2.6
* virtualenv (python2 version)
* [pip](https://github.com/pypa/pip)

### Installation
Run the following commands:

    git clone https://github.com/vhf/resrc.git
    cd resrc
    virtualenv2 -p /usr/bin/python2 venv --distribute
    source venv/bin/activate
    pip install -r requirements.txt
    python2 manage.py syncdb
    python2 manage.py migrate
    python2 manage.py runserver

Then visit <http://127.0.0.1:8000>


Contributing
------------

Fork and work on your own branch, submit pull-requests.

Main work branch is [resrc/master](https://github.com/vhf/resrc/tree/master). Production branch is [resrc/prod](https://github.com/vhf/resrc/tree/prod).


### Running the tests
First, install the requirements_dev : `pip install -r requirements_dev.txt`.

Then, to run the tests, simply run `fab test`. Alternatively, if you want the tests to run
everytime you modify a file, run `./watchmedo.sh`.

Changelog
---------

* 0.8.1 - Less dead code, more tests
* 0.8.0 - Display version in footer
