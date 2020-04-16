#!/usr/bin/env python3
# requires toml to be installed
# this tool is specific for poetry projects
import toml
import sys
import subprocess
import argparse
import shlex


def run_cmd(cmd, dry_run=False):
    if dry_run:
        print(" ".join([shlex.quote(c) for c in cmd]))
        return ""
    else:
        return subprocess.check_output(cmd).decode("utf-8")


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

    with open("pyproject.toml") as xfp:
        cfg = toml.load(xfp)

    current_version = cfg["tool"]["poetry"]["version"]

    print(f"Current version: {current_version}")

    current_version_parts = list(map(int, current_version.split(".")))

    if len(current_version_parts) != 3:
        print("Version must have three parts!")
        sys.exit(1)

    if cli_args.version == "patch":
        current_version_parts[2] += 1
    elif cli_args.version == "minor":
        current_version_parts[1] += 1
        current_version_parts[2] = 0
    elif cli_args.version == "major":
        current_version_parts[0] += 1
        current_version_parts[1] = 0
        current_version_parts[2] = 0
    else:
        print("Invalid choice for version")
        sys.exit(1)

    next_version = ".".join(str(p) for p in current_version_parts)

    print(f"move to next version inside repo: {next_version}")

    # update pyproject.toml
    print("update pyproject.toml")
    cfg["tool"]["poetry"]["version"] = next_version
    if not cli_args.dry_run:
        with open("pyproject.toml", "w") as xfp:
            toml.dump(cfg, xfp)

    # update cfg["tool"]["poetry"]["name"]/__init__.py

    init_py = f"""{cfg["tool"]["poetry"]["name"]}/__init__.py"""
    content = []
    print(f"update {init_py}")
    if not cli_args.dry_run:
        with open(init_py) as xfp:
            for x in xfp.readlines():
                if "__version__ = " in x:
                    x = f"""__version__ = "{next_version}" #"""
                content.append(x)

        with open(init_py, "w") as xfp:
            xfp.write("".join(content))

    print("committing and pushing to remote")

    message = f"move to next version: {next_version}"
    run_cmd(["git", "commit", "-m", message], cli_args.dry_run)
    run_cmd(["git", "tag", f"v{next_version}"], cli_args.dry_run)

    changelog = run_cmd(["poetry", "run", "gitchangelog"], cli_args.dry_run)
    if not cli_args.dry_run:
        with open("CHANGELOG.md", "w") as ch:
            ch.write(changelog)

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
