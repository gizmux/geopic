from setuptools import setup

setup(name='geopic',
      version='0.1',
      description='Simple extraction of geographic information from exif data',
      url='http://github.com/gizmux/geopic',
      author='gizmux',
      author_email='gizmux@gmail.com',
      license='MIT',
      packages=['geopic'],
      install_requires=[
          'pygeocoder',
          'exifread'
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)