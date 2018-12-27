from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(name="pymusician",
      version="1.0.2",
      description="A python package for music composition and analysis.",
      long_description="""
      Read the README here:
      https://github.com/ScottMorse/PyMusician
      This is a python package for representing musical structures. Its features have less to do with audio file production/management, and more with analysis and composition. However, the concepts represented here could be combined with other music/audio related code to make sophisticated musical projects.
      """,
      url="https://github.com/ScottMorse/PyMusician",
      author="Scott Morse",
      author_email="scottmorsedev@gmail.com",
      license="Apache",
      packages=["pymusician"],
      include_package_data=True,
      install_requires=[
          'numpy',
      ],
      python_requires='>3.6',
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)