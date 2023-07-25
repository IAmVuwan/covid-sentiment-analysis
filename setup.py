import setuptools

cli_name = "csa"

setuptools.setup(
    name=cli_name,
    version="0.0.1",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "setuptools",
    ],
    entry_points={
        "console_scripts": [
            f"{cli_name} = entrypoint:cli",
        ],
    },
)
