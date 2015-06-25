setuppycheck: A ``setup.py`` checker
====================================

Checks for questionable practices in ``setup.py`` files.

PyPI: https://pypi.python.org/pypi/setuppycheck

Install
-------

.. code-block: bash

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
