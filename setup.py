from setuptools import setup, find_namespace_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(name="cellular_automata",
      version='1.0.0',
      author="rshanker779",
      author_email="rshanker779@gmail.com",
      description="Cellular automata in python, including implementation of Conway's game" \
                  "of life and some terrain generation",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/rshanker779/cellular_automata/tree/master",
      license='MIT',
      python_requires='>=3.5',
      install_requires=['numpy',
                        'matplotlib',
                        'setuptools'],
      packages=['conway', 'common', 'terrain_generation'],
      entry_points={'gui_scripts': ['conway_=conway.conway:main', 'terrain_=terrain_generation.terrain:main']},
      zip_safe=True

      )
