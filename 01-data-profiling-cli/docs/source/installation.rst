Installation & Supported Formats
================================

Dependencies
------------

- **Python 3.11+**  
- **Poetry** (for dev & docs): `pip install poetry`  
- **Sphinx** + RTD theme: pulled in via `poetry install --with docs`

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

   # Or with full extras
   pip install dataprof[validation]



