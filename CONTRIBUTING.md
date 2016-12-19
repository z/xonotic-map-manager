# Notes for Xonotic Map Manager Contributors

## Learning Xonotic Map Manager

The fastest way to learn is to read the [documentation](http://xonotic-map-manager.readthedocs.io/en/develop/api.html).

## Before filing an issue

- Reporting a potential bug? Please read the "[How to file a bug report](https://github.com/z/xonotic-map-manager/blob/develop/CONTRIBUTING.md#how-to-file-a-bug-report)" section to make sure that all necessary information is included.

- Contributing code? Be sure to review the [contributor checklist](https://github.com/z/xonotic-map-manager/blob/develop/CONTRIBUTING.md#contributor-checklist) for helpful tips on the tools we use to build Xonotic Map Manager.

## Contributor Checklist

* Create a [GitHub account](https://github.com/signup/free).

* [Fork Xonotic Map Manager](https://github.com/z/xonotic-map-manager/fork).

* Install xmm in development move, preferably inside of a *virtual environment*, see the [README](https://github.com/z/xonotic-map-manager/tree/master/README.md) for details.

* Keep xmm current. Keep the repository up-to-date and rebase work-in-progress frequently with `git pull --rebase` to make merges simpler.

* Learn to use [git](http://git-scm.com), the version control system used by GitHub and the Xonotic project. Try a tutorial such as the one [provided by GitHub](http://try.GitHub.io/levels/1/challenges/1).

* For more detailed tips, read the [submission guide](https://github.com/z/xonotic-map-manager/blob/develop/CONTRIBUTING.md#submitting-contributions) below.

* Have fun!

## How to file a bug report

A useful bug report filed as a GitHub issue provides information about how to reproduce the error.

1. Before opening a new [GitHub issue](https://github.com/z/xonotic-map-manager/issues):
  - Try searching the existing issues.
  - Try some simple debugging techniques to help isolate the problem.
    - Try running the code with the debug log settings

2. If the problem is caused by a package in `requirements.in` rather than core xmm, file a bug report with the relevant package author rather than here.

3. When filing a bug report, provide where possible:
  - The full error message, including the backtrace.
  - A minimal working example, i.e. the smallest chunk of code that triggers the error. Ideally, this should be code that can be pasted into a REPL or run from a source file. If the code is larger than (say) 50 lines, consider putting it in a [gist](https://gist.github.com).
  - The version of xmm as provided by the `xmm --version` command. Occasionally, the longer output produced in `~/.xmm/xmm.log` may be useful also, especially if the issue is related to a specific package.

4. When pasting code blocks or output, put triple backquotes (\`\`\`) around the text so GitHub will format it nicely. Code statements should be surrounded by single backquotes (\`). Be aware that the `@` sign tags users on GitHub, so references to macros should always be in single backquotes. See [GitHub's guide on Markdown](https://guides.github.com/features/mastering-markdown/) for more formatting tricks.

## Submitting contributions


### Writing tests

There are never enough tests.

1. Browse through existing [tests](./tests)

2. Write your tests using [pytest](http://doc.pytest.org/en/latest/)

3. Run `make tests` to run your tests

5. Submit the test as a pull request (PR).

### Improving documentation

*By contributing documentation to Xonotic Map Manager, you are agreeing to release it under the [MIT License](https://github.com/z/xonotic-map-manager/tree/master/LICENSE.md).*

Xonotic Map Manager's documentation source files are stored in the `docs/` directory. Like everything else these can be modified using `git`. Documentation is built with [sphinx](http://www.sphinx-doc.org/), which uses Restructured Text syntax. The HTML documentation can be built locally by running

```
make docs
```

from Xonotic Map Manager's root directory. This will build the HTML documentation and place the resulting files in `doc/_build/html/`.

> **Note**
>
> When making changes to any of Xonotic Map Manager's documentation it is recommended that you run `make clean` to check the your changes are valid and do not produce any errors before opening a pull request.

#### News-worthy changes

For new functionality and other substantial changes, add a brief summary to `CHANGELOG.md`. The item should cross reference the pull request (PR) parenthetically, in the form `([#pr])`. To add the PR reference number, first create the PR, then push an additional commit updating `CHANGELOG.md` with the PR reference number.

### Contributing to core functionality or base libraries

*By contributing code to Xonotic Map Manager, you are agreeing to release it under the [MIT License](https://github.com/z/xonotic-map-manager/tree/master/LICENSE.md).*

The Xonotic Map Manager community uses [GitHub issues](https://github.com/z/xonotic-map-manager/issues) to track and discuss problems, feature requests, and pull requests (PR). You can make pull requests for incomplete features to get code review. The convention is to prefix the pull request title with "WIP:" for Work In Progress, or "RFC:" for Request for Comments when work is completed and ready for merging. This will prevent accidental merging of work that is in progress.

Add new code to Xonotic Map Manager's base libraries as follows:

 1. Edit the appropriate file in the `xmm/` directory, or add new files if necessary. Create tests for your functionality and add them to files in the `tests/` directory.

 2. Add any new files to `config.py` in order `util.create_if_not_exists` them.
 
 3. Add any new artifacts to `.gitignore`

Build as usual, and do `make clean && make lint && make tests` to test your contribution.

Make sure that [Travis](http://www.travis-ci.org) greenlights the pull request with a [`Good to merge` message](http://blog.travis-ci.com/2012-09-04-pull-requests-just-got-even-more-awesome/).

### Code Formatting Guidelines

#### General Formatting Guidelines for Python code contributions

 - PEP-8 compliance minus the ignored rules in the `Makefile`'s `lint` task. 

### Git Recommendations For Pull Requests

 - Branch off `develop` with your `feature/` or `bugfix/` prefix, e.g. `git checkout develop && git checkout -b feature/my-cool-feature`
 - Avoid working from the `master` branch of your fork, creating a new branch will make it easier if Xonotic Map Manager's `master` changes and you need to update your pull request.
 - Try to [squash](http://gitready.com/advanced/2009/02/10/squashing-commits-with-rebase.html) together small commits that make repeated changes to the same section of code so your pull request is easier to review, and Xonotic Map Managers's history won't have any broken intermediate commits. A reasonable number of separate well-factored commits is fine, especially for larger changes.
 - If any conflicts arise due to changes in Xonotic Map Managers's `develop`, prefer updating your pull request branch with `git rebase` versus `git merge` or `git pull`, since the latter will introduce merge commits that clutter the git history with noise that makes your changes more difficult to review.
 - Descriptive commit messages are good.
 - Using `git add -p` or `git add -i` can be useful to avoid accidentally committing unrelated changes.
 - GitHub does not send notifications when you push a new commit to a pull request, so please add a comment to the pull request thread to let reviewers know when you've made changes.
 - When linking to specific lines of code in discussion of an issue or pull request, hit the `y` key while viewing code on GitHub to reload the page with a URL that includes the specific version that you're viewing. That way any lines of code that you refer to will still make sense in the future, even if the content of the file changes.
 - Whitespace can be automatically removed from existing commits with `git rebase`.
   - To remove whitespace for the previous commit, run
     `git rebase --whitespace=fix HEAD~1`.
   - To remove whitespace relative to the `master` branch, run
     `git rebase --whitespace=fix master`.

## Resources

* xonotic-map-manager
  - **Homepage:** <https://github.com/z/xonotic-map-manager>
  - **IRC:** <http://webchat.freenode.net/?channels=xonotic>
  - **Source code:** <https://github.com/z/xonotic-map-manager>
  - **Git clone URL:** <git://github.com/z/xonotic-map-manager.git>
  - **Documentation:** <http://xonotic-map-manager.readthedocs.io/en/latest>
  - **Build Status:** <https://travis-ci.org/z/xonotic-map-manager.svg?branch=develop>

* Using GitHub
  - [General GitHub documentation](http://help.github.com/)
  - [GitHub pull request documentation](http://help.github.com/send-pull-requests/)