## Setting up pre-push hook

This repository includes a script that checks whether the current version of the package is already published on PyPI, to prevent accidental re-use of version numbers. This script is intended to be used as a Git pre-push hook, which means it runs automatically every time you push to the repository.

To set up this hook:

1. Copy the `pre_push_check.py` script to the `.git/hooks` directory and rename it to `pre-push`.

    ```
    cp pre_push_check.py .git/hooks/pre-push
    ```

2. Make the script executable.

    ```
    chmod +x .git/hooks/pre-push
    ```

Now every time you use `git push`, Git will first run this script. If the script finds that the current version is already on PyPI, it will prevent the push and output a relevant error message.
