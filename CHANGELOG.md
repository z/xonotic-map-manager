##  0.8.0 / 2016-12-xx

### Added
* Multi-repo support
* Created documentation with sphinx, hosted at readthedocs.io
* Integrated tests and CI with travis
* arg completion for bash and zsh via argcomplete
* `-L` flag on the `xmm show` subcommand to explicitly indicate showing map details from a locally installed map. Otherwise, the source_collection cache is used for all information. 
* `-R` flag to specify a single repository if using many

### Changed
* Complete overhaul of code base exposing a Python API