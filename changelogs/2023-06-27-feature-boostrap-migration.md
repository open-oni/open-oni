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

### Added
- This changelog
- Instructions for migrating sites and themes to new version of Open ONI
- Accessibility improvements
	- Add background color to nav item on hover
  - Add landmarks to meet ARIA 1.2 accessibility specifications
    - `<div id="main_content">` becomes `<main id="main_content">`
    - `<div id="footer">` becomes `<footer id="footer">`
    - `<nav>` landmark around navbar, pagination, and previous/next buttons
  - Add ARIA labels and roles to navigation, pagination, and form elements
- Add Bootstrap v5 classes for layout and accessibility
  - Add classes required by Bootstrap v5
      - Add `.breacrumb-item` class to breadcrumb `<li>` elements
      - Add `.form-check-*` classes to checkboxes
      - Add `.form-label` to form labels
      - Add `.form-select` to dropdowns
      - Add `.list-inline-item` to `.list-inline > li`
      - Add `.nav-item` to navbar `li`
      - Add `.nav-link` to navbar `a`
      - Add `.page-item` to `.pagination > li`
      - Add `.page-link` to `.pagination > li > a`
  - Add flexbox classes where a more responsive column layout is needed
    - main navigation
    - search results image gallery
    - `title.html` metadata columns 
    - `title.html` front page thumbnail and link
  - Add styles to form labels and legends to account for v3 to v5 visual changes
  - Add padding, margin, and alignment classes to make form elements and rows 
easier to distinguish
  - Add v5 padding classes to breadcrumbs
  - Add styles for `#newspaper_nav` pills to retain original styling on hover
  - Add `.table-responsive` to tables so they scroll horizontally rather than 
  extend beyond the page
- Add container to fix `pagination_bottom` alignment
- Add `scope="col"` to table headers



### Changed
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
- Accessibility improvements
  - Move `h1` tag from site title to page title
  - Change heading tags to follow hierarchical order
  - Change `div` wrapper around forms to `form` element
  - Wrap images in `figure` tags instead of `div` tags
  - Change calendar image alt text to indicate what the image links to
  - Change table row headers from `td` to `th` where applicable
- Update page layout for mobile / narrow browser widths
  - Change search results image gallery to use flexbox
  - Change navigation pill classes to wrap at smaller browser widths
  - Change column classes to accommodate wider browser widths
    - main navigation
    - search form in `search_advanced.html`
    - `extra_nav` in `issues_title.html`
    - view options and pagination in `search_page_results.html`
- Replace Bootstrap v3 classes with Bootstrap v5 classes
    - Change `.btn-default` to `.btn-secondary`
    - Change `.form-control` to `.form-select`
    - Change `.help-block` to `.form-text`
    - Change `.input-sm` to `.form-control-sm`
    - Change `.help-block` to `.form-text`
    - Change `.pagination-mini` (deprecated) to `.pagination-sm`
    - Change `.pull-*` to `.float-*`
    - Change `.sr-*` classes to `.visually-hidden-*` classes
    - Change v3 left/right margin and padding classes to v5 start/end classes
- Amend `forms.py` to distinguish between search form dropdowns and 
text fields (v5 requires different classes for each)
- Move `newspapers.html` search help text below form input and change from 
`span` to `div` (v5 removed `display:block` from help text)
- Move `search_advanced.html` "Limit By," "Search selected newspapers", and 
"Additional Filters" into a single fieldset
- Change `issue_pages.html` page label wrappers to be consistent (`p` instead 
of `div`)
- Change Previous/Next Issue buttons from `button` to `a` with ARIA properties 
and v5 button classes
- Change how spacing is handled on reports pages
  - Remove empty paragraphs and line breaks
  - Add Bootstrap v5 padding/margin classes to surrounding elements
- Change how striped table columns are generated
  - Remove Django table striping (`{% cycle 'lighytGray' 'white' %}`)
  - Add v5 `.table-striped` and `.table-hover` classes
- Replace inline CSS styles with Bootstrap classes

...
- Update core CSS to account for Bootstrap style changes
  - Change `.header_navbar a` selector to `.header_navbar .nav-item .nav-link` 
  to retain specificity
  - Change CSS selectors for link styles so they don't apply to buttons and 
  pagination links
  - Change `.title` class to `.site_title` to distinguish from 
  `<td class="title">` in calendar views

### Removed
- Remove deprecated Bootstrap v3 classes
	- `.bold`
	- `form-group`
  - `form-inline`
  - `.info`
- Remove Bootstrap style overrides from default theme CSS that are no 
longer necessary with v5
  - Remove `.main-content`padding
  - Remove `h1.title` `font-size` override
  - Remove `.header_navbar` `border` and `margin-bottom` overrides
- Remove unnecessary if loop from search results image gallery code
- Remove `width=100%` inline style from tables (no longer required with v5)


### Migration
- Migrate `core` and `default theme` from Bootstrap v3.4 to Bootstrap v5.3
  - Replace [Bootstrap v3.4 Compiled CSS and JS](https://getbootstrap.com/docs/3.4/getting-started/#download) 
  with [Bootstrap v5.3 Compiled CSS and JS](https://getbootstrap.com/docs/5.3/getting-started/download/)
  - Remove deprecated v3 classes (see Removed section of this document)
  - Change v3 classes to v5 classes (see Changed section of this document)
  - Change default theme CSS to account for Bootstrap framework changes (see 
  Changed section of this document)
  - Add v5 classes for layout and accessibility (see Added section of this 
  document)

### Deprecated
- Remove default theme CSS styles/selectors that are no longer in use
  - `.page-search .col-sm-auto`
- Remove outdated HTML and CSS comments

### Contributors
- Erin Chambers (erinchambers)
