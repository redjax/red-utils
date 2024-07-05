"""Cleanup your local git environment.

Description:
    This script compares git branches in a specified repository path,
    defaulting to the directory this script is run from i.e. ".",
    with branches on the remote, deleting any local branches not found on the remote.

    This helps by cleaning up branches that have been deleted from the remote, for example a merged feature or fix.
    
    By default, the script will not touch the following branches if they are found, regardless of their presence on the remote:
        - main
        - master
        - dev
        - rc
        - gh-pages
    
    See the `Usage` section for instructions on passing CLI args, adding more protected branch names, etc.

Usage:
    Run this script as a module, i.e. `python -m git_prune <args>`. To see available args and their description, run `python -m git_prune -h`.
    
    ## Prevent accidental deletions with `--dry-run`
    
    Run the script with `--dry-run` to prevent modifications on local branches,
    instead printing a message describing the action that would have been taken.

    ## Pass protected branches with `nargs`
    
    To add more branches that should be ignored in the local repository,
    you can either modify the `PROTECTED_BRANCHES` list below (not recommended),
    or you can pass additional protected branches with `-p`.
    
    For example, to protect the branches `ci` and `stage`, you would run `python -m git_prune -r <repo_path> -p "ci" -p "stage".
    
    ## Attempt to force deletion
    
    `git_prune` will first attempt to delete a branch with `git branch -d <branch>`. If this fails and you passed the `-f/--force` flag,
    a retry attempt will be made using `git branch -D <branch>`. If this also fails, a third and final attempt will be made using the host's
    git by running the command `git branch -D <branch>` through the `subprocess.run()` command.

"""

from __future__ import annotations

import argparse
import logging
import platform
import subprocess
import typing as t

log: logging.Logger = logging.getLogger("git_prune")
logging.getLogger("git").setLevel("WARNING")

import git

DEFAULT_REPO_PATH: str = "."
PROTECTED_BRANCHES: list[str] = ["main", "master", "dev", "rc", "gh-pages"]


def get_default_python() -> str:
    """Detect Python version from environment.

    Returns:
        (str): The detected Python version, in format 'major.minor' i.e. '3.11'.

    """
    pyver_tuple: tuple[str, str, str] = platform.python_version_tuple()
    pyver: str = f"{pyver_tuple[0]}.{pyver_tuple[1]}"

    return pyver


def is_git_installed() -> bool:
    """Detect GitPython package.

    Returns:
        (True): If `GitPython` package is detected in environment.
        (False): If `GitPython` package is not detected in environment.

    """
    try:
        import git

        return True
    except ImportError:
        return False


def append_protected_branch(
    protected_branches: list[str] = PROTECTED_BRANCHES, append_branch: str = None
) -> list[str]:
    """Add a branch to the existing list of protected branch names.

    Params:
        protected_branches (list[str]): Existing list of protected branch names.
        append_branch (str): Name of branch to append to list of protected branch names.

    Returns:
        (list[str]): A list of strings representing git branch names that should not be altered.

    """
    if protected_branches is None:
        ## Initialize empty list
        protected_branches: list[str] = []

    if append_branch is None:
        ## No branch names to append, return protected_branches
        return protected_branches

    else:
        ## Append branch and return
        protected_branches.append(append_branch)
        return protected_branches


PYTHON_VERSION: str = get_default_python()
GIT_INSTALLED: bool = is_git_installed()


def init_repo(repo_path: str = None) -> git.Repo:
    """Initialize a `GitPython` `git.Repo` object from a path.

    Params:
        repo_path (str): (Default: ".") Path to the local git repository.

    Returns:
        (git.Repo): An initialized `git.Repo` object for the given `repo_path`.
    """
    ## Initialize repository
    try:
        repo = git.Repo(path=repo_path)
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception initializing git.Repo object for repository path '{repo_path}'. Details: {exc}"
        )
        log.error(msg)

        raise exc

    ## Fetch latest changes & prune deleted branches
    try:
        repo.git.fetch("--prune")
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception fetching branches from remote. Details: {exc}"
        )
        log.error(msg)

        raise exc

    return repo


def get_local_branches(repo: git.Repo = None) -> list[str]:
    """Get list of branch names detected in local repository.

    Params:
        repo (git.Repo): An initialized `git.Repo` instance.

    Returns:
        (list[str]): List of local git branches.

    """
    ## Get a list of local branches
    local_branches: list[str] = [head.name for head in repo.heads]

    return local_branches


def get_remote_branches(repo: git.Repo = None) -> list[str]:
    """Get list of branch names detected in remote repository.

    Params:
        repo (git.Repo): An initialized `git.Repo` instance.

    Returns:
        (list[str]): List of remote git branches.

    """
    ## Get a list of remote branches
    remote_branches: list[str] = [
        ref.name.replace("origin/", "") for ref in repo.remotes.origin.refs
    ]

    return remote_branches


def get_delete_branches(
    repo: git.Repo = None,
    local_branches: list[str] = None,
    remote_branches: list[str] = None,
    protected_branches: list[str] = PROTECTED_BRANCHES,
) -> list[str]:
    """Compare local & remote git branches, return list of branch names to delete.

    Params:
        repo (git.Repo): An initialized `git.Repo` instance. Needed for instances where
            local_branches or remote_branches are empty/None.
        local_branches (list[str]): List of branch names found in local repository.
        remote_branches (list[str]): List of branch names found in remote repository.
        protected_branches (list[str]): List of branch names that will not be altered.

    Returns:
        (list[str]): List of git branches to delete from local repository.

    """
    if local_branches is None or remote_branches is None:
        if repo is None:
            raise ValueError(
                "Missing list of local and/or remote branch names, and no git.Repo object detected. Cannot determine list of branches."
            )

    if local_branches is None:
        ## Get list of local branch names
        local_branches = get_local_branches(repo=repo)

    if remote_branches is None:
        ## Get list of remote branch names
        remote_branches = get_remote_branches(repo=repo)

    ## Find local branches that are not present in remote branches
    branches_to_delete: list[str] = [
        branch
        for branch in local_branches
        if (branch not in remote_branches) and (branch not in protected_branches)
    ]

    return branches_to_delete


def delete_branches(
    repo: git.Repo = None,
    branches_to_delete: list[str] = None,
    force: bool = False,
    protected_branches: list[str] = PROTECTED_BRANCHES,
) -> list[str]:
    """Run git branch delete operation on list of branches.

    Params:
        repo (git.Repo): An initialized `git.Repo` instance.
        branches_to_delete (list[str]): List of branches to delete from local repository.
        force (bool): If `True`, delete operations will be retried if they fail. The first attempt will retry using
            the `-d` flag, and if that fails the function will attempt to use the host's `git` via `subprocess`.
        protected_branches (list[str]): List of branch names that will not be altered.

    Returns:
        (list[str]): The list of branches deleted from the local repository.

    """
    deleted_branches: list[str] = []

    ## Iterate over list of branches to delete
    for branch in branches_to_delete:
        ## Avoid deleting specified branches
        if branch not in protected_branches:
            try:
                repo.git.branch("-d", branch)
                log.info(f"Deleted branch '{branch}'")

                deleted_branches.append(branch)

            except git.GitError as git_err:
                msg = Exception(
                    f"Git error while deleting branch '{branch}'. Details: {git_err}"
                )

                ## Retry with -D if force=True
                if force:
                    log.warning(
                        "First attempt failed, but force=True. Attempting to delete with -D"
                    )
                    try:
                        repo.git.branch("-D", branch)
                        log.info(f"Force-deleted branch '{branch}'")

                        deleted_branches.append(branch)

                    except git.GitError as git_err2:
                        msg2 = Exception(
                            f"Git error while force deleting branch '{branch}'. Details: {git_err2}"
                        )
                        log.warning(
                            f"Branch '{branch}' was not deleted. Reason: {msg2}"
                        )

                        ## Retry with subprocess
                        try:
                            log.info("Retrying one more time using subprocess.")
                            subprocess.run(["git", "branch", "-D", branch], check=True)
                            log.info(
                                f"Force-deleted branch '{branch}'. Required fallback to subprocess."
                            )

                            deleted_branches.append(branch)

                        except subprocess.CalledProcessError as git_err3:
                            msg3 = f"Git error while force deleting branch '{branch}' using subprocess. Details: {git_err3}"
                            log.warning(
                                f"Branch '{branch}' was not deleted. Reason: {msg3}"
                            )

                        except Exception as exc:
                            msg = f"Unhandled exception attempting to delete git branch '{branch}' using subprocess.run(). Details: {exc}"
                            log.error(msg)

                ## force=false, do not retry with Subprocess
                else:
                    log.warning(f"Branch '{branch}' was not deleted. Reason: {msg}")

                continue

    return deleted_branches


def clean_branches(
    repo: git.Repo = None,
    dry_run: bool = False,
    force: bool = False,
    protected_branches: list[str] = PROTECTED_BRANCHES,
) -> list[str] | None:
    """Params:
        repo (git.Repo): An initialized `git.Repo` instance.
        dry_run (bool): If `True`, skip all operations that would alter git branches.
        force (bool): If `True`, when `git branch -d` fails, function will retry with `-D`.
            If this fails, a final attempt will be made using the host's `git` via `subprocess`.
        protected_branches (list[str]): List of branch names that will not be altered.

    Returns:
        (list[str]): List of branches deleted from local repository.

    """

    log.info("Cleaning local branches that have been deleted from the remote.")

    ## Get list of branch names in local repository
    local_branches: list[str] = get_local_branches(repo=repo)
    log.info(f"Found [{len(local_branches)}] local branch(es).")

    if len(local_branches) < 15:
        ## Print local branches if there are less than 15
        log.debug(f"Local branches: {local_branches}")

    ## Get list of branch names in remote repository
    remote_branches: list[str] = get_remote_branches(repo=repo)
    log.info(f"Found [{len(remote_branches)}] remote branch(es).")

    if len(remote_branches) < 15:
        ## Print remote branches if there are less than 15
        log.debug(f"Remote branches: {remote_branches}")

    ## Compare local & remote branches, return list of branches in local that are not in remote
    branches_to_delete: list[str] = get_delete_branches(
        local_branches=local_branches,
        remote_branches=remote_branches,
        protected_branches=protected_branches,
    )
    log.info(f"Prepared [{len(branches_to_delete)}] branch(es) for deletion.")

    if len(branches_to_delete) < 15:
        ## Print branches to delete if there are less than 15
        log.debug(f"Deleting branches: {branches_to_delete}")

    ## Terminate early if dry_run=True
    if dry_run:
        log.warning(f"dry_run=True, terminating early to avoid accidental deletion.")
        log.warning(f"Would have deleted [{len(branches_to_delete)}] branch(es).")
        for b in branches_to_delete:
            log.warning(f"[DRY RUN] Would delete branch: {b}")

        return

    else:
        ## Delete local branches
        try:
            deleted_branches: list[str] = delete_branches(
                repo=repo,
                branches_to_delete=branches_to_delete,
                protected_branches=protected_branches,
                force=force,
            )

            return deleted_branches
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception deleting git branches. Details: {exc}"
            )
            log.error(msg)

            raise exc


def program_args() -> list[tuple[list[str], dict[str, str]]] | None:
    """Define arguments for this script's parser.

    Usage:
        This method should be rewritten for each new script it's used in.
            The existing code can be used as a reference, but every script requires
            different args and the code in this function may not suit your script.

    Returns:
        (list[tuple[list[str], dict[str, str]]] | None): A tuple to be passed to the `parse_cli_args()` method, containing
            argument flags/actions/help strings.

    """
    ## Define list of args for script to parse
    add_args: list[tuple[list[str], dict[str, str]]] = [
        (
            ["--dry-run"],
            {
                "action": "store_true",
                "help": "Prevent any git operations from occurring, print messages indicating what would have happened.",
            },
        ),
        (
            ["-v", "--verbose"],
            {
                "action": "store_true",
                "help": "Set logging level to DEBUG.",
            },
        ),
        (
            ["-f", "--force"],
            {
                "action": "store_true",
                "help": "If GitPython module fails to delete branch with git branch -d and -D, attempt to delete the branch with the host's git using subprocess.",
            },
        ),
        (
            ["-r", "--repo-path"],
            {
                "type": str,
                "help": 'Specify the file path to the git repository. If no option is passed, uses ".", i.e. the directory where this script was run.',
            },
        ),
        (
            ["-p", "--protected-branches"],
            {
                "nargs": "+",
                "help": 'Specify additional protected branches. Can be used multiple times, i.e. -p "branch1" -p "branch2".',
                "metavar": "BRANCH",
            },
        ),
    ]

    return add_args


def parse_cli_args(
    program_name: str | None = __name__,
    usage: str | None = None,
    description: str | None = None,
    add_args: list[tuple[list[str], dict[str, str]]] | None = None,
) -> argparse.Namespace:
    """Parse arguments passed when this script runs.

    Usage:
        Call this function and assign it to a variable, like `args = parse_cli_args()`. Parsed
            args will be available via dot notation, for example an arg named `--verbose` will be available
            at `args.verbose`.

        Pass options/args as a list of tuples, see example of args/flags passed to `parse_cli_args(add_args=add_args)`:

        ```python title="Example add_args values" linenums="1"
            add_args = [
                (
                    ["-v", "--verbose"],
                    {
                        "action": "store_true",
                        "help": "Set logging level to DEBUG.",
                    },
                ),


                (
                    ["--name"],
                    {"type": str, "help": "Specify the name to be used in the operation."},
                ),
            ]
        ```

    Params:
        program_name (str): Name of the script/program for help menu.
        usage (str):  String describing how to call the app.
        description (str): Description of the script/program for help menu.
        add_args (list[tuple[list[str], dict[str, str]]] | None): List of tuples
            representing args to add to the parser.

    Returns:
        (argparse.Namespace): An object with parsed arguments. Arguments are accessible by their name, for
            example an argument `--verbose` is accessible at `args.verbose`. If an argument has a hyphen, like `--dry-run`,
            the hyphen becomes an underscore, i.e. `args.dry_run`.

    """
    parser = argparse.ArgumentParser(
        prog=program_name, usage=usage, description=description
    )

    ## Add arguments from add_args list
    if add_args:
        try:
            for flags, kwargs in add_args:

                parser.add_argument(*flags, **kwargs)
        except ValueError as parse_err:
            msg = ValueError(
                f"Error adding flag(s) '{flags}' to parser. Details: {parse_err}"
            )
            log.error(msg)

            raise exc
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception adding argument to parser. Details: {exc}"
            )
            log.error(msg)

            raise exc

    else:
        ## Uncomment to add default arguments
        # parser.add_argument("--dry-run", action="store_true")
        # parser.add_argument("-v", "--verbose", action="store_true")

        pass

    args: argparse.Namespace = parser.parse_args()

    return args


def setup(
    log_msg_fmt: (
        str | None
    ) = "%(asctime)s | %(levelname)s | %(name)s.%(funcName)s():%(lineno)d |> %(message)s",
    log_msg_datefmt: str = "%Y-%M-%d %H:%m:%S",
) -> argparse.Namespace:
    """Run program setup.

    Params:
        log_msg_fmt (str): The format string for logging messages.
        log_msg_datefmt (str): The format for timestamps on logging messages.

    Returns:
        (argparse.Namespace): An object with parsed arguments. Arguments are accessible by their name, for
            example an argument `--verbose` is accessible at `args.verbose`. If an argument has a hyphen, like `--dry-run`,
            the hyphen becomes an underscore, i.e. `args.dry_run`.

    """
    add_args: list[tuple[list[str], dict[str, str]]] | None = program_args()
    args: argparse.Namespace = parse_cli_args(
        program_name="python -m git_prune",
        add_args=add_args,
        description="Delete local branches that have been removed from the remote. Use --dry-run to prevent any actions on git branches.",
    )

    logging.basicConfig(
        level="DEBUG" if args.verbose else "INFO",
        format=log_msg_fmt,
        datefmt=log_msg_datefmt,
    )

    log.debug(
        f"Repository path: {args.repo_path}, Dry run: {args.dry_run}, Verbose: {args.verbose}, Force: {args.force}"
    )

    return args


def main(
    repo_path: str = DEFAULT_REPO_PATH,
    dry_run: bool = False,
    force: bool = False,
    protected_branches: list[str] = PROTECTED_BRANCHES,
) -> list[str]:
    """Method to run when this script is called directly.

    Params:
        repo_path (str): (Default: ".") Path to the local git repository.
        dry_run (bool): If `True`, skip all operations that would alter git branches.
        force (bool): If `True`, when `git branch -d` fails, function will retry with `-D`.
            If this fails, a final attempt will be made using the host's `git` via `subprocess`.
        protected_branches (list[str]): List of branch names that will not be altered.

    Returns:
        (list[str]): A list of branches deleted from the local repository.

    """
    log.debug(f"Found git: {GIT_INSTALLED}")
    log.debug(f"Python version: {PYTHON_VERSION}")
    log.debug(f"Protected branches: {protected_branches}")

    repo: git.Repo = init_repo(repo_path)

    deleted_branches: list[str] = clean_branches(
        repo=repo,
        dry_run=dry_run,
        force=force,
        protected_branches=protected_branches,
    )

    if deleted_branches:
        ## Re-check local branches
        _local_branches: list[str] = get_local_branches(repo=repo)

        log.debug(f"Refreshed local branches: {_local_branches}")

    return deleted_branches


if __name__ == "__main__":
    ## Run argument parser & logging config, get list of args from cli
    args: argparse.Namespace = setup()
    ## Initialize list of branch names to add to PROTECTED_BRANCHES.
    #  Do not modify this list directly. Use extra_protected_branches.append("branch_name") on lines below
    extra_protected_branches: list[str] = []

    protected_branches: list[str] = PROTECTED_BRANCHES + extra_protected_branches
    main(
        repo_path=args.repo_path,
        dry_run=args.dry_run,
        force=args.force,
        protected_branches=protected_branches,
    )
