from setuptools import setup, find_packages

install_requirements=[
    'device-detector',
    'geoip2',
    'requests',
    'reverse_geocoder',
    'scielo_log_validator',
    'wget',
]

setup(
    name='scielo-usage-counter',
    version='1.2.2',
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
        dl-geomap=scielo_usage_counter.proc.download_geomap:main
        dl-robots=scielo_usage_counter.proc.download_robots:main
        parse-log=scielo_usage_counter.proc.parse_log:main
    """
)
