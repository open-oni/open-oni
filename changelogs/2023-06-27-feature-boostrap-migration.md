Changelog format is based on [Keep a
Changelog](https://keepachangelog.com/en/1.0.0/).

Please respect the 80-character text margin and follow the [GitHub Flavored
Markdown Spec](https://github.github.com/gfm/).

### Fixed
- Fix color contrast to meet WCAG AA & AAA accessibility standards
- Fix heading tags to follow hierarchical order and not skip heading levels
- Fix `search_advanced.html` HTML error - `<h3>Search Terms</h2>`
- Fix `title.html` HTML error - extraneous `<dd>` in Language list 
- Fix missing `</tr>` tag in `awardee.html` table
- Fix `pagination_bottom` alignment
- Fix inconsistent page label wrappers on `issue_pages.html`

### Added
- This changelog
- Instructions for migrating sites and themes to new version of Open ONI
- Accessibility improvements
	- Add background color to nav item on hover
  - Add landmarks to meet ARIA 1.2 accessibility specifications
  - Add ARIA labels and roles to navigation, pagination, and form elements
  - Add `scope="col"` to table headers
  - Wrap images in `figure` tags
- Add element-specific classes required by Bootstrap v5
- Add v5 flexbox classes where a more responsive layout is needed
- Add v5 classes to replace v3 baked-in styles



### Changed
- Replace [Bootstrap v3.4 Compiled CSS and JS](https://getbootstrap.com/docs/3.4/getting-started/#download) with [Bootstrap v5.3 Compiled CSS and JS](https://getbootstrap.com/docs/5.3/getting-started/download/)
- Major changes to navigation menu from v3 to v5
  - Change navbar to `ul` to improve accessibility
	- Switch from `.navbar-inverse` to `.navbar-dark`
	- Add breakpoint and padding/margin classes to replace deprecated styling
	- Replace v3 menu toggle button with v5 version
	- Add required `.nav-item` class to navbar `li`
	- Add required `.nav-link` class to navbar `a`
  - Update padding and flexbox classes and styling to maintain existing layout
	- Update `navbar_search` block with `ul`, flexbox, and padding classes to 
  maintain existing layout
- Update column sizes for mobile / narrow browser widths
- Move `h1` tag from site title to page title and change headings tags to 
follow hierarchical order
- Change table row headers from `td` to `th`
- Amend `forms.py` to distinguish between search form dropdowns and 
text fields; v5 requires different classes for each
- Move `search_advanced.html` "Limit By," "Search selected newspapers", and 
"Additional Filters" into a single fieldset
- Switch Previous/Next Issue buttons to links with ARIA properties and v5 button classes
- Replace empty paragraphs and line breaks in reports with v5 padding/margin classes
- Replace Django table striping (`{% cycle 'lightGray' 'white' %}`) with v5 `.table-striped` and `.table-hover` classes
- Replace inline CSS styles with Bootstrap classes
- Update core CSS to account for Bootstrap style changes
  - Change CSS selectors for link styles so they don't apply to buttons and 
  pagination links
  - Change `.title` class to `.site_title` to distinguish from 
  `<td class="title">` in calendar views

### Removed
- Remove deprecated Bootstrap v3 classes
- Remove Bootstrap style overrides that are no longer necessary after migrating 
to v5
- Remove unnecessary if loop from search results image gallery


### Migration
- This release updates the OpenONI `core` files and `default theme` from 
Bootstrap v3.4 to Bootstrap v5.3
- If you have customized your site theme using Bootstrap, see 
the official [Bootstrap 3 -> 4](https://getbootstrap.com/docs/4.0/migration/) and [Bootstrap 4 -> 5](https://getbootstrap.com/docs/5.0/migration/) documentation for framework additions, 
changes, and deprecations.


### Deprecated
- Remove default theme CSS styles/selectors that are no longer in use
  - `.page-search .col-sm-auto`
- Remove outdated HTML and CSS comments

### Contributors
- Erin Chambers (erinchambers)
