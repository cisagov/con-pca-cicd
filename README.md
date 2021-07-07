# con-pca-cicd

This repository holds the automated pipeline for con-pca. The automated pipeline is a must so less time is spent on building/deploying manually and more time can be spent developing/testing and providing a valuable product.

## Github Actions

Github actions is used to run builds of the docker images, pushing them to AWS ECR and runs the terraform for the AWS deployments.

## Terraform

Terraform is used for deployments of resources to the INL and COOL environment.

## Environments

At the moment there are two different environments that we deploy to - INL (dev), COOL (staging, production). Two separate sets of terraform is required as the environments have different requirements. Hopefully at some point, this can be reduced to just the COOL environment.

### INL

There is currently an INL account that is used as a development environment. The terraform for that account is located [here](terraform/). The workflow for the INL environment is defined [here](.github/workflows/cicd.yml).

### COOL

Staging and production environments are deployed to the cool and the terraform for that is located [here](cool/). The workflow for the deployment to the COOL environment is defined [here](.github/workflows/cool.yml).

## Pipeline

As Github Actions does not have a good way to handle multi-repository pipelines, all the builds are in this repository, so credentials don't need added to be added to other repositories and the workflow can be defined in a single place with multiple triggers for that. Repository dispatch events are sent from the con-pca-api, con-pca-web, and con-pca-gophish repositories to build the respective docker container, push it to AWS ECR and then run the terraform to deploy the new containers.

## Deploying Manually

There is a [deploy](deploy.py) script that allows you to deploy manually. On configure, it will ask for a Github access token. You can find the instructions for creating one [here](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token). The following permissions are required.

- [ ] repo
  - [x] public_repo

After creating an access token, you can simply run the following for a deployment.

```python
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
