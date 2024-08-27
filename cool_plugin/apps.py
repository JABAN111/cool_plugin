from django.apps import AppConfig


class CoolPluginConfig(AppConfig):
    name = 'cool_plugin'

    plugin_app = {
        "url_config": {
            'lms.djangoapp': {
                "namespace": 'cool_plugin',
                "regex": '^plugin/',
                "relative_path": 'urls',
            },
        },
    }
