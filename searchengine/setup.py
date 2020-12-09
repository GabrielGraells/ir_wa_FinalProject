from setuptools import setup

setup(
    name="SearchEngine",
    version="1.0",
    py_modules=["twitterSE"],
    install_requires=[
        "Click",
        "Pandas"
    ],
    entry_points='''
        [console_scripts]
        twitterSE=twitterSE:cli
    ''',
) 