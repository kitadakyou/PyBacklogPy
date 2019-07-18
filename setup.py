from setuptools import setup, find_packages

setup(
    name='pybacklogpy',
    version='0.10',
    author='Hikaru ETO',
    author_email='kitadakyou@gmail.com',
    url='https://kitadakyou.github.io/PyBacklogPy/',
    description='A library for backlog api',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    license='Apache License 2.0',
    python_requires='>=3.5',
    install_requires=['requests==2.22.0'],
    packages=find_packages(),
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Natural Language :: Japanese',
    ],
)
