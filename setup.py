import os
from setuptools import setup

version_txt = os.path.join(os.path.dirname(__file__), 'colortrans', 'version.txt')
with open(version_txt, 'r') as f:
    version = f.read().strip()

with open('README.md') as f:
    long_description = f.read()

setup(
    author='Daniel Steinberg',
    author_email='ds@dannyadam.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'Topic :: Artistic Software',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
    ],
    description='An implementation of various color transfer algorithms',
    entry_points={
        'console_scripts': ['colortrans=colortrans.colortrans:main'],
    },
    keywords=['color', 'color-transfer'],
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    name='colortrans',
    package_data={'colortrans': ['version.txt']},
    packages=['colortrans'],
    python_requires='>=3.6',
    install_requires=['numpy', 'pillow'],
    url='https://github.com/dstein64/colortrans',
    version=version,
)
