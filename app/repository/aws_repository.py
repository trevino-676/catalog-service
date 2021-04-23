"""
author: Luis Manuel Torres Trevino
date: 21/04/2021
"""
import boto3
from botocore.exceptions import ClientError


class AWSRepository:
    def __init__(self):
        self.s3_client = boto3.client("s3")

    def upload_file(self, file, bucket, **kwargs):
        """Guarda un archivo en el bucket del servicio de AWS S3

        :param file: El archivo que se va a guardar.
        :param bucket: Bucket donde se va a guardar el archivo.
        :param object_name: S3 object_name. Si no se especifica
            entonces el nombre del archivo es el se usa.
        :return: True si el archivo se guardo correctamente, False
            si se encotro algun error o no se guardo de forma correcta
        """
        if "rfc" in kwargs:
            rfc = kwargs["rfc"]

        object_name = f"{rfc}/{file.filename}"
        try:
            response = self.s3_client.upload_fileobj(file, bucket, object_name,
                                                     ExtraArgs={"ACL": "public-read",
                                                                "ContentType":
                                                                    file.content_type})
        except ClientError as e:
            print(e)
            return False
        return True

    def create_presigned_url(self, bucket, object_name, expiration=3600):
        """crea un url de descarga del archivo que se pasa como
            parametro

        :param bucket: Bucket donde esta guardado el archivo.
        :param object_name: Nombre del archivo.
        :param expiration: Tiempo en milisegundo que tiene el enlace
            para ser utilizado.
        """
        params = {"Bucket": bucket, "Key": object_name}
        try:
            response = self.s3_client.generate_presigned_url("get_object", Params=params,
                                                             ExpiresIn=expiration)
        except ClientError as e:
            print(e)
            return None
        return response
