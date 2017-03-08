

from setuptools import setup, find_packages
# python setup.py bdist_wheel upload
setup(
    name='py_snippets',
    version='0.1.0',
    keywords=('daily practice python code snippets'),
    description='daily practice python code snippets for reusing.',
    license='MIT License',
    install_requires=[],
    py_modules=['py_snippets'],
    author='ClericPy',
    author_email='clericpy@gmail.com',
    url='https://github.com/ClericPy/python-snippet',
    packages=find_packages(),
    platforms='any',
    classifiers=[  
        "Programming Language :: Python :: 3"
    ],
)
