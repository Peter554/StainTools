from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name='staintools',
    version='0.0.2',
    description='A package for stain normalization, augmentation and more.',
    long_description=readme,
    author='Peter Byfield',
    author_email='byfield554@gmail.com',
    url='https://github.com/Peter554/StainTools',
    packages=find_packages(),
    install_requires=['numpy',
                      'opencv-python',
                      'matplotlib',
                      'jupyter'
                      ]
)