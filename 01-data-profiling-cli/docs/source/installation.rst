Installation & Supported Formats
================================

Dependencies
------------

- **Python 3.11+**  
- **Poetry** (for development & docs):  
  .. code-block:: bash

     pip install poetry

- **Sphinx** + Read-the-Docs theme: pulled in via

  .. code-block:: bash

     poetry install --with docs

Supported Input Formats
-----------------------

- **CSV** (default)  
- **Parquet** (`.parquet`, `.pq`; requires `pyarrow` or `fastparquet`)  
- **Excel** (`.xls`, `.xlsx`; requires `openpyxl`)

Example
-------

.. code-block:: bash

   # From PyPI
   pip install dataprof

   # Or install with all extras
   pip install "dataprof[validation]"
