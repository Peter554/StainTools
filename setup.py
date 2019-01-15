from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name='staintools',
    version='2.1.0',
    description='A package for tissue image stain normalization, augmentation and more.',
    long_description=readme,
    author='Peter Byfield',
    author_email='byfield554@gmail.com',
    url='https://github.com/Peter554/StainTools',
    packages=find_packages(exclude=('tests')),
    install_requires=[
        'numpy',
        'opencv-python',
        'spams',
        'matplotlib'
    ]
)
