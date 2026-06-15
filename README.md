 Balance Diario

Aplicación de escritorio para llevar el control de tus ingresos y gastos diarios. Hecha en Python con interfaz gráfica (Tkinter).

## Características

- Añadir ingresos y gastos con descripción, importe y fecha
- Tabla de movimientos con colores (verde = ingreso, rojo = gasto)
- Filtro por mes (formato MM/AAAA)
- Eliminar movimientos
- Resumen automático: ingresos totales, gastos totales y balance
- Los datos se guardan localmente en `mis_finanzas.json`

## Requisitos

- Python 3.10 o superior

## Instalación y uso

```bash
git clone https://github.com/Julio5-1-1997/Proyecto-BalanceDiario.git
cd Proyecto-BalanceDiario
python balanceDiario.py
```

## Generar ejecutable (.exe)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed balanceDiario.py
```

El ejecutable se generará en la carpeta `dist/`.

## Estructura del proyecto

```
BalanceDiario/
├── balanceDiario.py     # Código de la aplicación
├── mis_finanzas.json     # Datos guardados (se genera automáticamente)
├── .gitignore
└── README.md
```

## Próximas mejoras

- [ ] Categorías de gastos (comida, ocio, transporte...)
- [ ] Gráficas de gastos por categoría
- [ ] Exportar datos a Excel/CSV

## Licencia

Proyecto personal de uso libre.
