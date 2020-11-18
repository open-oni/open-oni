# Custom LCCN and MARC Records

There comes a time in many an organization's life when they find they need to
fabricate an LCCN and MARC Record. How can this be? Could be that:

- the title has never been added to the Library of Congress
- the MARC information is incorrect in the Library of Congress
- the Library of Congress's endpoint is temporarily offline

You may want to consult with a librarian to find out if your title SHOULD be
part of the Library of Congress's (LoC) records before you get too far, but
regardless it is possible to get your content into Open ONI, assuming that it
is part of a valid batch.

## Custom Endpoint

When loading a batch, Open ONI checks each of the titles in the batch's LCCN
and attempts to fetch a MARC record for them. By default, this uses the LoC
endpoint. However, you can change this to an endpoint of your choice with the
setting: `MARC_RETRIEVAL_URLFORMAT`.

For example, Open ONI has a [repository with mirrored MARC records](https://github.com/open-oni/marc-mirror).
You can use that repository by changing your settings to:

```
MARC_RETRIEVAL_URLFORMAT = "https://raw.githubusercontent.com/open-oni/marc-mirror/main/marc/%s/marc.xml"
```

Similarly, you could create your own MARC records and point your Open ONI
installation towards them with that setting.

## Load Title

Open ONI has a `load_titles` tool which accepts a path to directory containing
MARC records. Once a title is loaded in the database, loading a batch will no
longer attempt to retrieve MARC data.

Please see the [admin commands documentation](/docs/advanced/admin-commands.md)
for more information about `load_titles`.
