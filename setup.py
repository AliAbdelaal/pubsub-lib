import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

requirements = []
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="PubSubLib", # Replace with your own username
    version="0.0.1",
    author="Ali Abdelaal",
    author_email="aliabdelaal369@gmail.com",
    description="A simple unified pubsub library that supports kafka and google pubsub as backend.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AliAbdelaal/pubsub-lib",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=['PubSub'],
    install_requires=requirements,
    python_requires='>=3.7',
)