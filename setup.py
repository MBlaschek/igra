import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='igra',
    version='19.12',
    description='IGRAv2 radiosonde tools',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/MBlaschek/igra',
    author='MB',
    author_email='michael.blaschek@univie.ac.at',
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
    ],
    packages=setuptools.find_packages(),
    install_requires=['requests', 'numpy', 'pandas', 'xarray'],
    python_requires='>=3.6'
)

# Build and upload
# python3 setup.py bdist_wheel
# twine upload dist/* -r pypitest --verbose
