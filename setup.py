from setuptools import setup, find_packages

setup(
    name='staintools',
    version='2.1.2',
    description='A package for tissue image stain normalization, augmentation and more.',
    author='Peter Byfield',
    author_email='peter554-dev@protonmail.com',
    url='https://github.com/Peter554/StainTools',
    packages=find_packages(exclude=('tests')),
    install_requires=[
        'numpy',
        'matplotlib',
        'opencv-python'

        # Spams PyPI install is currently broken
        # 'spams'
    ]
)
