import sys
from logging.config import fileConfig
from alembic import context

sys.path.append("..")  # при необходимости укажите другой путь к корню проекта
from database import engine, Base  # <- замените на модуль, где объявлены engine и Base

config = context.config
fname = config.config_file_name
fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline():
    url = str(engine.url)
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
