from setuptools import setup, find_packages

install_requirements=[
    'device-detector',
    'geoip2',
    'mysqlclient',
    'requests',
    'reverse_geocoder',
    'sqlalchemy',
    'scielo_log_validator',
    'wget',
]

setup(
    name='scielo-usage-counter',
    version='0.3.5.1',
    description='The SciELO Usage Counter Tool',
    author='SciELO',
    author_email='scielo-dev@googlegroups.com',
    license='BSD',
    install_requires=install_requirements,
    url='https://github.com/scieloorg/scielo_usage_counter',
    keywords='usage access, project counter r5, sushi',
    maintainer_email='rafael.pezzuto@gmail.com',
    packages=find_packages(),
    entry_points="""
        [console_scripts]
        get_geomap=app.proc.download_geomap:main
        get_robots=app.proc.download_robots:main
        init_db=app.proc.initialize_database:main
        parse=app.proc.parse_log:main
        gen_pt=app.proc.generate_pretable:main
    """
)
