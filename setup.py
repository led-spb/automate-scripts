import setuptools
import automate_scripts as module

setuptools.setup(
    name=module.name,
    version=module.version,
    packages=setuptools.find_packages(exclude=["tests"]),
    install_requires=[
        'ipinfo', 'ipaddress', 'six'
    ],
    author="Alexey Ponimash",
    author_email="alexey.ponimash@gmail.com",
    scripts=[
        'bin/check-mounts',
        'bin/counters.sh',
        'bin/fail-stat.sh',
        'bin/lan-devices',
        'bin/weather.sh',
        'bin/wireless-stat',
        'bin/swaptop',
        'bin/fail2ban-mqtt.sh'
    ],
    entry_points={
        'console_scripts': [
            'ip-stat = automate_scripts.ip_stat:main'
        ]
    }
)
