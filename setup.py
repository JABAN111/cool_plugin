from setuptools import setup, find_packages

setup(
    name='cool_plugin',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # сюда необходимо подставить только те зависимости, которых нет в самом edx -> НЕ НАДО УСТАНАВЛИВАТЬ django и прочие мелочи
    ],
    entry_points={
        "lms.djangoapp": [
            "cool_plugin = cool_plugin.apps:CoolPluginConfig",
        ],
        "cms.djangoapp": [
        ],
    }
)
