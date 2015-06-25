setuppycheck: A ``setup.py`` checker
====================================

Checks for questionable practices in ``setup.py`` files.

E.g.:

.. code-block: bash

    [marca@marca-mac2 setuppycheck]$ ./setuppycheck.py examples/exact_pins/setup.py
    WARNING: exact pin: 'requests==2.7.0'
    [marca@marca-mac2 setuppycheck]$ echo $?
    1

    [marca@marca-mac2 setuppycheck]$ ./setuppycheck.py examples/reads_requirements_text/setup.py
    WARNING: reads '/Users/marca/dev/git-repos/setuppycheck/examples/reads_requirements_text/requirements.txt' - looks like a requirements file?
      You might want to look at https://caremad.io/2013/07/setup-vs-requirement/
    [marca@marca-mac2 setuppycheck]$ echo $?
    1
