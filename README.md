# Cephalon Seren

![GitHub release (with filter)](https://img.shields.io/github/v/release/MasterJ93/cephalon_seren)
![Discord](https://img.shields.io/discord/864182092271190096)

![Static Badge](https://img.shields.io/badge/I'm%20detecting%20a%20large%20security%20force%20heading%20your%20way-It's%20the%20Grineer.-purple)

Cephalon Seren is a Warframe-focused Discord bot. Even though his main goal is to moderate the Shinobi of the Lotus Discord server, he also helps with onboarding new members, delivers invite request, and posting billboards for other clans.

If you'd like to join the Shinobi of the Lotus clan or its respective alliance, you can visit us at <https://discord.gg/fpg88dzeyP>. We do require you to be actively playing Warframe, however. If you want to join the clan, you need to at least be 18 years old as well.

## Installation

### Production

To put this into a server or host it onto your local computer, we require a few prerequisites:

* Python 3.10 or higher.
* `discord.py`
* `aiofiles`
* (Optional, but recommended) `pyenv-virtualenv` (for managing the project-specific virtual environments)

### Development

For development, we also require the following:

* `pytest`
* `pytest-asyncio`

### Setting up the Environment

1. **Install `pyenv` and `pyenv-virtualenv`**

   If you haven't already installed `pyenv` and `pyenv-virtualenv`, please follow the instructions on the [`pyenv`](https://github.com/pyenv/pyenv) and [`pyenv-virtualenv`](https://github.com/pyenv/pyenv-virtualenv) GitHub pages respectively.

2. **Clone the Repository**:

   ```bash
   git clone https://github.com/MasterJ93/cephalon_seren.git
   cd cephalon-seren
   ```

3. **Setup the Python Environment**:

   When you enter the project directory, `pyenv` should automatically detect and set the Python version and virtual environment as specified in the ``.python-version`` file.

   If it's your first time, you'll need to create the virtual environment:

   ```bash
   pyenv virtualenv 3.10 cephelon-seren-venv
   ```

4. **Activate the Virtual Environment**:
   This step is usually automatic thanks to the `.python-version` file in the project directory. If you need to activate the environment manually, use:

   ```bash
   pyenv activate cephelon-seren-venv
   ```

5. **Install Dependencies**:
   Once your environment is set up and activated, install the project dependencies. If you're on a development environment, use:

   ```bash
   pip install -r dev-requirements.txt
   ```

   For a production environment, use:

   ```bash
   pip install -r prod-requirements.txt
   ```

### Notes for Non-`pyenv` Users

If you're not using `pyenv``, you can set up your Python environment using your preferred method, but ensure you are using the Python version specified in the .python-version file to avoid compatibility issues.

## Contributing

If you'd like to help work on this project, you're more than welcome to! There's a few things to keep in mind:

* All formatting should adhere to [PEP8 guidelines](https://peps.python.org/pep-0008/).
* When sending a Pull Request, make sure you follow the instructions of the guidelines in there.
* All tests must pass before the Pull Request can be considered for approval.

Above all, ensure that your coding style matches the existing code in the project.

## Getting Help

If you need help with understanding anything, let me (@MasterJ93) know. Or send an issue: whether for a bug, feature request, or linking a Pull Request to one.

## Licence

This project is licensed under the MIT License - see the LICENCE for details.

### Dependencies' Licenses

This project uses third-party libraries or dependencies, each with their own licenses:

* `aiofiles` is licensed under the Apache License 2.0. See the NOTICE file for more information.
