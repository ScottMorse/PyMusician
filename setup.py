from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name="musictools",
      version="0.1",
      description="A python package for music composition and analysis.",
      url="https://github.com/ScottMorse/Py-Music-Tools",
      author="Scott Morse",
      author_email="scottmorsedev@gmail.com",
      lisence="GPL",
      packages=['musictools'],
      install_requires=[
          'numpy',
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)