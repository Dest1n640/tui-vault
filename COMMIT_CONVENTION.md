# Commit Convention

We use [Conventional Commits](https://www.conventionalcommits.org/).
Every commit message should be structured as follows:

`<type>(<optional scope>): <description>`

## Types:
* **feat**: A new feature (e.g., adding a new screen, new C++ crypto function)
* **fix**: A bug fix
* **refactor**: Code changes that neither fix a bug nor add a feature
* **style**: Formatting, missing semi-colons, etc. (no code change)
* **docs**: Documentation only changes
* **chore**: Updating build tasks, package manager configs, etc.
* **build**: Changes that affect the build system (CMake, pyproject.toml)
* **test**: Adding missing tests or correcting existing tests

## Rules:
1. All commit messages MUST be in English.
2. Use the imperative mood in the description ("add feature" not "added feature").
3. Keep the first line under 72 characters.
