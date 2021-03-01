# extend-euserv

[![python](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/extend-euserv.svg)](https://badge.fury.io/py/extend-euserv)

Extend expiry date of euserv.com

## Automate extending expiry date of euserv.com

*   Fork this repo [https://github.com/ffreemt/extend-euserv/fork](https://github.com/ffreemt/extend-euserv/fork)
*   Set the resultant repo `Secrets`

	|Name | Value |
	|--    | --    |
	|EUSERV_EMAIL:| your_euserv_email|
	|EUSERV_PASSWORD:| your_euserv_password |

*   [Optionally] Change `crontab` in line 6 of `.github/workflows/schedule-extend-euserv.yml`([link](https://github.com/ffreemt/extend-euserv/blob/master/.github/workflows/schedule-extend-euserv.yml)) to your like. (This online crontab editor may come handy [https://crontab.guru/#0_0_*/9_*_*](https://crontab.guru/#0_0_*/9_*_*))


## Installtion

```bash
not ready yet pip install extend-euserv
```
or clone [https://github.com/ffreemt/extend-euserv](https://github.com/ffreemt/extend-euserv) and install from the repo.

## Usage
### Supply euserv `email` and `password` from the command line:
```bash
python -m extend-euserv -u your_euserv_email -p password
```
or use directly the ``extend-euserv`` script:
```bash
extend-euserv -u your_euserv_email -p password
```

### Use environment variables `EUSERV_EMAIL` and `EUSERV_PASSWORD`
*   Set email/password from the command line:
	```bash
	set EUSERV_EMAIL=your_euserv_email  # export in Linux or iOS
	set EUSERV_PASSWORD=password
	```
*   Or set email/password  in .env, e.g.,
	```bash
	# .env
	EUSERV_EMAIL=your_euserv_email
	EUSERV_EMAIL=password

Run `extend-euserv` or `python -m  extend_euserv`:

```bash
extend-euserv
```

or

```bash
python -m extend_euserv
```

### Check information only

```bash
extend-euserv -i
```

or

```bash
python -m extend_euserv -i
```

###  Print debug info

```bash
extend-euserv -d
```

or

```bash
python -m extend_euserv -d
```

### Brief Help

```bash
extend-euserv --helpshort
```

or

```bash
python -m extend_euserv --helpshort
```

### Turn off Headless Mode (Show the browser in action)

You can configure `EUSERV_HEADFUL`, `EUSERV_DEBUG` and `EUSERV_PROXY` in the `.env` file in the working directory or any of its parent directoreis. For example,

```bash
# .env
EUSERV_HEADFUL=1
EUSERV_DEBUG=true
# EUSERV_PROXY
```

### Automation via Github Actions

It's straightforward to setup `extend-euserv` to run via Github Actions, best with an infrequent crontab.
*   Fork this repo
*   Setup `Actions secrets` via `Settings/Add repository secrets`:

|Name | Value |
|--    | --    |
|EUSERV_EMAIL:| your_euserv_email|
|EUSERV_PASSWORD:| your_euserv_password |

For example, in `.github/workflows/schedule-extend-euserv.yml`
```bash
name: schedule-extend-euserv

on:
  push:
  schedule:
    - cron: '10,40 3 */9 * *'
...
setup, e.g. pip install -r requirements.txt or
poetry install --no-dev
...

      - name: Testrun
        env:
          EUSERV_EMAIL: ${{ secrets.EUSERV_EMAIL }}
          EUSERV_PASSWORD: ${{ secrets.EUSERV_PASSWORD }}
        run: |
          python -m extend_euserv -d -i

```