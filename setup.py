#!/usr/bin/env python

from distutils.core import setup

setup(name='cloud-calculator',
      version='0.1.0',
      description='Cost calculator for public cloud services.',
      author='Ilja Livenson/KBFI',
      author_email='ilja.livenson@gmail.com',
      url='https://github.com/HEP-KBFI/ccc',
      license='BSD (3-clause)',      
      package_dir = {'': 'src'},
      packages=['sitio', 'sitio.adapters', 'sitio.analyser', 'sitio.common', 'sitio.model'],
      package_data = {'sitio.analyser': ['pricelist/*.csv']},
                                    
      requires=['PuLP (==1.4.7)'],
     )