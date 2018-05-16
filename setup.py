from setuptools import setup

with open('README.md') as f:
    readme = f.read()

setup(
    name='staintools',
    version='0.0.1',
    description='A package for stain normalization, augmentation and more.',
    long_description=readme,
    author='Peter Byfield',
    author_email='byfield554@gmail.com',
    url='https://github.com/Peter554/StainTools',
    packages=['staintools'],
    install_requires=['numpy',
                      'opencv-python',
                      'matplotlib',
                      'jupyter'
                      ]
)