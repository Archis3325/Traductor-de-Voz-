import random
import time
import numpy as np
import scipy.io.wavfile as wav
import sounddevice as sd
import speech_recognition as sr

# 1. DICCIONARIOS DE PALABRAS Y TRADUCCIONES DIRECTAS
# Mantiene la estructura de dificultad exigida sin depender de APIs inestables
dictionary = {
    "facil": {
        "gato": {"en": "cat", "fr": "chat", "de": "katze", "it": "gatto", "pt": "gato"},
        "perro": {"en": "dog", "fr": "chien", "de": "hund", "it": "cane", "pt": "cao"},
        "manzana": {"en": "apple", "fr": "pomme", "de": "apfel", "it": "mela", "pt": "maca"},
        "cafe": {"en": "coffee", "fr": "cafe", "de": "kaffee", "it": "caffe", "pt": "cafe"},
        "agua": {"en": "water", "fr": "eau", "de": "wasser", "it": "acqua", "pt": "agua"},
        "mama": {"en": "mom", "fr": "maman", "de": "mama", "it": "mamma", "pt": "mae"},
    },
    "medio": {
        "platano": {"en": "banana", "fr": "banane", "de": "banane", "it": "banana", "pt": "banana"},
        "escuela": {"en": "school", "fr": "ecole", "de": "schule", "it": "scuola", "pt": "escola"},
        "amigo": {"en": "friend", "fr": "ami", "de": "freund", "it": "amico", "pt": "amigo"},
        "ventana": {"en": "window", "fr": "fenetre", "de": "fenster", "it": "finestra", "pt": "janela"},
        "amarillo": {"en": "yellow", "fr": "jaune", "de": "gelb", "it": "giallo", "pt": "amarelo"},
    },
    "dificil": {
        "tecnologia": {"en": "technology", "fr": "technologie", "de": "technologie", "it": "tecnologia", "pt": "tecnologia"},
        "universidad": {"en": "university", "fr": "universite", "de": "universitat", "it": "universita", "pt": "universidade"},
        "informacion": {"en": "information", "fr": "information", "de": "information", "it": "informazione", "pt": "informacao"},
        "pronunciacion": {"en": "pronunciation", "fr": "prononciation", "de": "aussprache", "it": "pronuncia", "pt": "pronuncia"},
        "imaginacion": {"en": "imagination", "fr": "imagination", "de": "fantasie", "it": "immaginazione", "pt": "imaginacao"},
        "telefono": {"en": "phone", "fr": "telephone", "de": "telefon", "it": "telefono", "pt": "telefone"},
    }
}

# Códigos de reconocimiento de voz para Google Speech Recognition
SPEECH_LANG_CODES = {
    "en": "en-US",
    "fr": "fr-FR",
    "de": "de-DE",
    "it": "it-IT",
    "pt": "pt-PT",
}

duration = 4  # Duración de grabación por palabra (segundos)
sample_rate = 44100
recognizer = sr.Recognizer()

# ---------------------------------------------------------
# INTERFAZ Y CONFIGURACIÓN (10 Pts)
# ---------------------------------------------------------
print("=" * 60)
print(
    """
   ██████╗ ██████╗ ███╗   ██╗██╗   ██╗███╗   ██╗██████╗██╗███████╗██████╗ 
   ██╔══██╗██╔══██╗████╗  ██║██║   ██║████╗  ██║██╔════╝██║██╔════╝██╔══██╗
   ██████╔╝██████╔╝██╔██╗ ██║██║   ██║██╔██╗ ██║██║     ██║█████╗  ██████╔╝
   ██╔═══╝ ██╔══██╗██║╚██╗██║██║   ██║██║╚██╗██║██║     ██║██╔══╝  ██╔══██╗
   ██║     ██║  ██║██║ ╚████║╚██████╔╝██║ ╚████║╚██████╗██║███████╗██║  ██║
"""
)
print("=" * 60)
print("   🎯 ¡Desafío de Traducción y Pronunciación! 🎯")
print("=" * 60)

# Selección de dificultad
print("\nSelecciona tu nivel de dificultad:")
print("  1. 🟢 Facil   (Palabras cortas)")
print("  2. 🟡 Medio   (Palabras compuestas)")
print("  3. 🔴 Dificil (Palabras avanzadas)")

level_choice = input("\n👉 Ingresa el número o nombre del nivel (1/2/3): ").strip().lower()

if level_choice in ["1", "facil", "fácil"]:
    level = "facil"
elif level_choice in ["2", "medio"]:
    level = "medio"
elif level_choice in ["3", "dificil", "difícil"]:
    level = "dificil"
else:
    print("⚠️ Opción inválida. Se seleccionó nivel 'Facil' por defecto.")
    level = "facil"

# Obtener las palabras en español según la dificultad elegida
spanish_words = list(dictionary[level].keys())
random.shuffle(spanish_words)

# Selección del idioma al que el usuario DEBE hablar
print("\n🌍 ¿A qué idioma deseas traducir y PRONUNCIAR las palabras?")
print("  [en] Inglés  |  [fr] Francés  |  [de] Alemán  |  [it] Italiano  |  [pt] Portugués")
target_lang = input("👉 Código de idioma (default 'en'): ").strip().lower()

if target_lang not in SPEECH_LANG_CODES:
    target_lang = "en"

rec_lang = SPEECH_LANG_CODES[target_lang]

# ---------------------------------------------------------
# SISTEMA DE PUNTOS Y LÓGICA DEL JUEGO (25 Pts + 10 Pts)
# ---------------------------------------------------------
score = 0
total_rounds = 3
current_round = 1

print(f"\n🚀 ¡El juego comienza! Tendrás {total_rounds} rondas.")
print(f"💡 Verás la palabra en Español y deberás decir su traducción en [{target_lang.upper()}].")
print("──────────────────────────────────────────────────────────")

for word_es in spanish_words[:total_rounds]:
    expected_word = dictionary[level][word_es][target_lang].lower()

    print(f"\nROUND {current_round}/{total_rounds}")
    print(f"📖 Palabra en Español: 👉  \033[1m{word_es.upper()}\033[0m  👈")

    # Cuenta regresiva
    for i in range(3, 0, -1):
        print(f"⏱️  Piénsala... grabando en {i}...", end="\r")
        time.sleep(1)

    print(f"\n🎙️  ¡DILO EN [{target_lang.upper()}] AHORA! Recording...               ")
    
    recording = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="int16",
    )
    sd.wait()
    wav.write("temp_game.wav", sample_rate, recording)

    print("⏳ Procesando tu voz...")

    with sr.AudioFile("temp_game.wav") as source:
        # Ajuste de ruido ambiental para mejorar la detección
        recognizer.adjust_for_ambient_noise(source, duration=0.3)
        audio = recognizer.record(source)

    try:
        # Detección de voz en el idioma seleccionado
        spoken_text = recognizer.recognize_google(audio, language=rec_lang).strip().lower()
        
        print(f"🎧 Escuchamos: '{spoken_text}'")
        print(f"✨ Traducción esperada: '{expected_word}'")

        # Evaluación del resultado
        if spoken_text == expected_word:
            print("✅ ¡EXCELENTE! Traducido y pronunciado perfectamente. (+10 Puntos)")
            score += 10
        elif expected_word in spoken_text or spoken_text in expected_word:
            print("🟡 ¡CASI! La palabra correcta estaba en lo que dijiste. (+5 Puntos)")
            score += 5
        else:
            print(f"❌ Incorrecto. Dijiste '{spoken_text}', pero la traducción era '{expected_word}'. (0 Puntos)")

    except sr.UnknownValueError:
        print(f"❌ No pudimos entender el audio en [{target_lang.upper()}]. Intenta hablar más claro o fuerte.")
    except sr.RequestError as e:
        print(f"⚠️ Error de conexión con Google STT: {e}")
    except Exception as e:
        print(f"⚠️ Error inesperado: {e}")

    current_round += 1
    time.sleep(1)

# ---------------------------------------------------------
# FIN DEL JUEGO Y RANGOS (10 Pts + 15 Pts Creatividad)
# ---------------------------------------------------------
max_score = total_rounds * 10

print("\n" + "=" * 60)
print("🏁 ¡FIN DEL JUEGO! 🏁")
print("=" * 60)
print(f"📊 Tu Puntuación Final: {score} / {max_score} PUNTOS")

if score == max_score:
    print("🏆 Rango: ¡POLÍGLOTA MAESTRO! 🥇")
    print("¡Impecable! Traduces y hablas el idioma con fluidez.")
elif score >= max_score // 2:
    print("🥈 Rango: ¡TRADUCTOR EN PROCESO! 🥈")
    print("¡Muy buen trabajo! Tienes buen vocabulario y pronunciación.")
else:
    print("🥉 Rango: ¡PRINCIPIANTE ENTUSIASTA! 🥉")
    print("¡Sigue practicando! Repasar el vocabulario te ayudará bastante.")

print("\n¡Gracias por jugar! 👋\n")
