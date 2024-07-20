# VS Code Debug Configuration for Python Script

This section provides an explanation of the VS Code `launch.json` configuration file, which is used to set up debugging for a Python script. The configuration specifies how to run and debug `main.py` with specific arguments and environment variables.

## Overview

The `launch.json` file performs the following key tasks:
1. Defines the version of the configuration schema.
2. Specifies a configuration for running `main.py`.
3. Sets up arguments, console type, and environment variables for the debug session.

### Configuration Breakdown

- **version**: Specifies the version of the configuration schema.
- **configurations**: An array containing configuration objects.
```json

  "version": "0.2.0",
  "configurations":
```

#### Configuration Object


- **name**: The name of the configuration. This name will be displayed in the VS Code debug panel.
- **type**: Specifies the type of debugger to use. Here, it is set to `python`.
- **request**: Specifies the request type of the configuration. `launch` indicates that this configuration will launch the specified program.
- **program**: Specifies the path to the Python script to be executed. `${workspaceFolder}` is a variable that points to the root of the workspace.
- **args**: An array of command-line arguments to pass to the program. In this case, `--mode train --env local`.
- **console**: Specifies where to launch the debug session. `integratedTerminal` uses VS Code's integrated terminal.
- **env**: Specifies environment variables for the debug session.
- **PYTHONPATH**: Sets the `PYTHONPATH` environment variable to the workspace folder.
  
```json
{
  "name": "Python: Run main.py",
  "type": "python",
  "request": "launch",
  "program": "${workspaceFolder}/main.py",
  "args": ["--mode", "train", "--env", "local"],
  "console": "integratedTerminal",
  "env": {
    "PYTHONPATH": "${workspaceFolder}"
  }
}
```

