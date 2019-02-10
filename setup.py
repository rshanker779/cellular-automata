from setuptools import setup, find_namespace_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(name="conways-game-of-life",
      version='1.0.0',
      author="rshanker779",
      author_email="rshanker779@gmail.com",
      description="Simple python implementation of Conway's game" \
                  "of life",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/rshanker779/conways-game-of-life/tree/master",
      license='MIT',
      python_requires='>=3.5',
      install_requires=['numpy',
                        'matplotlib',
                        'setuptools'],
      packages=find_namespace_packages(),

      )
