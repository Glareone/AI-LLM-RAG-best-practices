# MCP SERVER EXAMPLE USING FASTMCP

Project setup for macOS:
### Install uv globally (one-time setup)
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```
 or: 

```
brew install uv
```

### Create virtual environment using uv
```
uv venv
```

### Install dependencies (creates .venv automatically)
```
uv pip install -r requirements.txt
```

### Run the server:
```
uv run python mcp_example.py
```

### Development:
#### Add new dependencies

```
uv add package-name
```

#### Add dev dependencies
```
uv add --dev pytest black
```

#### Update dependencies
```
uv lock --upgrade
```