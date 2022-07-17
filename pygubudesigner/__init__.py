__version__ = "0.28"

#
def get_requirements():
    """Get requirements for product environment, write the requirements of
    development environment in 'pygubudesigner.sh' file.

    Returns:
        list: The requirements for product environment.
    """

    return [
        # ("require","version","license","project_url")
        (
            "appdirs",
            ">=1.4.3",
            "MIT License",
            "http://github.com/ActiveState/appdirs",
        ),
        (
            "Mako",
            ">=1.1.4",
            "MIT License",
            "https://github.com/sqlalchemy/mako",
        ),
        (
            "screeninfo",
            ">=0.8",
            "MIT License",
            "https://github.com/rr-/screeninfo",
        ),
        (
            "pygubu",
            ">=0.23",
            "MIT License",
            "https://github.com/alejandroautalan/pygubu",
        ),
        (
            "black",
            ">=22.1.0",
            "MIT License",
            "https://github.com/psf/black",
        ),
    ]


def get_product_requirements():
    return get_requirements()


def get_setup_requirements():
    return [r[0] + r[1] for r in get_requirements()]
