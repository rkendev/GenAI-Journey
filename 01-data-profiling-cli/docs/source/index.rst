Welcome to Data Profiling CLI’s documentation!
==============================================

Welcome to the official documentation for Data Profiling CLI—a fast,
extensible command-line interface for profiling tabular data, with
sampling, trend plotting, chunk aggregation, and Great Expectations
integration.

Quickstart
----------

1.  Install:

    .. code-block:: bash

        pip install dataprof

2.  Minimal profiling:

    .. code-block:: bash

        dataprof profile data.csv --minimal --out reports/

3.  Reservoir sampling:

    .. code-block:: bash

        dataprof profile data.csv --reservoir-size 1000 --out reports/

4.  Trend plotting:

    .. code-block:: bash

        dataprof plot-trends --db runs.db

5.  Chunk aggregation:

    .. code-block:: bash

        dataprof aggregate-chunks reports/ --out summary.json


API Reference
-------------

.. toctree::
   :maxdepth: 1

   modules/index


Changelog
---------

.. toctree::
   :maxdepth: 1

   changelog


Contributing
------------

.. toctree::
   :maxdepth: 1

   contributing
