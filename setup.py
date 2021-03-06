import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gesture-rec-pkg",
    version="0.0.1",
    description="Gesture Recognition",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marina-dunn/SENG499",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
          'face-recognition',
      ],
)
