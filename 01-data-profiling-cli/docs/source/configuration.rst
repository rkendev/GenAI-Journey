Configuration via YAML
======================

You can override any of `ProfileReport`’s parameters by passing `--config config.yaml`.

Sample `config.yaml`
--------------------

.. code-block:: yaml

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

Usage
-----

.. code-block:: bash

   dataprof profile data.csv \
     --config config.yaml \
     --minimal \
     --out custom-reports/
