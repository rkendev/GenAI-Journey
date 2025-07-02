dataprof package
=================

The **dataprof** package provides a simple CLI for profiling tabular data
(CSV, Parquet, Excel), with sampling, reservoir sampling, chunked reports,
trend plotting, and Great Expectations stubs.

.. automodule:: dataprof
   :members:
   :undoc-members:
   :show-inheritance:

Submodules
----------

dataprof.cli module
-------------------

This module implements the CLI entry points for:

- **profile**: ingest data, sample, generate per-chunk JSON summaries and a final HTML/JSON report (with optional GE stub).  
- **plot-trends**: plot duration vs. sample‐fraction based on recorded runs.  
- **aggregate-chunks**: merge all per-chunk JSON profiles into a single summary.

.. automodule:: dataprof.cli
   :members:
   :undoc-members:
   :show-inheritance:
