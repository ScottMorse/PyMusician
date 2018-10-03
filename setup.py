from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(name="pymusician",
      version="0.1",
      description="A python package for music composition and analysis.",
      url="https://github.com/ScottMorse/PyMusician",
      author="Scott Morse",
      author_email="scottmorsedev@gmail.com",
      lisence="GPL",
      packages=["pymusician"],
      include_package_data=True,
      install_requires=[
          'numpy',
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)