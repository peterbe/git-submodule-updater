from urllib.parse import urlparse

import click

from .core import make_prs, CoreException


@click.command()
@click.option(
    "--branch", default="master", help="name of main branch (default 'master')"
)
@click.option("--submodule", default="", help="name of submodule (default first found)")
@click.option(
    "--submodule-branch",
    default="master",
    help="name of submodule branch (default 'master')",
)
@click.option(
    "--submodule-origin-name",
    default="origin",
    help="name of submodule origin (default 'origin')",
)
@click.argument("repo")
def cli(repo, branch, submodule, submodule_branch, submodule_origin_name):
    git_server = "github.com"
    if "github.com" in repo and "://" not in repo:
        # E.g. github.com/mdn/stumptown-renderer
        repo = "https://" + repo
    if "://" in repo:
        parsed = urlparse(repo)
        git_server = parsed.netloc
        org, repo = parsed.path[1:].split("/", 1)
        if repo.endswith(".git"):
            repo = repo[:-4]
    elif "/" in repo:
        org, repo = repo.split("/", 1)
    else:
        raise NotImplementedError(f"Don't know how to parse {repo!r}")

    config = {
        "branch": branch,
        "submodule_branch": submodule_branch,
        "submodule_origin": submodule_origin_name,
        "submodule_name": submodule,
        "git_server": git_server,
    }
    try:
        make_prs(org, repo, config)
    except CoreException as exception:
        info_out(exception.__class__.__name__)
        error_out(str(exception))
        raise click.Abort


def error_out(msg):
    click.echo(click.style(msg, fg="red"))


def info_out(msg):
    click.echo(click.style(msg, fg="yellow"))
