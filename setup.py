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
    entry_points={
        'console_scripts': ['asp2cnl = asp2cnl.asp2cnl:run_asp2cnl',
                            'asp2nl = asp2nl.asp2nl:run_asp2nl',
                            'cnl2nl = cnl2nl.cnl2nl:run_cnl2nl'],
    },
    install_requires=['lark', 'inflect', 'multipledispatch', 'cnl2asp'],
    python_requires=">=3.10"
)