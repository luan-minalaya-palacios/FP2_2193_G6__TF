# 🏋️ Sistema de Gestión GymFit Center

Sistema desarrollado aplicando los principios de **Programación Orientada a Objetos (POO)** para optimizar la gestión administrativa de un gimnasio.

---

## 📋 Análisis del problema

### 🏢 1.1 Generalidades de la Empresa

**Nombre de la empresa:** GymFit Center  
*Empresa ficticia desarrollada con fines académicos.*

### 💼 Giro del negocio

Prestación de servicios de acondicionamiento físico, entrenamiento personalizado y asesoramiento en salud y bienestar para personas de diferentes edades.

### 🎯 Misión

Brindar servicios de entrenamiento físico de calidad, promoviendo la salud, el bienestar y el desarrollo físico de nuestros clientes mediante atención personalizada y un ambiente seguro y motivador.

### 👁️ Visión

Ser reconocidos como uno de los gimnasios líderes de la localidad, destacando por la calidad de sus servicios, la satisfacción de sus clientes y el uso de tecnología para optimizar la gestión y la toma de decisiones.

---

## 👥 Estructura Organizacional

La empresa cuenta con la siguiente estructura:

- 👨‍💼 Gerente Operativo
- 👩‍💻 Secretaria Turno Mañana
- 👩‍💻 Secretaria Turno Tarde
- 🏋️ Profesores de Gimnasio (3)
- 🧹 Personal de Limpieza (1)

---

## 🔍 1.2 Descripción del Problema

Actualmente, el gimnasio realiza la mayor parte de sus procesos administrativos de manera manual mediante hojas de cálculo, cuadernos de registro y anotaciones individuales.

Esta forma de trabajo dificulta el control de clientes, membresías, pagos y asistencias.

---

## 🧠 Marco Conceptual del Sistema

El sistema ha sido desarrollado aplicando los principios fundamentales de la **Programación Orientada a Objetos (POO)**.

### 🔒 Encapsulamiento

Los atributos de las clases se encuentran protegidos mediante atributos privados y métodos `get` y `set`.

### 🧬 Herencia

El sistema utiliza herencia para reutilizar atributos y comportamientos.

Ejemplo:

`Persona` → `Socio`

`Persona` → `Entrenador`

`Socio` → `SocioVIP`

### 🔄 Polimorfismo

Las clases de membresía utilizan métodos comunes que presentan comportamientos según el tipo de membresía.

---

## 🧩 Clases principales del sistema

- `Persona`
- `Socio`
- `SocioVIP`
- `Entrenador`
- `Membresia`
- `MembresiaBasica`
- `MembresiaTrimestral`
- `MembresiaAnual`
- `Pago`
- `RegistroAsistencia`
- `GymManager`

---

## ⚙️ Funcionalidades del Sistema

### 👥 Gestión de Clientes

- Registrar clientes.
- Modificar información.
- Consultar historial de membresías.
- Buscar clientes.
- Identificar clientes morosos.

### 💳 Gestión de Membresías

- Consultar membresías vigentes.
- Generar alertas de vencimiento.
- Renovar membresías.

### 💰 Gestión de Pagos

- Registrar pagos.
- Generar comprobantes.
- Consultar historial de pagos.

### 📅 Control de Asistencia

- Registrar asistencia.
- Consultar asistencias diarias.
- Analizar frecuencia de asistencia.
- Identificar clientes inactivos.

### 📊 Reportes e Indicadores

- Clientes activos e inactivos.
- Ingresos mensuales.
- Renovaciones.
- Vencimientos próximos.
- Tendencia de crecimiento.
- Ranking de planes.

---

## 💻 Tecnologías utilizadas

- 🐍 Python
- 🧠 Programación Orientada a Objetos
- 🌿 Git
- 🐙 GitHub

---

## 👨‍💻 Equipo de Desarrollo

| Integrante | Rol |
|---|---|
| Luan | Estructura POO y membresías |
| Karen | Gestión de clientes y herencia |
| Miguel | Pagos y asistencia |
| Brigham | Control, reportes e interfaz |

---

## 🎓 Proyecto Académico

**Curso:** Fundamentos de Programación 2  
**Proyecto:** Sistema de Gestión GymFit Center
