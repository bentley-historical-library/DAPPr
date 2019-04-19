import setuptools

setuptools.setup(
    name="dappr",
    version="0.0.1",
    author="Bentley Historical Library",
    description="DSpace API Python Programming Language resource",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests",
        "humanize"
    ]
)
