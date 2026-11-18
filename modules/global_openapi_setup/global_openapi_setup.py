from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.routing import iter_route_contexts

from modules.session.unauthorized_error import unauthorized_error
from modules.global_exception_handlers.request_validation_error_handler import create_request_validation_api_error_case
from modules.session.app.provider.provide_app_session import provide_app_session


def global_openapi_setup(app: FastAPI):
    # Если схема уже сгенерирована, возвращаем её (кэширование FastAPI)
    if app.openapi_schema:
        return app.openapi_schema

    # Генерируем стандартную схему
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        openapi_version=app.openapi_version,
        description=app.description,
        routes=app.routes,
    )


    for path in openapi_schema['paths'].values():
        for method in path.values():
            responses = method.get('responses', { })

            # Заменяем 422 Validation Error на 400 Bad Request во всех роутах схемы
            if '422' in responses:
                http422 = responses['422']
                if http422['description'] == 'Validation Error':
                    responses.pop('422')
                    validation_error_case = create_request_validation_api_error_case(
                        [
                            {
                                'loc': [
                                    'string',
                                    0
                                ],
                                'msg': 'string',
                                'type': 'string',
                                'input': 'string',
                                'ctx': {}
                            }
                        ]
                    )
                    validation_error_case.add_example_to_openapi_responses(responses)



    # Проходимся по всем роутам приложения
    for route_context in iter_route_contexts(app.routes):
        route = route_context.route  # Получаем сам объект APIRoute

        if hasattr(route, 'dependant') and route.dependant:

            # Собираем зависимости
            dependencies = [d.call for d in route.dependant.dependencies if d.call]

            if hasattr(route, 'dependencies'):
                dependencies.extend([d.dependency for d in route.dependencies if d.dependency])

            # Проверяем, привязана ли функция авторизации provide_app_session к эндпоинту
            if provide_app_session in dependencies or provide_app_session == route.dependant.call:

                # Инициализируем словарь ответов для методов (GET, POST и т.д.), если его нет
                for method in route.methods:
                    method_lower = method.lower()
                    path_format = route_context.path_format

                    # Проверяем, существует ли путь в схеме
                    if path_format in openapi_schema['paths']:
                        path_node = openapi_schema['paths'][path_format]

                        if method_lower in path_node:
                            responses = path_node[method_lower].setdefault('responses', {})

                            # Если 401 статус еще не задокументирован для этого роута вручную, добавляем его
                            if '401' not in responses:
                                unauthorized_error.add_example_to_openapi_responses(responses)


    app.openapi_schema = openapi_schema
    return app.openapi_schema


def init_openapi(app: FastAPI):
    app.openapi = lambda: global_openapi_setup(app)
