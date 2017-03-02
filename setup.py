from setuptools import setup, find_packages


setup(
    name = 'infosystem',
    version = '0.1.12',
    summary = 'Infosystem Framework',
    url = 'https://github.com/samueldmq/infosystem',
    author = 'Samuel de Medeiros Queiroz',
    author_email = 'samueldmq@gmail.com',
    license = 'Apache-2',
    packages = find_packages(exclude=["tests"])
    )
