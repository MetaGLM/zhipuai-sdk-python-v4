from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as readme_file:
    readme = readme_file.read()

with open("requirements.txt") as requirements_file:
    requirements = requirements_file.read().splitlines()

setup(
    name="zhipuai",
    version="v2.0.1",
    description="A SDK library for accessing big model apis from ZhipuAI",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Zhipu AI",
    url="https://open.bigmodel.cn/",
    packages=find_packages(exclude=['test', 'examples']),
    include_package_data=True,
    install_requires=requirements,
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
