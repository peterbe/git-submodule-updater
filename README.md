# git-submodule-updater

A tool to automate making GitHub Pull Requests about updating
git submodules.

You should be able to just give it the name of a repo (e.g. `mozilla/kuma`)
and it finds out which submodules there are and looks to see if they can be
updated.

## Demo

Not really a demo but [this pull request](https://github.com/mdn/stumptown-renderer/pull/62)
was entirely made from this script.

## Limitations and caveats

At the time of writing, **this is a prototype**. It's doing the least possible
to make the most basic thing work.

- It requires that you're allowed to push branches to the origin.
- It only really works with GitHub.com
- It's doing the `git` clone with SSH. So not sure how to make this work in
  a server.
- It's only a CLI at the moment.
- There's no good way to auto-close now out-of-date older PRs
- No unit tests
- Not tested beyond the defaults of `master` and `origin`
- It can only make 1 PR per the difference between the head and the submodule.
- To see what the difference in a submodule update you have to rely on GitHub's
  "Files changed" tab on the PR.

## Getting started

You'll need a GitHub access token.
Go to [github.com/settings/tokens](https://github.com/settings/tokens) and create a token,
copy and paste it into your `.env` file or use `export`. E.g.

    cat .env
    GITHUB_ACCESS_TOKEN=a36f6736...

    pip install git-submodule-updater
    gsmu github.com/mdn/stumptown-renderer  # for example

If you don't use a `.env` file you can use:

    GITHUB_ACCESS_TOKEN=a36f6736... gsmu myorg/myrepo

## Goal

This tool should be possible to run as a CLI and as a web server
so it can be connected to a GitHub repo Webhook.

## Contributing

Clone this repo then run:

    pip install -e ".[dev]"

That should have installed the CLI `gsmu`

    gsmu --help

If you wanna make a PR, make sure it's formatted with `black` and passes `flake8`.
