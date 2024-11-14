from setuptools import setup, find_packages

setup(
    name='MyCase-Ledes-Fixer',
    version='1.0.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A tool to transform LEDES files',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/your_username/your_repository',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'numpy',
        'ttkbootstrap',
        'tkinterdnd2',
        # Add other dependencies
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
) 