# Catalogs microservices
Este microservicio contiene los distintos catalogos que se utilizan en la aplicacion de [sonar32].

## Catalogos
---
- Usuarios
- Empresas
- Autenticacion
- Provedores

## Instalar dependencias
```bash
pip install -r requirements.txt
# Levantar servidor
cp .env.example .env
# Agregar las colecciones (catalogos)
# al .env
python main.py
```

[sonar32]: https://sonar32.com.mx