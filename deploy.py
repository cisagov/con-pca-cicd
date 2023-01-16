"""Script to deploy to staging or production COOL environments."""
import configparser

import click
import requests  # type: ignore


@click.group()
@click.pass_context
def cli(ctx):
    """Create cli."""
    return


def main():
    """Execute main."""
    cli.add_command(deploy)
    cli.add_command(configure)
    cli()


@click.command()
@click.option(
    "--environment",
    required=True,
    prompt=True,
    type=click.Choice(["sandbox", "inl-staging", "cool-staging", "production"]),
)
def deploy(environment):
    """Deploy to defined environment."""
    token = get_token()
    if not token:
        click.echo("no token found - running configure")
        configure()
        token = get_token()

    click.confirm(f"Are you sure you want to deploy {environment}?", abort=True)

    result = {}
    if environment == "production":
        result = deploy_production(token)
    elif environment == "cool-staging":
        result = deploy_cool_staging(token)
    elif environment == "inl-staging":
        result = deploy_inl_staging(token)
    elif environment == "sandbox":
        result = deploy_sandbox(token)

    if result.status_code != 204:
        click.echo(
            f"There was an error deploying {environment}, please check your token."
        )
    else:
        click.echo(f"Successfully started deployment for {environment}")


@click.command("configure")
@click.option("--token", required=True, prompt=True)
def configure(token):
    """Configure access point in config.ini file."""
    config = configparser.ConfigParser()
    config["DEFAULT"] = {"github_access_token": token}
    with open("config.ini", "w") as configfile:
        config.write(configfile)


def get_token():
    """Get token from config.ini file."""
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config["DEFAULT"].get("github_access_token")


def deploy_sandbox(token):
    """Deploy to INL sandbox environment."""
    return requests.post(
        url="https://api.github.com/repos/cisagov/con-pca-cicd/dispatches",
        json={"event_type": "deploy-sandbox", "client_payload": {}},
        headers=get_auth_header(token),
    )


def deploy_inl_staging(token):
    """Deploy to INL staging environment."""
    return requests.post(
        url="https://api.github.com/repos/cisagov/con-pca-cicd/dispatches",
        json={"event_type": "deploy-staging", "client_payload": {}},
        headers=get_auth_header(token),
    )


def deploy_cool_staging(token):
    """Deploy to COOL staging environment."""
    return requests.post(
        url="https://api.github.com/repos/cisagov/con-pca-cicd/dispatches",
        json={"event_type": "deploy-cool-staging", "client_payload": {}},
        headers=get_auth_header(token),
    )


def deploy_production(token):
    """Deploy to COOL production environment."""
    return requests.post(
        url="https://api.github.com/repos/cisagov/con-pca-cicd/dispatches",
        json={"event_type": "deploy-cool-production", "client_payload": {}},
        headers=get_auth_header(token),
    )


def get_auth_header(token):
    """Get authorization header."""
    return {"Authorization": f"Bearer {token}"}


if __name__ == "__main__":
    main()
