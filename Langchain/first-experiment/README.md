## Langchain demos
There are several demo scenarios how langchain could be used in simple case with or without pydantic output parser

## Running the project
To run this project you I use conda and uv combination.
You can use the same combination or use just `uv`.

## Pyproject + conda-uv
Pyproject file contains the following configuration which prevents venv folder creation.  
All dependencies will be installed into the active conda environment.

```toml
[tool.uv]
no-venv = true
````

Create and activate a conda environment (all dependencies will be installed into `conda` environment):
```bash
# create conda environment with defined python version
conda create -n myproject python=3.12
# Activate your conda environment first
conda activate langchain-first-experiments

# With UV_NO_VENV=1 set, these install into active conda environment
uv add requests
uv add fastapi
uv add pytest --dev

# This way:
# Packages install into your conda environment
# PyCharm sees all packages
# No .venv folder created
```
## Ignore .venv for all applications
```bash
# Add to ~/.bashrc or ~/.zshrc (permanent)
export UV_NO_VENV=1
# Now it works for all conda environments in all your projects
conda activate any-created-environment
uv sync  # Will always use the active conda environment

```
