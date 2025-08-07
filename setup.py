"""
AI Transformation Playbook Setup
Enterprise AI implementation guide and change management framework
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ai-transformation-playbook",
    version="1.0.0",
    author="AI Transformation Team",
    author_email="info@ai-transformation.com",
    description="Complete enterprise AI implementation guide and change management framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ai-transformation/playbook",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology", 
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Office/Business :: Scheduling",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
            "pre-commit>=2.17.0",
        ],
        "web": [
            "streamlit>=1.10.0",
            "dash>=2.0.0",
            "fastapi>=0.75.0",
            "uvicorn>=0.17.0",
        ],
        "reporting": [
            "python-pptx>=0.6.21",
            "reportlab>=3.6.0",
            "openpyxl>=3.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "ai-transform=transformation_orchestrator:main",
            "ai-assess=strategic_foundation.ai_readiness_assessor:main",
            "ai-business-case=strategic_foundation.business_case_generator:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.yaml", "*.yml", "*.json", "*.txt"],
    },
    project_urls={
        "Bug Reports": "https://github.com/ai-transformation/playbook/issues",
        "Source": "https://github.com/ai-transformation/playbook",
        "Documentation": "https://ai-transformation.readthedocs.io/",
    },
)