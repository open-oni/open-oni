- List changes with brief descriptions
  - Closes #

## Submitter Checklist

- [ ] Verify all tests pass
  - Run tests with `docker-compose -f test-compose.yml -p onitest up test`
- [ ] Update `README.md` and `docs/` as necessary
  - [ ] If a `manage.py` command is added, deleted, or modified its help text must
    be valid and it should be documented in detail in
    `docs/advanced/admin-commands.md`
- Update `CHANGELOG.md`
  - [ ] Describe change(s) in appropriate section(s)
  - [ ] List self in Contributors section
- If a release PR:
  - [ ] In `CHANGELOG.md`, replace `[Unreleased]` with version and update compare link
  - [ ] Update `core/version.py` with new version
- [ ] Resolve merge conflicts
- [ ] @mention individual(s) you would like to review the PR
  - Reviews for releases must come from a reviewer at another institution

## Reviewer Checklist

- [ ] Verify all tests pass
- [ ] Review changes for behavior, bugs, and compliance with [Development
  Standards](https://github.com/open-oni/open-oni/tree/dev/CONTRIBUTING.md#development-standards)
  - Request the submitter make any changes rather than pushing changes yourself.
    Otherwise ask another reviewer to look at any changes you have made.
- [ ] If a release, follow the [Release
  Checklist](https://github.com/open-oni/open-oni/tree/dev/CONTRIBUTING.md#release-checklist)
<!-- Markdown renders in unwanted carriage return if this text is continued on
     the next line, so breaking character margin intentionally here -->
