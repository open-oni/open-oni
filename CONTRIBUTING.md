# Contributing to Open ONI

We would love any and all contributions to Open ONI, be they words of
encouragement, issue reporting, questions, or collaboration.

Everyone interacting within the Open ONI community is expected to follow the
[Open ONI Community Code of
Conduct](https://github.com/open-oni/open-oni/tree/dev/CODE_OF_CONDUCT.md)

**Contents**

- [Develop With Us](#develop-with-us)
  - [Workflow](#workflow)
  - [Testing](#testing)
- [Development Standards](#development-standards)
  - [Style Guidelines](#style-guidelines)
    - [Documentation](#documentation)
  - [Source Control](#source-control)
    - [Feature Branches](#feature-branches)
    - [Pull Requests and Merging](#pull-requests-and-merging)
  - [Security](#security)
  - [Release Checklist](#release-checklist)

## Develop With Us

There is a lot of work to be done on Open ONI. [Joining us on
Slack](https://join.slack.com/t/open-oni/shared_invite/enQtMzg5MDg5NjU5MDU2LTA4MmViOTkxZDliZWZmM2FlMGU5ODZjNDU0OWQxYzIzMTY1YmFlMWEzZDFkNDNjZmYxYzUyMmMwZjlkMjU1MGE)
and [submitting issues](https://github.com/open-oni/open-oni/issues) are both
great ways to get involved without diving into the code.

For those willing to write code, we adhere to our [development
standards](#development-standards) below to keep us all on the same page.

You should start by reviewing the [Docker
install](https://github.com/open-oni/open-oni/tree/dev/docs/install/docker.md)
page to help set up a development environment.

### Workflow

**Important**: All features should be based on the `dev` branch! We use a loose
[gitflow-like](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)
branching strategy, and `main` is meant to always be production-ready. Only
*major* bug fixes (such as security issues) should be applied directly to the
`main` branch. Also read the following to inform your git use:
https://drewdevault.com/2019/02/25/Using-git-with-discipline.html

First, fork the [Open ONI repository](https://github.com/open-oni/open-oni) in
GitHub so you have rights to push code. Then clone it, check out `dev`, create a
feature branch, and do your work:

```bash
git clone https://github.com/<your github namespace>/open-oni.git
cd open-oni
git checkout dev
git checkout -b feature/my-awesome-oni-thing
```

When you're ready, push up your code and
[submit a pull request](https://github.com/open-oni/open-oni/pulls).
**Make sure** the pull request is against the `dev` branch, *not* `main`.

### Testing

```bash
docker-compose -f test-compose.yml -p onitest up test
```

This will produce a lot of output and you'll have to scroll back to get read
test failure information, but it runs a test container setup that ensures your
development data will not be modified.

## Development Standards

Below are our coding standards and best practices for Open ONI development.

Language Notes:

- "Use" is a positive instruction, equivalent to "must use".
- "Prefer" indicates a better option and its alternative to watch out for.
- "Avoid" means don't do it unless you have good reason.
- "Don't" means there's never a good reason.

### Style Guidelines

1. In existing files, prefer to stay consistent with code style used by the
   older code
1. In new code, use [Django coding
   standards](https://docs.djangoproject.com/en/2.2/internals/contributing/writing-code/coding-style/)
1. Don't mix style fixes with other changes
1. Don't rewrite entire files to fix style without communicating to the team
   (this can result in VERY painful merging)
1. Use unix-style line endings
1. Use a newline at the end of the file
1. Don't leave trailing whitespace

#### Documentation

1. Try to document every method using block comments
    - Prefer docstring-style comments for easier automatic documentation
1. Avoid inline comments

### Source Control

1. Use Git and GitHub for source control
1. Use commit messages that follow the conventions here whenever possible:
   http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html
1. Use [semantic versioning](http://semver.org/) for tags

#### Feature Branches

1. Do work in feature branches, named with a prefix `feature/[branch-name]`
1. Publish feature branches to the GitHub repository when:
    - Collaboratively developing the feature
    - Seeking code review in advance of a pull request
    - Sharing the feature externally
    - If your code isn't going to be useful or meaningful to others, clean it up
      first
1. Send pull requests to merge features to `dev`
1. Delete branches when they are fully merged and no longer needed
1. Developers will collaborate to merge additions to `dev` into `main` for
   releases

#### Pull Requests and Merging

1. Keep pull requests clean:
    - Retain "milestone" commits, representing substantial peices of work
    - Squash minor and personal workflow commits into milestones
1. Pull requests are subject to review. Someone other than you must merge them

### Security

1. Prefer environment variables for storing confidential information (database
   passwords, session secrets, etc)
1. When configuration files are required:
    - Do provide an example config
    - Use .gitignore to ensure the true config is not in source control
    - Prefer production config setup via automatic deploys, not manually copying
      files

### Release Checklist

Follow these steps for each Open ONI release:

- Ensure `core/version.py` is set to the new version on the release PR
- Review and merge the release PR into `main`
- [Create a GitHub release](https://github.com/open-oni/open-oni/releases/new)
- Update [open-oni.github.io
  source](https://github.com/open-oni/open-oni.github.io) as necessary
- Merge the `main` branch back into the `dev` branch
- Copy the template for unreleased work in `CHANGELOG.md` on the `dev` branch
- Post an announcement to #general channel on Slack and the [Chronam Users
  mailing list](https://listserv.loc.gov/cgi-bin/wa?A0=CHRONAM-USERS)

