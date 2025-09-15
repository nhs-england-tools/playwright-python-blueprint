# This file is for you! Edit it to implement your own hooks (make targets) into
# the project as automated steps to be executed on locally and in the CD pipeline.

include scripts/init.mk

# ==============================================================================

# This allows the setup of Playwright by using a single command ready to use, and checks
# if the user is in a virtual environment before running the setup.

.PHONY: check-venv
check-venv: # Checks if in a Python venv / VIRTUALENV before installing a bunch of dependencies
	@python -c "import sys, os; \
venv = (hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) or 'VIRTUAL_ENV' in os.environ); \
import sys; sys.exit(0 if venv else 1)"

setup-playwright: # Install Playwright and associated packages, and create local.env
	@echo "Checking for virtual environment..."
	$(MAKE) check-venv || (echo "ERROR: Not in a virtual environment, please create before running this command!"; exit 1)

	@echo "Install Playwright"
	pip install -r requirements.txt
	playwright install

	@echo "Setup local.env file"
	python setup_env_file.py
