crm
***

Django CRM application


717-django-mptt
===============

.. todo:: Convert ticket ``crm_contact`` to ``contact``.

.. todo:: Make ``contact`` a non-blank foreign key.

.. todo:: Remove ``UserContact``.  We are not using it at present.

::

  0003_auto_20150704_0036.py            # mptt
  0004_auto_20150713_0801.py            # rename contact to crm_contact on ticket and usercontact
  0005_auto_20151220_2043.py            # add new contact to ticket and usercontact
  0006_contactcrm.py                    # new ContactCrm table
  0007_auto_20160124_1748.py            # move old contact to new contact

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
