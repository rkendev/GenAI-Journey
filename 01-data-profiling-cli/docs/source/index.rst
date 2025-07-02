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

Configuration
-------------

You can customize your profiling report via a YAML file:

.. code-block:: yaml

   # config.yaml
   title: "🔍 Custom Data Profiler Report"
   explorative: false
   minimal: true
   pool_size: 2
   progress_bar: false
   correlations:
     pearson:
       calculate: true
     spearman:
       calculate: true
   missing_diagrams:
     bar: true
     matrix: true
     heatmap: false

Example:

.. code-block:: bash

   dataprof profile data.csv \
     --config config.yaml \
     --minimal \
     --out demo-config

.. toctree::
   :maxdepth: 2

   installation
   configuration
   modules/index
   changelog
   contributing
