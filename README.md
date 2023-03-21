# cli

Cli for managing server

```bash
domain-manager [command] subdomain [...flags]
```

## Содержание

1. [**Доступные команды**](#доступные-команды)
2. [**Глобальные флаги**](#глобальные-флаги)
3. [**Описание команд**](#описание-команд)
4. [**Разработка**](#разработка)

## Доступные команды

- [**new** ](#new)- создает нужные конфигурации, сертификаты и директории для нового поддомена
- [**remove** ](#remove)- удаляет конфигурации, сертификаты и директории для поддомена
- [**list** ](#list)- выводит список всех активных поддоменов
- [**activate** ](#activate)- активирует поддомен
- [**deactivate** ](#deactivate)- деактивирует поддомен
- [**generate-cert** ](#generate-cert) - генерирует новый сертификат и приватный ключ для поддомена
- [**regenerate** ](#regenerate)- регенерирует нужные конфигурации, сертификаты и директории для поддомена

## Глобальные флаги

1. -d/--domain [_**Optional**_] - Родительский домен. По умолчанию домен - ktep-inside.local

## Описание команд

### new

Создает конфигурации для глобального nginx'а, генерирует SSL сертификаты, которые подключаются в конфигурацию nginx'а и создает директорию для логов и директорию в документах для исходников проекта.

По удачному завершению выводит полный адрес домена, пути до файлов/директорий и текущее состояние(активный или нет).

#### Флаги:

1. --no-source-dir[_**Optional**_] - Отменяет генерацию директории для исходного кода
2. --activate[_**Optional**_] - Активирует поддомен, после его создания

### remove

Удаляет конфигурации для глобального nginx'а, SSL сертификаты и директории.

По удачному завершению, выводит сообщение, что удалено успешно.

### list

Выводит список доменных имен на сервере.

Формат вывода:
| N | subdomain | domain | status | createdAt |
|---|-----------|--------|--------|-----------|
| 0 | test | ktep-inside.local | activated |2023-03-15 |

#### Флаги

1. --activated[_**Optional**_] - Выводит список активных доменных имен
2. --deactivated[_**Optional**_] - Выводит список отключенных доменных имен
3. --parent[_**Optional**_] - Выводит список всех родительских доменов
4. --name-only[_**Optional**_] - Выводит только полные доменные имена

### activate

Активирует доменное имя, если оно активировано, то ничего не делает

По удачному завершению, выводит сообщение, что активировано успешно.

#### Флаги:

1. --all[_**Optional**_] - Применяется на все поддомены в текущем домене.

### deactivate

Деактивирует доменное имя, если оно активировано, то ничего не делает

По удачному завершению, выводит сообщение, что деактивировано успешно.

#### Флаги:

1. --all[_**Optional**_] - Применяется на все поддомены в текущем домене.

### generate-cert

Заново генерирует сертификаты для поддомена.

По удачному завершению, выводит путь до сертификата.

### regenerate

Заново генерирует все сертификаты, конфигурации и директории.

По удачному завершению, выводит пути для каждого доменного имени.

#### Флаги

1. --activated[_**Optional**_] - Генерирует только для текущих активных
2. --deactivated[_**Optional**_] - Генерирует только для текущих неактивных
3. --name-only[_**Optional**_] - Выводит только полные доменные имена

## Разработка

1. Склонировать репозиторий
2. Внести изменения в проект
3. Открыть ПР в develop ветку