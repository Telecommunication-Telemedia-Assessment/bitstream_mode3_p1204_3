Changelog
=========


v0.1.3 (2022-05-03)
-------------------
- Update tests, there were no differences, only formatting. [Steve]
- Update requirements for docker. [Steve]
- Go to current scikit-learn version. [Steve]
- Remove unneeded dependency sklearn-json. [Steve]
- Changes to make it working with a newer version of sklearn. [Steve]
- Remove debugging code. [Steve]
- Update to never python packages. [Steve]
- Cleanup. [Steve]
- Minor fix in mos from r. [Steve]
- Update model.py. [rakeshraor]
- Removed debug print statement. [Steve Goering]
- Add version to the output report. [Steve Goering]
- Make feature values as separate key in the final report. [Steve
  Goering]
- Add more debug data to the report. [Steve Goering]
- Add some fallback error handling to process at least the other
  specified videos in case something is wrong with the video. [Steve]
- Create default model. [Steve]
- Remove poetry dependency within docker container. [Steve]
- Add requiements.txt for docker container. [Steve]
- Update readme. [Steve]
- Merge branch 'master' of github.com:Telecommunication-Telemedia-
  Assessment/bitstream_mode3_p1204_3. [Steve]
- Fix Docker build. [Werner Robitza]

  Fixes a bug with Poetry/Python 3.6, related to:

  - https://github.com/python-poetry/poetry/issues/1427#issuecomment-537260307
  - https://github.com/python-poetry/poetry/issues/3078
- Fix order of options for docker script. [Werner Robitza]

  Otherwise, -v will be passed to p1204 itself
- Minor edit. [rakeshraor]
- Merge branch 'master' of https://github.com/Telecommunication-
  Telemedia-Assessment/bitstream_mode3_p1204_3. [rakeshraor]
- Update README.md. [rakeshraor]
- Handling per-sec score calculation. [rakeshraor]
- Merge pull request #14 from Telecommunication-Telemedia-
  Assessment/viewing-distance. [Steve Göring]

  Fix usage of viewing distance and display size
- Fix usage of viewing distance and display size. [Werner Robitza]
- Add flag to deactivate caching of features, add __main__ to enable
  usage out of poetry. [Steve]
- Add hints of help to readme. [Steve]
- Add hints for not used params. [Steve]
- Add a hint about the input params. [Steve]
- Improve Dockerfile. [Werner Robitza]

  - Add dockerignore
  - Remove test videos from image, mount locally
- Add Dockerfile. [Max]

  added Dockerfile and Docker build and test script

  Update Dockerfile

  Removed comment for ENTRYPOINT, this was just for testing

  Update Dockerfile

  Changed to correct upstream
  Shallow cloning of repos
- Explain output format. [Werner Robitza]
- Mention memory requirements. [Werner Robitza]
- Add a line break in the python version variable inside the release
  script, this line break is required to not break the code. [Steve]
- Add a line break in the python version variable inside the release
  script, this line break is required to not break the code. [Steve]


v0.1.2 (2020-04-17)
-------------------
- Bump version. [Werner Robitza]
- Fix release script. [Werner Robitza]
- Update README.md. [Steve Göring]
- Update testcases to final model version. [Steve]
- Prevent prettifier for touching lookup tables. [Steve]
- Added missing import. [Steve]
- Cleanup temporary versioning changes that were not required. [Steve]
- Add error output to shellcall. [Steve]
- Merge branch 'master' of github.com:Telecommunication-Telemedia-
  Assessment/bitstream_mode3_p1204_3. [Steve]
- Merge pull request #7 from Telecommunication-Telemedia-Assessment/fix-
  release-2. [Steve Göring]

  Fix release script
- Merge pull request #7 from Telecommunication-Telemedia-Assessment/fix-
  release-2. [Steve Göring]

  Fix release script
- Push to all remotes. [Werner Robitza]
- Fix error with writing changelog. [Werner Robitza]
- Merge pull request #3 from Telecommunication-Telemedia-Assessment/fix-
  release. [Steve Göring]

  improve release script
- Improve release script. [Werner Robitza]

  - add a way to specify patch/minor/major
  - do not double push current version and next version; only push current version
  - add a way to dry-run before doing anything
  - add a way to prevent pushing
  - use subprocess instead of os.system
  - create a CHANGELOG automatically
- Typo fix. [Steve]
- Changed to prevent scikit learn warning #4 closed. [Steve]
- Merge pull request #5 from Telecommunication-Telemedia-
  Assessment/logging. [Steve Göring]

  add possibility to set different log levels
- Add possibility to set different log levels. [Werner Robitza]

  - add debug option to toggle debug logs
  - add quiet option to only show errors (enables parsing JSON output from stdout)
- Add devekopment version of the model. [Steve]
- Go to next version; cleanup some project settings. [Steve]
- Fix release script. [Steve]
- Update model coefficients to the ones used in the standard. [Steve]


v0.1.0 (2020-04-14)
-------------------
- Change videoparser update handling. [Steve]
- Add release tool to repo. [Steve]
- Add version string to module. [Steve]
- Merge branch 'master' of github.com:Telecommunication-Telemedia-
  Assessment/bitstream_mode3_p1204_3. [Steve]
- Minor edit. [rakeshraor]
- Small changes in readme, added new todo. [Steve]
- Add info msg. [Steve]
- Remove unneded import. [Steve]
- Pseudoupdate videoparser repo. [Steve]
- Fix build script for video parser, it is now build.sh minimal other
  changes regarding pathes. [Steve]
- Change date. [Steve]
- Removed version. [Steve]
- Prettify. [Steve]
- Add test vectors and add first unit test. [Steve]
- Add testreports. [Steve]
- Add tests. [Steve]
- Add install to check script. [Steve]
- Add prettify script and also perform it on the code, so now everything
  is prettified using black. [Steve]
- Small change. [Steve]
- Change some of the code parts, to make it simpler, added debug output
  of model internal steps. [Steve]
- Add unittest todo. [Steve]
- Add a simple check. [Steve]
- Removed version as report part idea. [Steve]
- Update libs to newer versions. [Steve]
- Add json load method. [Steve]
- Solved some todos. [Steve]
- Prettify outout of run. [Steve]
- Add wrapper code for json models. [Steve]
- Moved to serialized json models. [Steve]
- Minimal change. [Steve]
- Merge branch 'master' of github.com:Telecommunication-Telemedia-
  Assessment/bitstream_mode3_p1204_3. [Steve]
- Typo. [Werner Robitza]
- Change url of parser to final url. [Steve]
- Add requrements for parser to guide. [Steve]
- Add some more docu in readme. [Steve]
- Add licence file for bbb. [Steve]
- Change to new repository for bitstream parser, still some parts to be
  done. [Steve]
- Merged changes. [Steve]
- Fixed bug in per second score prediction. [rakesh]
- Added something or nothing, don't really remember. [rakesh]
- Fixed some bugs. [rakesh]
- Merge branch 'master' of https://avt10.rz.tu-ilmenau.de/git/avt-
  pnats2avhd/bitstream_mode3_p1204_3. [rakesh]
- Added fix to per-sec score calculation bug. [rakesh]
- Add some error handling. [Steve]
- Update ignore. [Steve]
- Update reports. [Steve]
- Fix bitdepth. [Steve]
- Videos for which the video parser fails. [Rakesh Rao Ramachandra Rao]
- Add todos. [Steve]
- Fix model missing thing. [Steve]
- Rephrase. [Steve]
- Prettify readme. [Steve]
- Add cli help output. [Steve]
- Update install guide. [Steve]
- Add support for output reports. [Steve]
- Merge branch 'master' of avt10.rz.tu-ilmenau.de:avt-
  pnats2avhd/bitstream_mode3_p1204_3. [Steve]
- Minor modification with affiliation. [Rakesh Rao Ramachandra Rao]
- Add missing test videos. [Steve]
- Prettify code a bit. [Steve]
- Fix typi, rename. [Steve]
- Add more ignore rules. [Steve]
- Restructure things, so far it runs. [Steve]
- Add duration to ffprobe. [Steve]
- Minimal changes to debug some parts, there is still something to be
  done, not sure if the current ffprobe result handling and bitstream
  handling will be done in the future. [Steve]
- Cleanup checks. [Steve]
- Add temp folder. [Steve]
- Add some more code from the VM, THIS IS NOT WORKING. [Steve]
- Add more dependencies. [Steve]
- Fix typo. [Steve]
- Change script name to p1204_3. [Steve]
- Poetry fixes. [Steve]
- Add licence file. [Steve]
- Add licence text to readme. [Steve]
- Add missing dependency. [Steve]
- Add codec check, add logging macros. [Steve]
- Change authors in readme formatting. [Steve]
- Add developers. [Steve]
- Typo. [Steve]
- Add changes for general model framework. [Steve]
- Add some checks. [Steve]
- Add initital files for project. [Steve]
- Initial commit. [Steve Göring]


