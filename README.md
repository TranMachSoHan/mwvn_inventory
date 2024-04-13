# Template folder

## Getting started

- Clone this repository

- Press `Ctrl+Shift+P` - search for `Task: Run task` - and then execute `Setup Environement` 

- Once the prompt is open, input Odoo version number, path to Odoo directory and path to Enterprise directory respectively. Then a linter file should be generated as a result.  

- If the cloned project comes in as a single folder, rename the folder as `addons`, then look up `.:/mnt/extra-addons` in `docker-compose.override.yml` and change it to `./addons:/mnt/extra-addons`

- Enable linting on VSCODE - `Ctrl+Shift+P` - search for Python: Select Linter and select pylint

- Run `sudo ./start` or just `./start`. In case you are denied permission, run `chmod u+x ./start`. And if you are not able to run the command due to not found error, refer to this [Stack Overflow post](https://stackoverflow.com/questions/27275118/linux-shell-script-not-found-but-it-does-exist) for help



