from setuptools import find_packages, setup

setup(
    name="latestnumbers",
    version="1.0.0",
    url="http://github.com/praekeltfoundation/latest-numbers",
    license="BSD",
    author="Praekelt Foundation",
    author_email="dev@praekeltfoundation.org",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django==4.1.7",
        "djangorestframework==3.14.0",
        "requests==2.28.2",
        "django-environ",
        "dj-database-url",
        "psycopg2-binary"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
