import streamlit as st
from collections import defaultdict
from datetime import datetime

class GeneradorLinealCongruente:
    def __init__(self, semilla, a=1597, c=51749, m=244944):
        self.x = semilla
        self.a = a
        self.c = c
        self.m = m

    def siguiente(self) -> int:
        self.x = (self.a * self.x + self.c) % self.m
        return self.x % 37

class AnalizadorRuleta:
    def __init__(self):
        self.orden_ruleta = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36,
                             11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9,
                             22, 18, 29, 7, 28, 12, 35, 3, 26]
        self.glc = GeneradorLinealCongruente(datetime.now().microsecond)

    def analizar(self, numeros, umbral_caliente=3):
        frecuencias = defaultdict(int)
        for num in numeros:
            frecuencias[num] += 1

        calientes = [num for num, freq in frecuencias.items() if freq >= umbral_caliente]
        frios = [num for num in range(37) if frecuencias[num] < 2]

        return {
            "calientes": sorted(calientes),
            "frios": sorted(frios),
            "prediccion": self.glc.siguiente()
        }

# Streamlit UI
st.title("Analizador de Ruleta")

entrada = st.text_input("Ingrese los últimos números separados por comas (ej: 5,12,20,36):")

if entrada:
    try:
        numeros = [int(n.strip()) for n in entrada.split(",") if 0 <= int(n.strip()) <= 36]
        if len(numeros) == 0:
            st.warning("Debe ingresar al menos un número válido.")
        else:
            analizador = AnalizadorRuleta()
            resultado = analizador.analizar(numeros)

            st.subheader("Resultados:")
            st.write(f"Últimos {len(numeros)} números: {numeros}")
            st.write(f"Números calientes: {resultado['calientes']}")
            st.write(f"Números fríos: {resultado['frios']}")
            st.write(f"Predicción del siguiente número: {resultado['prediccion']}")
    except ValueError:
        st.error("Por favor ingrese números válidos entre 0 y 36.")
