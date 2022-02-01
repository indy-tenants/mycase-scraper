#!/usr/bin/env python
from os import path
from typing import Union

from setuptools import find_packages

classifiers = [
      'Development Status :: 3 - Alpha',
      'Programming Language :: Python :: 3.8',
      'Programming Language :: Python :: 3.9',
      'License :: OSI Approved :: MIT License',
      'Operating System :: OS Independent',
]

main: Union[bytes, str] = path.join(path.abspath(path.dirname(__file__)))
with open(path.join(main, 'requirements.txt'), 'r', encoding='utf-8') as f:
    requirements = f.read().splitlines()

about = {}
with open(path.join(main, 'mycase_scraper', '__version__.py'), 'r', encoding='utf-8') as f:
    exec(f.read(), about)

import distutils.core
distutils.core.setup(
      name=about['__title__'],
      version=about['__version__'],
      author=about['__author__'],
      author_email=about['__author_email__'],
      description=about['__description__'],
      long_description_content_type='text/markdown',
      url=about['__url__'],
      license=about['__license__'],
      packages=find_packages(),
      classifiers=classifiers,
      install_requires=requirements,
      python_requires=">=3.8",
      zip_safe=False,
      entry_points={
          'console_scripts': ['mycase-scraper=mycase_scraper.scraper:main']
      },
      project_urls={
          'Source': 'https://github.com/indy-tenants/mycase-scraper'
      }
)
