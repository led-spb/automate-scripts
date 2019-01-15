import setuptools


setuptools.setup(
    name="automate-scripts",
    version="0.1.0",
    author="Alexey Ponimash",
    author_email="alexey.ponimash@gmail.com",
    scripts=[
        'bin/check-mounts',
        'bin/counters.sh',
        'bin/fail-stat.sh',
        'bin/lan-devices',
        'bin/weather.sh',
        'bin/wireless-stat'
    ]
)
