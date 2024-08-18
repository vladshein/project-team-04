from setuptools import setup, find_packages

setup(
    name="assistant-bot",
    version="0.8.0",
    author="project-team-04",
    description="The personal assistant bot",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/vladshein/project-team-04",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        # 'package_name>=version',
        "prompt_toolkit==3.0.47",
        "wcwidth==0.2.13",
        "tabulate==0.9.0",
    ],
    entry_points={
        "console_scripts": [
            "assistant-bot=src.main:main",
        ],
    },
)
