# App de Automatización de Comparación de Seguros para Corredores de Autos Livianos

Esta aplicación automatiza el proceso de comparación de seguros para corredores de autos livianos, facilitando la obtención de cotizaciones de diversas empresas de seguros de manera eficiente.

## Configuración inicial

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/mauriciocruzriveros/Comparador_seguro_autoliviano.git
   ```

2. **Configurar credenciales de empresas de seguros:**
   - Añadir usuarios y contraseñas de las empresas de seguros deseadas en el archivo `credenciales.json`.

## Uso

1. **Ejecutar `ExtraerDatos.py`:**
   - Ingresar los datos del auto a cotizar cuando se solicite.

2. **Ejecutar `Launcher_paralelo.py` o `Launcher.py`:**
   - Si cuentas con un PC potente que soporte la ejecución en paralelo, usar `Launcher_paralelo.py`.
   - Si tienes recursos limitados, utilizar `Launcher.py` para ejecutar en cola.

## Requisitos del sistema

- Python 3.x
- Bibliotecas adicionales: (        )

## Contribuciones

¡Las contribuciones son bienvenidas! Si deseas contribuir al proyecto, sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/feature-name`).
3. Realiza tus cambios y commitea (`git commit -am 'Añadir nueva característica'`).
4. Haz push a la rama (`git push origin feature/feature-name`).
5. Crea un nuevo Pull Request.

## Contacto

Para cualquier duda o sugerencia, puedes contactarme a través de mauriciocruzriveros@gmail.com
