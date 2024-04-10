from setuptools import setup, find_packages

setup(
    name='asp2cnl',
    version='1.0.0',
    description='A tool for converting Answer Set Programming into a Controlled Natural Language based on English',
    url='https://github.com/dodaro/asp2cnl',
    license='Apache License',
    author='Carmine Dodaro',
    author_email='carmine.dodaro@unical.it',
    maintainer='Kristian Reale',
    maintainer_email='kristian.reale@unical.it',
    package_dir={'': 'src'},
    packages=find_packages('src', exclude=['test*']),
    package_data={'': ['asp_core_2_grammar/asp_grammar.lark']},
    install_requires=['lark'],
    python_requires=">=3.10"
)