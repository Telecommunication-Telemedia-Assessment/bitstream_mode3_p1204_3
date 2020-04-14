#!/usr/bin/env python3
# requires toml to be installed
# this tool is specific for poetry projects
import toml
import os

print("perform release of current version")

with open("pyproject.toml") as xfp:
    cfg = toml.load(xfp)

current_version = cfg["tool"]["poetry"]["version"]
print(f"release current version {current_version}")
cmd = f"""git tag -a v{current_version} -m "Releasing version v{current_version}" """

os.system(cmd)

cmd = "git remote | xargs -i git push {} " + f"v{current_version}"
os.system(cmd)

current_version_parts = list(map(int, current_version.split(".")))
current_version_parts[-1] += 1

next_version = ".".join(map(str, current_version_parts))
print(f"move to next version inside repo: {next_version}")
print(next_version)

# update pyproject.toml
print("update pyproject.toml")
cfg["tool"]["poetry"]["version"] = next_version
with open("pyproject.toml", "w") as xfp:
    toml.dump(cfg, xfp)

# update cfg["tool"]["poetry"]["name"]/__init__.py

init_py = f"""{cfg["tool"]["poetry"]["name"]}/__init__.py"""
content = []
print(f"update {init_py}")
with open(init_py) as xfp:
    for x in xfp.readlines():
        if "__version__ = " in x:
            x = f"""__version__ = "{next_version}" #"""
        content.append(x)

with open(init_py, "w") as xfp:
    xfp.write("".join(content))

os.system(f"""git commit -m"move to next version: {next_version}" . """)
os.system("git remote | xargs -i git push {} ")