openoni
=======

openoni is a community maintained project developed from chronam, the [Django](http://djangoproject.com) application that the
Library of Congress uses to make its
[Chronicling America](http://chroniclingamerica.loc.gov) website.
The Chronicling America website makes millions of pages of historic American
newspapers that have been digitized by the
[National Digital Newspaper Program (NDNP)](http://www.loc.gov/ndnp/)
browsable and searchable on the Web. A little bit of background is needed to
understand why this software is being made available.

NDNP is actually a partnership between the Library of Congress, the
[National Endowment for the Humanities (NEH)](http://www.neh.gov), and
cultural heritage organizations
([awardees](http://chroniclingamerica.loc.gov/awardees/)) across the
United States who have applied for grants to help digitize newspapers
in their state. Awardees digitize newspaper microfilm according
to a set of [specifications](http://www.loc.gov/ndnp/guidelines/)
and then ship the data back to the Library of Congress where it is
loaded into Chronicling America.

Awardee institutions are able to use this data however
they want, including creating their own websites that highlight their
newspaper content in the local context of their own collections. The idea of
making openoni available here on Github is to provide a technical option to
these awardees, or other interested parties who want to make their own websites
of NDNP newspaper content available. openoni provides a core set of functionality
for loading, modeling and indexing NDNP data, while allowing you to customize
the look and feel of the website to suit the needs of your organization.

The NDNP data is in the Public Domain and is itself [available]
(http://chroniclingamerica.loc.gov/data/batches/) on the Web for anyone to use.
The hope is that the openoni software can be useful for others who want to
work with and/or publish the content.

Install
-------

**Please note**: for development, look at the [docker setup](docker/README.md).

Production install instructions are still a work in progress.

Testing
-------

    docker-compose -f test-compose.yml -p onitest up test

This will spew a lot of output and you'll have to scroll back a ways to get at
test failure information.  But it runs a test container setup that ensures your
development data cannot possibly be modified.

Slack
-----
We have a development slack at open-oni.slack.com. Please email kdalziel [at] unl.edu for an invite. 

License
-------

[Licensed](https://github.com/open-oni/open-oni/blob/master/LICENSE) under the Apache License, Version 2.0.

Documentation
-------------

Documentation is in progress on the [project Wiki](https://github.com/open-oni/open-oni/wiki). 
