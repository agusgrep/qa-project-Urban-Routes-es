# Urban Routes QA Automation Project

## Descripción del Proyecto
Este proyecto contiene una suite de pruebas automatizadas de extremo a extremo (E2E) para la aplicación web **Urban Routes**. El objetivo principal es verificar los flujos funcionales del proceso de solicitud de viajes en taxi, garantizando la correcta configuración de la ruta, la selección de tarifas personalizadas, la vinculación de métodos de pago y la solicitud de requisitos adicionales para el viaje.

Las pruebas cubren los siguientes escenarios:
1. Configuración de direcciones de origen y destino.
2. Selección de la tarifa Comfort.
3. Relleno y validación del número de teléfono mediante intercepción de código SMS.
4. Vinculación de una tarjeta de crédito como método de pago.
5. Inclusión de un mensaje personalizado para el conductor.
6. Solicitud de accesorios adicionales (manta y pañuelos).
7. Incremento de artículos adicionales en el pedido (2 helados).
8. Apertura y visualización de la ventana modal de búsqueda de taxi.

---

## Tecnologías y Técnicas Utilizadas

- **Lenguaje de programación:** Python 3.x
- **Framework de pruebas:** Pytest
- **Herramienta de automatización web:** Selenium WebDriver
- **Patrón de diseño:** **Page Object Model (POM)**, separando la lógica de interacción con la interfaz (`UrbanRoutesPage`) de la lógica de aserción y validación (`TestUrbanRoutes`).
- **Manejo de sincronización:** Esperas explícitas (`WebDriverWait` y `expected_conditions`) para gestionar la asincronía y tiempos de carga de la interfaz sin pausas estáticas.
- **Intercepción de eventos de red:** Uso de Chrome DevTools Protocol (`CDP`) y logs de rendimiento del navegador para extraer dinámicamente el código de confirmación SMS sin depender de dispositivos físicos.

---

## Requisitos Previos

Antes de ejecutar las pruebas, asegúrate de tener instalado:
- **Python** (versión 3.8 o superior)
- Navegador web **Google Chrome** y su respectivo **ChromeDriver** compatible con tu versión instalada
- Gestor de paquetes **pip**

---

## Instalación y Configuración

1. Clona el repositorio en tu máquina local:
   ```bash
   git clone [https://github.com/agusgrep/qa-project-Urban-Routes-es.git](https://github.com/agusgrep/qa-project-Urban-Routes-es.git)
   cd qa-project-Urban-Routes-es