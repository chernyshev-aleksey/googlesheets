import os

from pydantic import BaseModel, ValidationError
from loguru import logger
from dotenv import dotenv_values


class Config(BaseModel):
	DB_LOGIN: str
	DB_PASSWORD: str
	DB_NAME: str
	GOOGLESHEETS_ID: str
	NAME_CERVICES_ACCOUNT: str
	CA_FILE: str
	DB_COL_NAME: str


logger.add(os.path.dirname(os.path.abspath(__file__)) + "/../logs/errors_{time:MM.YYYY}.log", level="ERROR")

config_dict = {
	**dotenv_values(os.path.dirname(os.path.abspath(__file__)) + "/../.env.server"),
	**dotenv_values(os.path.dirname(os.path.abspath(__file__)) + "/../.env.local"),
}

try:
	config = Config(**config_dict)
except ValidationError:
	logger.exception('Ошибка загрузки конфига')
	exit(1)
else:
	CONNECTION_STRING = f"mongodb://{config.DB_LOGIN}:{config.DB_PASSWORD}@rc1b-okazhb06hqauc9ep.mdb.yandexcloud.net:" + \
						f"27018/?replicaSet=rs01&authSource={config.DB_NAME}"
