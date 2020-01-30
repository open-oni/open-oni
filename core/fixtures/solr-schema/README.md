# Solr Schema Fixtures

This directory holds the JSON files which define ONI's Solr schema.  These
files must:

- Be sorted in the order they are meant to load, in case of any dependencies,
  e.g., custom field types have to be defined before fields using them
- **Not** be modified after they're part of an ONI release!  A single error in
  one file, *including* a "field already exists" error, will prevent the
  **entire file** from being loaded.
- Be under 8192 bytes each!  The Solr image uses a configuration we can't
  override without complicating the stack, and which doesn't allow more than 8k
  in a request's body
- Be idempotent: sending any file a second time should not change Solr's
  configuration in any way

Unfortunately, the final point means copy fields have to be in code
(`core/management/commands/setup_index.py`) rather than just JSON here.  Copy
fields can be duplicated as many times as somebody calls that API, and they all
end up in the schema file as well as being returned when requesting the schema
throught the Solr APIs.  Field types and regular fields are actually checked
for uniqueness, so I'm not sure why copy fields aren't, but I don't know what
the ramifications may be of having dozens of redefined copy fields... and I'm
pretty sure we're better off not finding out.

[View Open ONI's primary documentation](/docs/)
