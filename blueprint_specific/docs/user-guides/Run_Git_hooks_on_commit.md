# Guide: Run Git hooks on commit

- [Guide: Run Git hooks on commit](#guide-run-git-hooks-on-commit)
  - [Overview](#overview)
  - [Key files](#key-files)
  - [Testing](#testing)

## Overview

Git hooks are scripts that are located in the [`./blueprint_specific/scripts/githooks`](../../blueprint_specific/scripts/githooks) directory. They are executed automatically on each commit, provided that the `make config` command has been run locally to set up the project. These same scripts are also part of the CI/CD pipeline execution. This setup serves as a safety net and helps to ensure consistency.

The [pre-commit](https://pre-commit.com/) framework is a powerful tool for managing Git hooks, providing automated hook installation and management capabilities.

## Key files

- Scripts
  - [`check-file-format.sh`](../../blueprint_specific/scripts/githooks/check-file-format.sh)
  - [`check-markdown-format.sh`](../../blueprint_specific/scripts/githooks/check-markdown-format.sh)
  - [`scan-secrets.sh`](../../blueprint_specific/scripts/githooks/scan-secrets.sh)
- Configuration
  - [`pre-commit.yaml`](../../blueprint_specific/scripts/config/pre-commit.yaml)
  - [`init.mk`](../../blueprint_specific/scripts/init.mk): make targets

## Testing

You can run and test the process by executing the following commands from your terminal. These commands should be run from the top-level directory of the repository:

```shell
make githooks-config
make githooks-run
```