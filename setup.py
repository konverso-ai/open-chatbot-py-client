import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="open-chatbot-py-client",
    version="0.1.0",
    author="Konverso",
    author_email="contact@konverso.ai",
    description="Client to access any chatbot compliant with the Alliance for Open Chatbot standard",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.konverso.ai",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
