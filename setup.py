import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="daily-report-package-HeechanKim",
    version="0.0.1",
    author="Heechan Kim",
    author_email="chan-@kakao.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/heechankim/daily-report-telegram-notion",
    project_urls={
        "Bug Tracker": "https://github.com/heechankim/daily-report-telegram-notion/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)