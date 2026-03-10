# HormigasAIS AirCity — Guia de Demo Tecnica

Protocolo LBH v1.1 | Soberania Digital | Edge Computing
Autor: Ing. Cristhiam Leonardo Hernandez Quinonez (CLHQ)
Version: v1.2.0 | DOI: https://zenodo.org/records/17767205

---

## 1. Que es HormigasAIS AirCity?

Sistema de gestion de trafico aereo no tripulado (UTM) basado en el
protocolo soberano LBH (Lenguaje Binario HormigasAIS). Opera sin
dependencia de infraestructura cloud, sobre redes mesh locales con
comunicacion cifrada HMAC-SHA256 entre nodos fisicos.

Caso de uso principal: Aeropuerto del Pacifico, Conchagua La Union,
El Salvador - apertura 2027, inversion $1,424M.

---

## 2. Como ejecutar la demo en vivo

Requisitos: 2 Android con Termux, misma red WiFi, Python 3.x

PASO 1 - Nodo Receptor (dispositivo B):
  git clone https://github.com/HormigasAIS/HormigasAIS-AirCity.git
  cd HormigasAIS-AirCity/src
  python3 lbh_demo_red.py receptor

PASO 2 - Nodo Emisor (dispositivo A):
  cd HormigasAIS-AirCity/src
  python3 lbh_demo_red.py emisor <IP_RECEPTOR>

Resultado esperado:
  Feromona 1/5: ESTADO:OPERATIVO    -> ACEPTADO
  Feromona 2/5: PATH_CLEAR:0x10    -> ACEPTADO
  Feromona 3/5: LATIDO:0x01        -> ACEPTADO
  Feromona 4/5: MED_PRIORITY:0x77  -> ACEPTADO
  Feromona 5/5: ESTADO:SOBERANO    -> ACEPTADO
  Feromonas aceptadas: 5/5 - Interoperabilidad: CONFIRMADA

---

## 3. Que muestra cada componente?

lbh_demo_red.py        - Demo interoperabilidad TCP entre 2 nodos fisicos
lbh_node_v1_1.py       - Motor LBH con HMAC-SHA256 y anti-replay
CENTINELA_V24_PILOTO.py - Scanner BLE para consenso de colonia
nlp_edge.py            - Procesamiento comandos UTM en el borde
diccionario_LBH.json   - Mapa comandos 0x00-0xFF para gestion de drones

Comandos UTM implementados:
  0x01 PULSE_HEART    - Latido soberano activo
  0x10 PATH_CLEAR     - Espacio aereo despejado
  0x22 ALERT_WIND     - Viento excesivo, drones en tierra
  0x77 MED_PRIORITY   - Emergencia medica, prioridad absoluta
  0xFF SOVEREIGN_LOCK - Bloqueo total, intervencion manual

---

## 4. Caso de uso: Aeropuerto del Pacifico 2027

Inversion: $1,424M en corredor logistico multimodal
Apertura: segundo semestre 2027
Administrador: CEPA

HormigasAIS AirCity ofrece:
- Gestion UTM soberana sin dependencia de proveedores externos
- Protocolo LBH con estandar tecnico propio (RFC-LBH-0001 al 0005)
- Operacion en red mesh local, funciona sin internet
- Cifrado HMAC-SHA256 en cada feromona transmitida
- Escalable desde 2 nodos hasta enjambre ilimitado

Modelos de implementacion:
- Freemium:   1 nodo Android, comandos basicos
- Premium:    3 nodos, emergencias medicas, $1,200/anio
- Enterprise: nodos ilimitados, hardware dedicado, $12,000/anio

---

## 5. Links de referencia

Repositorio AirCity:    https://github.com/HormigasAIS/HormigasAIS-AirCity
Organizacion GitHub:    https://github.com/HormigasAIS
DOI Zenodo:             https://zenodo.org/records/17767205
RFC-LBH-0001 al 0005:  https://github.com/HormigasAIS/HormigasAIS-LBH-Protocol
Adaptador XOXO-LBH:    https://github.com/HormigasAIS/xoxo-lbh-adapter

---

La colonia no reside en la plataforma, reside en el protocolo.
-- Ing. Cristhiam Leonardo Hernandez Quinonez, CLHQ
