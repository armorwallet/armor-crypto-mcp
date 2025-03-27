from setuptools import setup, find_packages

# Read the long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="armor-crypto-mcp",
    version="0.1.0",
    description=(
        "MCP to interface with multiple blockchains, staking, DeFi, swap, bridging, wallet management, "
        "and to develop crypto trading strategies through tools like dynamic DCA"
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.11",
    install_requires=[
        "mcp>=1.1.0",
        "python-dotenv>=1.0.0",
        "requests>=2.31.0",
        "uvicorn>=0.32.1",
        "httpx",
    ],
    author="Armor Wallet",
    author_email="info@armorwallet.ai",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "armor-crypto-mcp=armor_mcp:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",  # Adjust if using a different license
        "Operating System :: OS Independent",
    ],
)
