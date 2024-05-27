from setuptools import find_packages, setup

setup(
    name='netbox-routing',
    version='0.1.2',
    description='NetBox Routing',
    long_description='Plugin for documentation of routing configuration and objects',
    url='https://github.com/dansheps/netbox-routing/',
    download_url='https://pypi.org/project/netbox-routing/',
    author='Daniel Sheppard',
    author_email='dans@dansheps.com',
    maintainer='Daniel Sheppard',
    maintainer_email='dans@dansheps.com',
    license='All rights reserved',
    platform=[],
    keywords=['netbox', 'netbox-plugin'],
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 3',
    ],
    install_requires=[
        'django-polymorphic',
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
