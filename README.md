# CPA
## Continuous Phishing Assessment

### Project Directory
- [Client](https://github.com/cisagov/cpa/tree/develop/client)
- [Controller](https://github.com/cisagov/cpa/tree/develop/controller)
- [GoPhish](https://github.com/cisagov/cpa/tree/develop/gophish)

### Requirements
* For local setup, Get the right flavor of Docker for your OS...
    - [Docker for Mac](https://docs.docker.com/docker-for-mac/install/)
    - [Docker for Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
    - [Docker for Windows](https://docs.docker.com/docker-for-windows/install/)

    **Note:** The recommended requirement for deployment of this project is 4 GB RAM.
    For Docker for Mac, this can be set by following these steps:

    Open Docker > Preferences > Advanced tab, then set memory to 4.0 GiB

## Local project setup:

Create your .env files
- `cp ./controller/etc/env.dist .env`
- `cp ./gophish/etc/env.dist .env`

Build containers
- `make build`

Run your web application locally
- `make up`

Stop containers
- `make stop`

Remove containers
- `make down`

## Contributing ##

We welcome contributions!  Please see [here](CONTRIBUTING.md) for
details.

## License ##

This project is in the worldwide [public domain](LICENSE).

This project is in the public domain within the United States, and
copyright and related rights in the work worldwide are waived through
the [CC0 1.0 Universal public domain
dedication](https://creativecommons.org/publicdomain/zero/1.0/).

All contributions to this project will be released under the CC0
dedication. By submitting a pull request, you are agreeing to comply
with this waiver of copyright interest.
