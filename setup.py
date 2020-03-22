from setuptools import setup
import re

requirements = []
with open('requirements.txt') as f:
  requirements = f.read().splitlines()

version = ''
with open('classcharts/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

readme = ''
with open('README.md') as f:
    readme = f.read()

setup(name='classcharts.py',
      author='NCPlayz',
      author_email='chowdhurynadir0@outlook.com',
      url='https://github.com/NCPlayz/classcharts.py',
      project_urls={
        "Issue tracker": "https://github.com/NCPlayz/classcharts.py/issues",
      },
      version=version,
      packages=['classcharts', 'classcharts.homework', 'classcharts.student'],
      license='MIT',
      description='A python wrapper for the Classcharts API',
      long_description=readme,
      long_description_content_type='text/markdown',
      install_requires=requirements,
      python_requires='>=3.7.0',
)