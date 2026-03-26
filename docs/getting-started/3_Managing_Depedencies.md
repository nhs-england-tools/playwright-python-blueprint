# Getting Started #3: Managing Dependencies

This guide outlines the guidance for managing dependencies within this project, specifically
Python packages and GitHub action uses.

## Contents

- [Getting Started #3: Managing Dependencies](#getting-started-3-managing-dependencies)
  - [Contents](#contents)
  - [Dependency Management Considerations](#dependency-management-considerations)
  - [How Dependencies Are Managed](#how-dependencies-are-managed)
    - [GitHub Actions](#github-actions)
    - [Python](#python)
      - [How Packages Are Managed](#how-packages-are-managed)
      - [Managing `requirements-lock.txt`](#managing-requirements-locktxt)

## Dependency Management Considerations

When managing any external dependencies within an NHS England project, we should always aim to reference
the versions of these using the commit SHA (hash) value rather than version numbers directly. This is
primarily due to a number of recent security incidents relating to GitHub Actions being compromised and
maliciously updated, so by locking dependencies to very specific code that we know is safe, we can
incrementally update code and mitigate the risk of a GitHub Action or Python project with malicious
code being executed on our devices or GitHub Action runners.

Working in this way also provides the following benefits:

- In CI/CD workflows, we can ensure that we are always running the same code, mitigating issues arising as a result of unexpected updates.
- We prevent downloading a tag that has been spoofed by using a content-addressed mechanism instead.
- We can manage updates to actions in a way that allows us to assure the updated versions work as intended with our workflows.

## How Dependencies Are Managed

### GitHub Actions

With any GitHub actions, we should always reference the commit SHA of the release we want to use, so
for example if we want to reference an external marketplace action, we should do so by specifying the
SHA as the version number, followed by a comment indicating the version number like so:

```yaml
    - name: "Authenticate to send the report"
      uses: aws-actions/configure-aws-credentials@8df5847569e6427dd6c4fb1cf565c83acfa8afa7 # v6.0.0
```

> NOTE: This only applies to externally managed dependencies, not those that are managed by the
> team directly.

### Python

#### How Packages Are Managed

Python packages in this project are managed by the following files:

| File                                                   | Purpose                                                                                                                                                                                                      |
| ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [`requirements.txt`](../../requirements.txt)           | This file references the packages needed to run the Playwright project and any other dependencies we may want to run as part of a GitHub Action workflow or locally.                                         |
| [`requirements-dev.txt`](../../requirements-dev.txt)   | This file references the packages needed locally to allow for additional development actions, but also installs everything listed in `requirements.txt`.                                                     |
| [`requirements-lock.txt`](../../requirements-lock.txt) | This file references the commit SHA values for the package versions identified within `requirements.txt`, and is the file that should be used to build any Python code as part of a GitHub Actions workflow. |

#### Managing `requirements-lock.txt`

With any Python packages, we should update the appropriate version number in
[`requirements.txt`](../../requirements.txt) and then use the `pip-compile` command
from `pip-tools` (installed via [`requirements-dev.txt`](../../requirements-dev.txt)) to generate
the [`requirements-lock.txt`](../../requirements-lock.txt) file.

The lock file stores all the commit SHA values that are applicable
to our project, and it is this file that is used to install packages when executing any code
within the GitHub Actions workflows.

The following command can be used to regenerate the file when package versions have been changed
(e.g. by a Dependabot update) and then run in the workflow to ensure changes are compatible
before merging:

```shell
pip-compile --generate-hashes requirements.txt --output-file requirements-lock.txt
```
