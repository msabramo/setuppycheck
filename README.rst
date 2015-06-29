setuppycheck: A ``setup.py`` checker
====================================

.. image:: https://travis-ci.org/msabramo/setuppycheck.svg?branch=master
    :target: https://travis-ci.org/msabramo/setuppycheck

.. image:: https://img.shields.io/pypi/v/setuppycheck.svg
    :target: https://pypi.python.org/pypi/setuppycheck

.. image:: https://img.shields.io/pypi/wheel/setuppycheck.svg

Checks for questionable practices in ``setup.py`` files.

- PyPI: https://pypi.python.org/pypi/setuppycheck
- GitHub https://github.com/msabramo/setuppycheck

Install
-------

.. code-block:: bash

    $ pip install setuppycheck

Use
---

.. code-block:: bash

    [marca@marca-mac2 setuppycheck]$ setuppycheck examples/exact_pins/setup.py
    WARNING: exact pin: 'requests==2.7.0'
    [marca@marca-mac2 setuppycheck]$ echo $?
    1

    [marca@marca-mac2 setuppycheck]$ setuppycheck examples/reads_requirements_text/setup.py
    WARNING: reads '/Users/marca/dev/git-repos/setuppycheck/examples/reads_requirements_text/requirements.txt' - looks like a requirements file?
      You might want to look at https://caremad.io/2013/07/setup-vs-requirement/
    [marca@marca-mac2 setuppycheck]$ echo $?
    1

Checks
------

- Checks that you are not using exact pins in your `setup.py` file -- Exact pins in `setup.py` get baked into the packages you build and limit flexibility. Folks using your package will have to have that same exact version. If you want to update it, you have to build a new package.

- Checks that you are not reading a `requirements.txt` file and using it to populate `install_requires` in `setup.py`. I think that people mostly do this because they don't understand the differences between `setup.py` and `requirements.txt` so I would advise reading https://caremad.io/2013/07/setup-vs-requirement/
