
# Set ENV_FILE variable if it wasn't set already (for example, through shell)
ENV_FILE ?= ./deploy-dev/.env.dev

# Load env vars from file to shell
ifneq (,$(wildcard $(ENV_FILE)))
    include $(ENV_FILE)
    export
endif



dev:
	uv run fastapi dev main.py --host $(FASTAPI_HOST) --port $(FASTAPI_PORT)
