import os
import os.path as op
import setuptools

requires = [
    "flake8 > 3.0.0",
    "pycodestyle",
]

with open(op.join('README.rst'), 'r') as fid:
    lines = fid.readlines()
    description = lines[-1]
print(os.listdir('.'))
with open(op.join('flake8_array_spacing', '__init__.py'), 'r') as fid:
    for line in fid:
        if line.startswith('__version__ ='):
            version = line.split('=')[1].strip().replace('\'', '')
            break
    else:
        raise RuntimeError('Could not determine version')

if __name__ == "__main__":
    if op.exists('MANIFEST'):
        os.remove('MANIFEST')

    setuptools.setup(
        name="flake8_array_spacing",
        license="BSD (3-clause)",
        version=version,
        description=description,
        author="Me",
        author_email="larson.eric.d@gmail.com",
        url="https://github.com/larsoner/flake8-array-spacing",
        python_requires=">=3.6",
        packages=[
            "flake8_array_spacing",
        ],
        install_requires=requires,
        entry_points={
            'flake8.extension': [
                'A2 = flake8_array_spacing:ArraySpacing',
            ],
        },
        classifiers=[
            "Framework :: Flake8",
            "Environment :: Console",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: BSD License",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Topic :: Software Development :: Quality Assurance",
        ],
    )
