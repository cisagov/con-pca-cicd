# con-pca-cicd

## Description

CICD repo for con-pca. Contains terraform for deployments and github actions jobs for building.

## Source Repositories

There are three different repositories that can trigger this pipeline to run via a [repository dispatch event](https://docs.github.com/en/actions/reference/events-that-trigger-workflows#repository_dispatch).

- [con-pca-api](https://github.com/cisagov/con-pca-api)
- [con-pca-web](https://github.com/cisagov/con-pca-web)
- [con-pca-gophish](https://github.com/cisagov/con-pca-gophish)

This pipeline can also be triggered on push to the develop branch on this repository via a [push event])

The source repositories access dispatch the CICD repository through the using of a [Github access token](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token). This access token is loaded into the secret called "CON_PCA_ACCESS_TOKEN".

## Deploying Manually

There is a [deploy](deploy.py) script that allows you to deploy manually. On configure, it will ask for a Github access token. You can find the instructions for creating one [here](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token). The following permissions are required.

- [ ] repo
  - [x] public_repo

After creating an access token, you can simply run the following for a deployment.

```basg
pip install -r requirements.txt
python deploy.py configure
python deploy.py deploy --environment staging|production
```

## Contributing

We welcome contributions! Please see [here](CONTRIBUTING.md) for
details.

## License

This project is in the worldwide [public domain](LICENSE).

This project is in the public domain within the United States, and
copyright and related rights in the work worldwide are waived through
the [CC0 1.0 Universal public domain
dedication](https://creativecommons.org/publicdomain/zero/1.0/).

All contributions to this project will be released under the CC0
dedication. By submitting a pull request, you are agreeing to comply
with this waiver of copyright interest.
