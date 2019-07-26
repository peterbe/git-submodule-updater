import tempfile
import subprocess
from pathlib import Path

import git
from decouple import config
from github import Github

GITHUB_ACCESS_TOKEN = config("GITHUB_ACCESS_TOKEN")


def make_prs(org, repo, config):
    clone_url = f"git@github.com:{org}/{repo}.git"
    name = repo
    config["repo_name"] = f"{org}/{repo}"
    with tempfile.TemporaryDirectory() as tmpdir:
        destination = Path(tmpdir) / name
        cmd = f"git clone --depth=50 {clone_url} {destination}".split()
        popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        r = popen.communicate()
        assert not r[1], r[1]
        make_branch(destination, config)


class SubmoduleFindingError(Exception):
    """when struggling to find the submodule."""


class PullRequestError(Exception):
    """when struggling to find, edit, or make pull request."""


def make_branch(repo_path, config):
    repo = git.Repo(repo_path)
    submodules = {}
    name = config.get("submodule_name")
    for submodule in repo.submodules:
        submodules[submodule.name] = submodule
    if not submodules:
        raise SubmoduleFindingError("No submodules found")
    elif len(submodules) > 1 and not name:
        raise SubmoduleFindingError(f"Found more than 1 ({submodule.keys()}")
    elif not name:
        submodule, = list(submodules.values())
        name = submodule.name
    else:
        submodule = submodules[name]

    submodule.update(init=True)
    branch_name = config.get("submodule_branch") or "master"
    origin_name = config.get("submodule_origin") or "origin"
    sub_repo = submodule.module()
    sub_repo.git.checkout(branch_name)
    for remote in sub_repo.remotes:
        if remote.name == origin_name:
            break
    else:
        raise SubmoduleFindingError(f"Can't find origin {origin_name!r}")
    sha = sub_repo.head.object.hexsha

    short_sha = sub_repo.git.rev_parse(sha, short=7)
    remote.pull(branch_name)
    sha2 = sub_repo.head.object.hexsha
    short_sha2 = sub_repo.git.rev_parse(sha2, short=7)

    new_branch_name = f"update-{name}-{short_sha}-to-{short_sha2}"
    print("new_branch_name", new_branch_name)
    current = repo.create_head(new_branch_name)
    current.checkout()
    repo.git.add(A=True)
    msg = f"Update submodule {name!r} from {short_sha} to {short_sha2}"
    repo.git.commit(["-m", msg])
    pushed = repo.git.push("origin", new_branch_name)
    print("PUSHED:")
    print(repr(pushed))

    g = Github(GITHUB_ACCESS_TOKEN)
    # Bail if we already have a PR by this branch name
    repo_name = config["repo_name"]
    g_repo = g.get_repo(repo_name)
    if config["git_server"] != "github.com":
        raise NotImplementedError
    # pulls = repo.get_pulls(state='open', sort='created', base='master')
    pulls = g_repo.get_pulls(sort="created", base="master")
    for pull in pulls:
        branch_ref_name = pull.raw_data["head"]["ref"]
        if new_branch_name in branch_ref_name:
            url = pull.raw_data["_links"]["html"]["href"]
            raise PullRequestError(f"Already at a pull request at {url}")

    # https://github.com/PyGithub/PyGithub/blob/6e79d2704b8812d26435b21c1258c766418ab25e/github/Repository.py#L1207
    body = "Updating the submodule! 😊\n"
    created_pr = g_repo.create_pull(msg, body, "master", new_branch_name)
    print(created_pr.html_url)
    return created_pr