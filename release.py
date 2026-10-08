#!/usr/bin/env python3
# requires uv to be installed
import sys
import subprocess
import argparse
import shlex


def run_cmd(cmd, dry_run=False):
    if dry_run:
        print(" ".join([shlex.quote(c) for c in cmd]))
        return ""
    else:
        try:
            return subprocess.check_output(cmd).decode("utf-8")
        except subprocess.CalledProcessError as e:
            print(e)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("version", choices=["patch", "minor", "major"])
    parser.add_argument(
        "-np", "--no-push", help="do not push commits/tags", action="store_true"
    )
    parser.add_argument(
        "-n", "--dry-run", help="only show what would be done", action="store_true"
    )
    cli_args = parser.parse_args()

    run_cmd(["git", "fetch", "--all"], cli_args.dry_run)
    status = run_cmd(["git", "status", "-sb"], cli_args.dry_run)
    if "behind" in status:
        print("Your local branch is behind the remote. Please run `git pull --rebase` first.")
        sys.exit(1)

    current_version = run_cmd(["uv", "version", "--short"]).strip()
    print(f"Current version: {current_version}")

    # update pyproject.toml and uv.lock
    print("update pyproject.toml")
    run_cmd(["uv", "version", "--bump", cli_args.version], cli_args.dry_run)
    if cli_args.dry_run:
        next_version = run_cmd(["uv", "version", "--short", "--bump", cli_args.version, "--dry-run"]).strip()
    else:
        next_version = run_cmd(["uv", "version", "--short"]).strip()

    print(f"move to next version inside repo: {next_version}")

    init_py = "p1204_3/__init__.py"
    content = []
    print(f"update {init_py}")
    if not cli_args.dry_run:
        with open(init_py) as xfp:
            for x in xfp.readlines():
                if "__version__ = " in x:
                    x = f"""__version__ = "{next_version}" #\n"""
                content.append(x)

        with open(init_py, "w") as xfp:
            xfp.write("".join(content))

    print("committing and pushing to remote")

    message = f"move to next version: {next_version}"
    run_cmd(["git", "commit", "-a", "-m", message], cli_args.dry_run)
    run_cmd(["git", "tag", f"v{next_version}"], cli_args.dry_run)

    changelog = run_cmd(["uv", "run", "gitchangelog"], cli_args.dry_run)
    if not cli_args.dry_run:
        with open("CHANGELOG.md", "w") as ch:
            ch.write(changelog)
    run_cmd(["git", "add", "CHANGELOG.md"], cli_args.dry_run)

    run_cmd(["git", "commit", "--amend", "--no-edit"], cli_args.dry_run)
    # repeat tag for changelog (forced)
    run_cmd(["git", "tag", "-f", f"v{next_version}"], cli_args.dry_run)

    if not cli_args.no_push:
        remotes = run_cmd(["git", "remote"]).rstrip()
        for remote in remotes.split("\n"):
            run_cmd(["git", "push", remote], cli_args.dry_run)
            run_cmd(["git", "push", remote, "--tags"], cli_args.dry_run)


if __name__ == "__main__":
    main()
