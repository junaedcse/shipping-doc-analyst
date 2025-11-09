from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="shipping-doc-analyst",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="AI-powered shipping document analysis system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/shipping-doc-analyst",
    packages=find_packages(exclude=["tests", "tests.*", "docs", "scripts"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "shipping-analyst=shipping_doc_analyst.cli.main:cli",
        ],
    },
)
