from dotenv import load_dotenv

load_dotenv()

import asyncio
from enum import Enum

import click

from csa.download import CsaDownloads
from csa.preprocess import CsaPreProcess

CliAction = Enum(
    "cli_actions",
    ("download", "extract", "extract-embedded", "preprocess"),
)


@click.command(
    context_settings=dict(
        ignore_unknown_options=True,
        allow_extra_args=True,
    )
)
@click.option(
    "--action",
    required=True,
    type=click.Choice(list(map(lambda x: x.name, CliAction)), case_sensitive=True),
)
@click.pass_context
def cli(ctx, action: CliAction):
    args = dict()
    for item in ctx.args:
        args.update([item.split("=")])
    click.echo(f"... Executing <{action}> {ctx.args}...")
    if action == "download":
        downloads = CsaDownloads()
        downloads.download_data()
        downloads.download_tweets()
    elif action == "extract":
        downloads = CsaDownloads()
        downloads.extract_tweets()
        downloads.extract_datasets()
    elif action == "extract-embedded":
        downloads = CsaDownloads()
        downloads.extract_embedded_datasets()
        downloads.extract_datasets()
    elif action == "preprocess":
        preprocess = CsaPreProcess()
        preprocess.preprocess_tweets()
    else:
        click.echo(f"Invalid action: {action}")
    click.echo(f"... Done <{action}> {ctx.args}...")


def _is_true(key, args) -> bool:
    return to_bool(args.get(f"{key}", False))


def to_bool(value) -> bool:
    if value == "true":
        return True
    elif value == "True":
        return True
    elif value == "false":
        return False
    elif value == "False":
        return False
    elif value == 0:
        return False
    elif value == 1:
        return True
    else:
        raise ValueError("Value was not recognized as a valid Boolean.")
