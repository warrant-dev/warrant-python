import pathlib
from setuptools import setup

DIR = pathlib.Path(__file__).parent
README = (DIR / "README.md").read_text()

setup(
    name="warrant-python",
    version="2.2.0",
    description="Python SDK for Warrant",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Warrant",
    author_email="hello@warrant.dev",
    url="https://github.com/warrant-dev/warrant-python",
    license="Apache Software License (http://www.apache.org/licenses/LICENSE-2.0.txt)",
    keywords="warrant api authorization access control",
    packages=["warrant"],
    install_requires=["requests"],
    project_urls={
        "Bug Tracker": "https://github.com/warrant-dev/warrant-python/issues",
        "Documentation": "https://docs.warrant.dev",
        "Source Code": "https://github.com/warrant-dev/warrant-python",
    },
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
