from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

setup(
    name='staintools',
    version='1.2.4',
    description='A package for tissue image stain normalization, augmentation and more.',
    long_description=readme,
    author='Peter Byfield',
    author_email='byfield554@gmail.com',
    url='https://github.com/Peter554/StainTools',
    packages=find_packages(exclude=('tests')),
    install_requires=['numpy',
                      'opencv-python',
                      'matplotlib',
                      'jupyter',
                      'future',
                      'cython'
                      ],
    classifiers=[
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.5'
    ]
)
