# Solr 6.x

**Contents**

- [Install](#install)
- [Configure](#configure)

## Install

General installation and configuration is outside the scope of Open ONI
documentation, but follow these to start:
- [Solr Downloads](https://lucene.apache.org/solr/downloads.html)
- [Production Service
  Install](https://lucene.apache.org/solr/guide/6_6/taking-solr-to-production.html#TakingSolrtoProduction-ServiceInstallationScript)

## Configure
```bash
sudo -u solr /opt/solr/bin/solr create_core -c openoni
```

Copy in Open ONI's Solr `schema.xml` and `solrconfig.xml`. Delete
`managed-schema` so Solr regenerates it based on `schema.xml`. Ensure Solr has
appropriate permissions on copied files. Restart Solr so the core uses the Open
ONI schema.

```bash
sudo cp /opt/openoni/docker/solr/schema.xml /var/solr/data/openoni/conf/schema.xml
sudo cp /opt/openoni/docker/solr/solrconfig.xml /var/solr/data/openoni/conf/solrconfig.xml

# https://lucene.apache.org/solr/guide/6_6/schema-factory-definition-in-solrconfig.html#SchemaFactoryDefinitioninSolrConfig-Switchingfromschema.xmltoManagedSchema
sudo rm /var/solr/data/openoni/conf/managed-schema

sudo chown -R solr.solr /var/solr/data/openoni

sudo service solr restart
```

