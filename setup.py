from setuptools import setup, find_packages

setup(
    name="insightlog101",
    version="0.1.6",
    author="kmukoo101",
    description="Secure, redactable, context-aware logger for security and DevOps workflows.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kmukoo101/insightlog",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    python_requires=">=3.7",
    install_requires=[
        "colorama>=0.4.6",
        "PyYAML>=6.0",
        "cryptography>=41.0.0"
    ],
    include_package_data=True,
    zip_safe=False,
)
