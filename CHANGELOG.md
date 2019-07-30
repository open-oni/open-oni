# Open ONI Changelog
All notable changes to Open ONI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic
Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
Coming soon

## [v0.10.0] - 2018-01-29 - Hey it actually really works again!
- Unpinned RAIS for Docker users
- Fixed URL for pulling MARC records from Chronicling America

## [v0.9.0] - 2018-01-24 - Hey it works again!
- Freezes dependencies to fix a problem where new installs would simply not work
  due to missing python libraries
- Updates advanced search to put "Search Terms" above "Proximity Search" based
  on user feedback

## [v0.8.0] - 2017-11-14 - Bug fixes
Adds "proximity" searching back into the advanced search, and improves
accessibility with the search results pagination

## [v0.7.0] - 2017-10-25 - Bug fixes
Multiple bugs have been addressed:
- The "about" page, when the first or last issue wasn't digitized, no longer
  crashes
- The "page number" in advanced search was never working and has been replaced
  with a checkbox to choose front pages only
- The selected titles, from advanced search, now persist when refining search
  results
- The "jump to page" functionality no longer loses various search filters
- Various other "refine search" persistence problems have been addressed

## [v0.6.0] - 2017-09-21 - New languages support, universal viewer support, mariadb
This is a big back-end release:
- We've now got Solr configured to support a bunch of new languages instead of
  just the four or five we had from the chronam fork.
- We've updated the docker setup to use mariadb instead of mysql (you'll
  probably want to dump your MySQL database and import it into MariaDB).
- Last, but definitely not least: there is now significantly better support for
  IIIF systems like the Universal Viewer!

## [v0.5.0] - 2017-09-07 - Bug fixes
- Fixes a failure that affected everybody trying to set up a new ONI site. Oops.
- Adds image attribution on image pages
- Fixes a crash in the title "front pages" view when a published image wasn't
  digitized

## [v0.4.0] - 2017-08-29 - Bug fixes and dev improvements
Highlights finally work properly (we think)!! Also, skip links work better,
there's an easier way to run tests locally via docker, and Apache log level is
configurable by an environment variable.

## [v0.3.0] - 2017-08-24 - Search fixed and slightly better UI
- Improves accessibility on the advanced search form and the search results
  templates
- Removes state dropdowns from advanced search and search results templates
- Removes the redundant link in the titles list ("More Info") for newspapers
  with essays associated

## [v0.2.2] - 2017-08-22 - Faster purge
Removes the solr and mysql optimization as a default step when purging batches,
as it can take a very long time with large datasets. Optimization can still be
done by adding `--optimize` to the purge command.

## [v0.2.1] - 2017-08-11 - Image URL bug fixes
Fixes a bug where resized image URLs were always at the thumbnail size. Adds a
new size option, "tiny", for accommodating smaller devices more effectively.

## [v0.2.0] - 2017-08-09
This release upgrades the docker-compose setup to use Solr 6.6, and fixes a few
bugs only discovered when there were multiple pages of batches

## [v0.1.0] - 2017-07-24
This is the official initial release of Open ONI. The changes since forking are
too numerous to try and describe.

[Unreleased]: https://github.com/open-oni/open-oni/compare/v0.10.0...dev
[v0.10.0]: https://github.com/open-oni/open-oni/compare/v0.9.0...v0.10.0
[v0.9.0]: https://github.com/open-oni/open-oni/compare/v0.8.0...v0.9.0
[v0.8.0]: https://github.com/open-oni/open-oni/compare/v0.7.0...v0.8.0
[v0.7.0]: https://github.com/open-oni/open-oni/compare/v0.6.0...v0.7.0
[v0.6.0]: https://github.com/open-oni/open-oni/compare/v0.5.0...v0.6.0
[v0.5.0]: https://github.com/open-oni/open-oni/compare/v0.4.0...v0.5.0
[v0.4.0]: https://github.com/open-oni/open-oni/compare/v0.3.0...v0.4.0
[v0.3.0]: https://github.com/open-oni/open-oni/compare/v0.2.2...v0.3.0
[v0.2.2]: https://github.com/open-oni/open-oni/compare/v0.2.1...v0.2.2
[v0.2.1]: https://github.com/open-oni/open-oni/compare/v0.2.0...v0.2.1
[v0.2.0]: https://github.com/open-oni/open-oni/compare/v0.1.0...v0.2.0
[v0.1.0]: https://github.com/open-oni/open-oni/releases/tag/v0.1.0

