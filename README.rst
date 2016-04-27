crm
***

Django CRM application

Install
=======

Virtual Environment
-------------------

::

  virtualenv --python=python3 venv-crm
  source venv-crm/bin/activate
  pip install --upgrade pip

  pip install -r requirements/local.txt

Testing
=======

::

  find . -name '*.pyc' -delete
  py.test -x

Usage
=====

::

  ./init_dev.sh

Release
=======

https://www.kbsoftware.co.uk/docs/
