"""
author: Luis Manuel Torres Trevino
date: 22/04/2021
"""
from app.repository import AWSRepository


class UploadFilesService:

    def __init__(self, repository: AWSRepository):
        self.repo = repository

    def upload_file(self, file, bucket, object_name=None, **kwargs) -> bool:
        """Sube el documento al bucket indicado en el parametro en
        aws.

        :param file: Archivo que se va a cargar.
        :param bucket: Nombre del bucket donde se va a guardar.
        :param object_name: Nombre del archivo con el que se va
            a guardar.
        :return: True si no hubo ningun problema al subir el archivo.
            False si hubo un problema.
        """
        rfc = kwargs["rfc"] if "rfc" in kwargs else None
        if rfc is not None:
            return self.repo.upload_file(file, bucket, rfc=rfc)
        return self.repo.upload_file(file, bucket)

    def get_url(self, object_name, bucket, expiration=3600):
        """obtiene una url del archivo que se esta consultando

        :param object_name: Nombre del archivo.
        :param bucket: Nombre del bucket donde se encuentra el archivo
        :param expiration: Tiempo de expiracion del link, por default
            3600 ms
        :return: url del archivo
        """
        return self.repo.create_presigned_url(bucket, object_name, expiration)