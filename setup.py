from os import path
from setuptools import setup, find_packages

_here = path.dirname(__file__)


dev_requirements = ["black==19.3b0", "flake8==3.7.8"]

setup(
    name="git-submodule-updater",
    version="0.0.1",
    author="Peter Bengtsson",
    author_email="mail@peterbe.com",
    url="https://github.com/peterbe/git-submodule-updater",
    description="Lemme make a PR for you to update that git submodule",
    long_description=open(path.join(_here, "README.md")).read(),
    license="MPL 2.0",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=["GitPython", "click", "PyGithub", "python-decouple"],
    extra_require={"dev": dev_requirements},
    entry_points="""
        [console_scripts]
        gsmu=gsmu.main:cli
    """,
    setup_requires=[],
    tests_require=["pytest"],
    keywords="git github submodule",
)
