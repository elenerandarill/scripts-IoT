from setuptools import setup, find_packages
setup(
    name='sql',
    sdk_version='1.0.5',
    version='0.0.1',
    author='whb',
    author_email='whb@ursalink.com',
    description='',
    license='PRIVATE',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    zip_safe=False,
    install_requires=[
    ],
    entry_points="""
        [console_scripts]
        sql = Application:main
        """
)