Что такое тутор?
---

> Tutor is the official Docker-based Open edX distribution, both for production and local development. The goal of Tutor
> is to make it easy to deploy, customise, upgrade and scale Open edX. Tutor is reliable, fast, extensible, and it is
> already used to deploy hundreds of Open edX platforms around the world.

Tutor не является обязательным инструментом для работы с Open edX,
но он значительно упрощает первые запуски и позволяет "пощупать" платформу.
Кроме того, Tutor позволяет расширять функционал Open edX без изменения ее исходного кода, чем мы и займемся в этой
статье.

## Как выглядит плагин для Open edX?

Плагин для Open edX представляет собой обычное Django-приложение с небольшими
доработками. [Официальный гайд Open edX](https://edx.readthedocs.io/projects/edx-django-utils/en/latest/plugins/how_tos/how_to_create_a_plugin_app.html)
рекомендует использовать [edx-cookiecutter](https://pypi.org/project/cookiecutter-openedx-plugin/) для создания
плагинов, однако это не обязательно — аналогичный результат можно достичь с помощью любой IDE, например PyCharm, которая
умеет создавать скелет для Django-приложения.

В общем случае, плагин для Open edX мало чем отличается от стандартного Django-приложения.
Главное отличие это plugin_settings = {} в конфигурационном классе и дополнительные настройки setup.py.

Пример создания плагина для Open edX, который добавит api
---

Важно отметить, что мы создаем плагин именно для платформы Open edX, а не для Tutor.
Плагины Tutor предназначены для вмешательства в процесс сборки и модификации некоторых настроек платформы edx без
изменения ее исходного кода.
Подробнее об этом можно узнать в официальной документации по созданию плагина
для [Tutor](https://docs.tutor.edly.io/tutorials/plugin.html#plugin-development-tutorial).

Итак, что нам нужно для создания плагина?

1. [ ] Установить Tutor и все необходимые зависимости (например, Docker и Docker Compose*).
2. [ ] Создать скелет Django-приложения.
3. [ ] Добавить наш плагин через изменение config.yml в Tutor.

* Важно: последние версии Tutor используют именно ```docker compose```, а не ```docker-compose```. Если будет
  установлена только docker-compose, то ничего не заработает.

Установка тутора
---

1. Для начала создадим виртуальное пространство для избежания проблем при работе тутора и установим его

```bash
python -m venv venv
source venv/bin/activate
pip install "tutor[full]"
```

2. Поздравляю, теперь мы можем вызывать команды тутора. Для ознакомления с ними достаточно будет вызвать

```bash
tutor -h
```

3. Для запуска в минимальном окружении тутора выполним команду

```bash
tutor local launch
```

Далее платформа в интерактивном режиме предложит вам настроить некоторые параметры системы, а именно спросит не является
ли её текущая конфигурация 'продакшеном' и прочие мелочи

```text
$ tutor local launch
==================================================
        Interactive platform configuration
==================================================
Are you configuring a production platform? Type 'n' if you are just testing Tutor on your local computer [y/N] 
As you are not running this platform in production, we automatically set the following configuration values:
    LMS_HOST = local.edly.io
    CMS_HOST = studio.local.edly.io
    ENABLE_HTTPS = False
Your platform name/title [edx] 
Your public contact email address [contact@local.edly.io] 
The default language code for the platform [en] 
Configuration saved to /home/jaba/.local/share/tutor/config.yml
Environment generated in /home/jaba/.local/share/tutor/env
======================================
        Building Docker images
======================================
No image to build
==============================================
        Stopping any existing platform
==============================================
docker compose -f /home/jaba/.local/share/tutor/env/local/docker-compose.yml -f /home/jaba/.local/share/tutor/env/local/docker-compose.prod.yml --project-name tutor_local stop
[+] Running 12/0
 ⠿ Container tutor_local-cms-worker-1     Stopped                                                                                                                                        0.0s
 ⠿ Container tutor_local-mfe-1            Stopped                                                                                                                                        0.0s
 ⠿ Container tutor_local-lms-worker-1     Stopped                                                                                                                                        0.0s
 ⠿ Container tutor_local-caddy-1          Stopped                                                                                                                                        0.0s
 ⠿ Container tutor_local-cms-1            Stopped                                                                                                                                        0.0s
 ⠿ Container tutor_local-lms-1            Stopped                                                                                                                                        0.0s
 ⠿ Container tutor_local-elasticsearch-1  Stopped                                                                                                                                        0.0s
 ⠿ Container tutor_local-mongodb-1        Stopped                                                                                                                                        0.0s
 ⠿ Container tutor_local-smtp-1           Stopped                                                                                                                                        0.0s
 ⠿ Container tutor_local-mysql-1          Stopped                                                                                                                                        0.0s
 ⠿ Container tutor_local-redis-1          Stopped                                                                                                                                        0.0s
 ⠿ Container tutor_local-permissions-1    Stopped                                                                                                                                        0.0s
======================================================
        Starting the platform in detached mode
======================================================
docker compose -f /home/jaba/.local/share/tutor/env/local/docker-compose.yml -f /home/jaba/.local/share/tutor/env/dev/docker-compose.yml --project-name tutor_dev stop
docker compose -f /home/jaba/.local/share/tutor/env/local/docker-compose.yml -f /home/jaba/.local/share/tutor/env/local/docker-compose.prod.yml --project-name tutor_local up --remove-orphans -d
```

Несложно заметить, что при выполнении тех или иных команд tutor вызывает команды docker compose. Настройки
docker compose можно найти при помощи команды

```bash
cd $(tutor config printroot)/env/local  
```

Создаем приложение-плагин для edx
---
И так мы запустили tutor и остались в здравии. Перейдем к самому интересному, а именно созданию плагина. Для этого можно
воспользоваться различными инструментами, например, IDE Pycharm, которая создаст нам скелет для django приложения. 

Устанавливаем все необходимые зависимости

```bash
pip install django_rest_framework setuptools
```

Отлично, теперь перейдем к написанию модуля views, в нем создадим класс UserManager, наследника от APIView

```python
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response


class UserManager(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        username = request.user.username if request.user.is_authenticated else 'пользователь не авторизован'
        return Response({'username': username, })


```

Обновим наш urls.py, обратите внимание, что путь был указан при помощи метода ```re_path()```

```python
from django.contrib import admin
from django.urls import path, re_path
from .views import UserManager

urlpatterns = [
    re_path(r'^user', UserManager.as_view(), name='user'),
]

```

Также не забудем добавить в ```INSTALLED_APPS``` rest_framework

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
]
```

Для проверки, что мы еще ничего не сломали, запускаем

```bash
python manage.py runserver 
```

и проверяем, что выдает

```bash
$ curl http://127.0.0.1:8000/user
{"username":"пользователь не авторизован"}
```

Отлично, у нас получилось обычное django приложение, но что там на счёт edx...?

Главное отличие начинается с класса конфига, а именно с дополнения его plugin_app. И так создаем ```apps.py``` и в нем
наш класс со следующей конфигурацией:

```python
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

```

Имена можно вводить в ручную, а можно установить ```edx_django_utils``` через pip и импортировать их в виде констант(
пример из документации edx).

```python
from django.apps import AppConfig
from edx_django_utils.plugins.constants import (
    PluginURLs, PluginSettings, PluginContexts
)


class MyAppConfig(AppConfig):
    name = 'full_python_path.my_app'

    # Class attribute that configures and enables this app as a Plugin App.
    plugin_app = {

        # Configuration setting for Plugin URLs for this app.
        PluginURLs.CONFIG: {

            # Configure the Plugin URLs for each project type, as needed. The full list of project types for edx-platform is
            # here:
            # https://github.com/openedx/edx-platform/blob/2dc79bcab42dafed2c122eb808cdd5604327c890/openedx/core/djangoapps/plugins/constants.py#L14 .
            # Other IDAs may use different values.
            'lms.djangoapp': {

                # The namespace to provide to django's urls.include.
                PluginURLs.NAMESPACE: 'my_app',

                # The application namespace to provide to django's urls.include.
                # Optional; Defaults to None.
                PluginURLs.APP_NAME: 'my_app',

                # The regex to provide to django's urls.url.
                # Optional; Defaults to r''.
                PluginURLs.REGEX: r'^api/my_app/',

                # The python path (relative to this app) to the URLs module to be plugged into the project.
                # Optional; Defaults to 'urls'.
                PluginURLs.RELATIVE_PATH: 'api.urls',
            }
        },

        # Configuration setting for Plugin Settings for this app.
        PluginSettings.CONFIG: {

            # Configure the Plugin Settings for each Project Type, as needed. The full list of setting types for edx-platform is
            # here:
            # https://github.com/openedx/edx-platform/blob/2dc79bcab42dafed2c122eb808cdd5604327c890/openedx/core/djangoapps/plugins/constants.py#L25 .
            # Other IDAs may use different values.
            'lms.djangoapp': {

                # Configure each settings, as needed.
                'production': {

                    # The python path (relative to this app) to the settings module for the relevant Project Type and Settings Type.
                    # Optional; Defaults to 'settings'.
                    PluginSettings.RELATIVE_PATH: 'settings.production',
                },
                'common': {
                    PluginSettings.RELATIVE_PATH: 'settings.common',
                },
            }
        },

        # Configuration setting for Plugin Signals for this app.
        PluginSignals.CONFIG: {

            # Configure the Plugin Signals for each Project Type, as needed.
            'lms.djangoapp': {

                # The python path (relative to this app) to the Signals module containing this app's Signal receivers.
                # Optional; Defaults to 'signals'.
                PluginSignals.RELATIVE_PATH: 'my_signals',

                # List of all plugin Signal receivers for this app and project type.
                PluginSignals.RECEIVERS: [{

                    # The name of the app's signal receiver function.
                    PluginSignals.RECEIVER_FUNC_NAME: 'on_signal_x',

                    # The full path to the module where the signal is defined.
                    PluginSignals.SIGNAL_PATH: 'full_path_to_signal_x_module.SignalX',

                    # The value for dispatch_uid to pass to Signal.connect to prevent duplicate signals.
                    # Optional; Defaults to full path to the signal's receiver function.
                    PluginSignals.DISPATCH_UID: 'my_app.my_signals.on_signal_x',

                    # The full path to a sender (if connecting to a specific sender) to be passed to Signal.connect.
                    # Optional; Defaults to None.
                    PluginSignals.SENDER_PATH: 'full_path_to_sender_app.ModelZ',
                }],
            }
        },

        # Configuration setting for Plugin Contexts for this app.
        PluginContexts.CONFIG: {

            # Configure the Plugin Signals for each Project Type, as needed.
            'lms.djangoapp': {

                # Key is the view that the app wishes to add context to and the value
                # is the function within the app that will return additional context
                # when called with the original context
                'course_dashboard': 'my_app.context_api.get_dashboard_context'
            }
        }
    }
```

Отлично, теперь перейдем к созданию и настройки нашего ```setup.py```

```python
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

```

Фактически эти данные подставятся в edx setup.py, а именно в его разделы с lms.djangoapp и cms.djangoapp
Важное замечание здесь следующее: в lms.djangoapps/cms.djangoapps мы указываем имя в формате name = full_pythonname:
ConfigClass и никак иначе.\
На этом создание нашего плагина заканчивается. Нам не нужно никуда его вручную добавлять через ```INSTALLED_APPS```,
т.к. здесь за нас работает IDA(Independently Deployable Application) от edx.

Добавляем плагин в tutor
---
Добавляем наш плагин в Tutor как дополнительную pip-зависимость, для этого нам необходимо изменить config.yml. Открываем
его:

```bash
$ vim $(tutor config printroot)/config.yml
```

и добавляем следующую строчку

```yml
OPENEDX_EXTRA_PIP_REQUIREMENTS:
  - git+<ссылка до нашего репозитория с плагином>
  - git+https://github.com/JABAN111/cool_plugin.git
```

Для просмотра возможных параметров или дополнения/изменения них, мы можем обратиться к исходникам tutor, а именно к
файлу [defaults.yml](https://github.com/overhangio/tutor/blob/master/tutor/templates/config/defaults.yml)

После того как мы добавили, нам необходимо сохранить новые настройки(для того, чтобы заново создались env/) и заново
сбилдить образ edx

```bash
tutor config save && tutor images build openedx && tutor local launch -I
```

Флаг I при вызове команды tutor local launch пропускает этап с интерактивным запуском

Все, теперь мы можем найти наше творение по [local.edly.io/plugin/user](local.edly.io/plugin/user)

Если хотим запустить это на версии dev, то предварительно необходимо ее сбилдить:

```bash
tutor images build openedx-dev
```

Отныне наше творение также доступно на [local.edly.io:8000/plugin/user](local.edly.io:8000/plugin/user)