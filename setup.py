from setuptools import setup

setup(name='igra',
      version='0.1',
      description='IGRA radiosonde tools',
      url='https://github.com/MBlaschek/igra',
      author='MB',
      author_email='michael.blaschek@univie.ac.at',
      license='UNIVIE GNU GPL',
      packages=['igra'],
      install_requires=['numpy', 'pandas', 'xarray'],
      zip_safe=False)
