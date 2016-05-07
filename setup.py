from setuptools import setup, find_packages

setup(
      name='kamerie',
      version='0.1',
      url='https://github.com/kamerie/kamerie-server',
      packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
      platforms='any',
      license='Apache 2.0',
      install_requires=['pika'],
      zip_safe=False,
      classifiers=[
          'Programming Language :: Python',
          'Development Status :: 4 - Beta',
          'Natural Language :: English',
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Software Development :: Libraries :: Application Frameworks',
      ],
)
