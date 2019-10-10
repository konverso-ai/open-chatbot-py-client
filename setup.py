import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="open-chat-bot-client",
    version="0.0.1",
    author="Konverso",
    author_email="",
    description="Client for Open Chat Bot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://konverso.ai",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
