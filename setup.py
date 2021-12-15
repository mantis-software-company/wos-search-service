import setuptools

setuptools.setup(
    name="wos-search-service",
    version="1.0.1",
    author="Furkan Kalkan",
    author_email="furkankalkan@mantis.com.tr",
    description="Web of Science Search Service",
    url="https://github.com/mantis-software-company/wos-search-service",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    platforms="all",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Internet",
        "Topic :: Software Development",
        "Topic :: Utilities",
        "Intended Audience :: Developers",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Operating System :: Microsoft",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8"
    ],
    install_requires=['Flask~=2.0.2', 'flask-smorest~=0.35.0', 'marshmallow~=3.14.0', 'pyctuator~=0.16.0',
                      'wos~=0.2.5', 'lxml~=4.6.4'],
    python_requires=">3.8.*, <4",
20

    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"}
)
