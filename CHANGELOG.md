##  0.8.0 / 2016-12-xx

### Added
* Multi-repo support
* Created documentation with sphinx, hosted at readthedocs.io
* Integrated tests and CI with travis
* arg completion for bash and zsh via argcomplete
* `-L` flag on the `xmm show` subcommand to explicitly indicate showing map details from a locally installed map. Otherwise, the source_collection cache is used for all information. 
* `-R` flag to specify a single repository if using many
* `--version` flag
* User-configurable Logging

### Changed
* Complete overhaul of code base exposing a Python API
* No longer using pickle, storing data in *JSON*
* Configuration updates, see [Upgrading](http://xonotic-map-manager.readthedocs.io/en/latest/upgrading.html)