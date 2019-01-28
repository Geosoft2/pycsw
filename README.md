pycsw enhancement for geospatial similarity calculation
============

[![image](https://travis-ci.org/geopython/pycsw.svg?branch=master)](https://travis-ci.org/geopython/pycsw)

pycsw is an OGC CSW server implementation written in Python.

pycsw fully implements the OpenGIS Catalogue Service Implementation
Specification (Catalogue Service for the Web). Initial development
started in 2010 (more formally announced in 2011). The project is
certified OGC Compliant, and is an OGC Reference Implementation. Since
2015, pycsw is an official OSGeo Project.

pycsw allows for the publishing and discovery of geospatial metadata via
numerous APIs (CSW 2/CSW 3, OpenSearch, OAI-PMH, SRU). Existing
repositories of geospatial metadata can also be exposed, providing a
standards-based metadata and catalogue component of spatial data
infrastructures.

pycsw is Open Source, released under an MIT license, and runs on all
major platforms (Windows, Linux, Mac OS X).

Please read the docs at <http://pycsw.org/docs> for more information.

### Installation

``` sourceCode python
git clone https://github.com/bennidietz/pycsw_fork.git && cd pycsw
pip install -e . && pip install -r requirements-standalone.txt
python pycsw/wsgi.py
```

### Start virtenv and pycsw again

Run in pycsw folder:

``` sourceCode python
python pycsw/wsgi.py
```

### What is new in our pycsw version?
We enhanced pycsw with two similarity functions that include metadata
fields of the records like the wkt\_geometry, the temporal extent, the
vector representation and the format of the related file.

Similar records can be displayed by the 'getSimilarRecords'-request that
react to the following parameters:

  - id (required)
  - all parameter that are included in the 'getRecordById'-request
  - maxrecords <sup>[2](#footnote2)</sup>  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  max number of shown similar records
  - spatial\_weight <sup>[1](#footnote1)</sup>  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  how relevant shall the spatial factor be in
    the similarity calculation
  - temp\_weight <sup>[1](#footnote1)</sup>  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;how relevant shall the temporal factor be in the
    similarity calculation
  - datatype\_weight <sup>[1](#footnote1)</sup> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;how relevant shall the similarity of
    datatypes be in the similarity calculation
  - location\_weight <sup>[1](#footnote1)</sup> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;how relevant shall the location factor be in
    the similarity calculation
  - geographic\_weight <sup>[1](#footnote1)</sup>&nbsp;&nbsp;how relevant shall the geographic factor be
    in the similarity calculation
  - extent\_weight <sup>[1](#footnote1)</sup> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; how relevant shall the extent factor be in the
    similarity calculation
    
<a name = "footnote1"> 1 </a> The range of the weights can be definded in the `preferences.cfg-file <https://github.com/KathHv/pycsw/blob/master/preferences.cfg>`_ file as well through the 'max_value_for_weight' variable (right boundry).
    the default weight for each weight can be set in this file as well  
<a name = "footnote2"> 2 </a>  the limit for this parameter can be set in the `preferences.cfg-file <https://github.com/KathHv/pycsw/blob/master/preferences.cfg>`_ through the parameter 'limit_for_similarrecords'.
