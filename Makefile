.PHONY: help
.DEFAULT_GOAL := help
export TF_VAR_release_name := production
help:
	@echo "---------------------------------------------------------------------------------------"
	@echo ""
	@echo "				CLI"
	@echo ""
	@echo "---------------------------------------------------------------------------------------"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"; printf "Usage: make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-25s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Development

dev_env:
	virtualenv venv
	./venv/local/bin/activate

dev_install: dev_env
	pip install -r requirements.txt && pip install --editable .

dev_clean:
	rm -rf venv
