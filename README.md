# Static Site Generator
This is a static site generator which can be used to construct full static html sites from markdown documents and html templates.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for testing purposes.

### Prerequisites

This project only requires that an up-to-date version of python3 is installed.
- [Download Python | Python.org](https://www.python.org/downloads/)

### Installing

1. Clone the repository to your local machine and enter into it.
```
git clone https://github.com/ae99/StaticSiteGenerator.git
cd StaticSiteGenerator
```

2. Run the setup script to create a new project.
```
python3 setup.py
```

This will generate all necessary folders to construct your static site.

### Developing with this Static Site Generator

Place templates in the `templates` and your markdown documents into the `documents` folder.

See an example site in the `example` folder for usage of the templating language and on how to give documents metadata.

### Generating the site
Simply run
```
python3 generate.py
```
Your static site will be generated and can be found in the `dist` folder.

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
