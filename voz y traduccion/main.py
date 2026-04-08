import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator
import random
import time
from difflib import SequenceMatcher

# === RECORD SYSTEM ===
record_file = "record.txt"

def load_record():
    try:
        with open(record_file, "r") as f:
            return int(f.read())
    except:
        return 0

def save_record(new_record):
    with open(record_file, "w") as f:
        f.write(str(new_record))

record = load_record()

# === Configuración ===
duration = 8
sample_rate = 44100
max_errors = 3
score = 0
errors = 0
combo = 0

# === Palabras por nivel ===
words_by_level = {
    "facil": [
        "gato", "perro", "casa", "árbol", "libro",
        "mesa", "silla", "agua", "pan", "sol",
        "luna", "flor", "niño", "puerta", "ventana",
        "coche", "calle", "escuela", "amigo", "familia"
    ],
    "medio": [
        "elefante", "mariposa", "computadora", "teléfono", "avión",
        "ciudad", "hospital", "restaurante", "biblioteca", "universo",
        "montaña", "playa", "bosque", "trabajo", "dinero",
        "música", "película", "idioma", "viaje", "tiempo"
    ],
    "dificil": [
        "tecnología", "universidad", "información", "pronunciación", "imaginación",
        "desarrollo", "comunicación", "responsabilidad", "conocimiento", "experiencia",
        "investigación", "oportunidad", "internacional", "independencia", "organización",
        "programación", "inteligencia", "aprendizaje", "competencia", "habilidad"
    ]
}

# === Selección de dificultad ===
print("🎮 Bienvenido al juego de pronunciación en inglés!")
print("Selecciona un nivel de dificultad: (facil, medio, dificil)")
print(f"🏆 Récord actual: {record}")

level = input("Nivel de dificultad: ").strip().lower()

while level not in words_by_level:
    print("❗ Nivel no válido. Por favor, elige entre 'facil', 'medio' o 'dificil'.")
    level = input("Nivel de dificultad: ").strip().lower()

# 🔥 10 palabras aleatorias
word_list = random.sample(words_by_level[level], 10)

print(f"\n✅ Has seleccionado el nivel '{level.capitalize()}'. ¡Buena suerte!")
print("💡 Pronuncia la traducción en inglés")
print("❤️ Tienes 3 vidas | 🔥 Haz combos para más puntos!")
time.sleep(2)

# === Inicialización ===
recognizer = sr.Recognizer()
translator = Translator()

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

# === Bucle principal ===
for word in word_list:
    print("\n==============================")
    print(f"🔤 Palabra en español: {word}")
    print(f"❤️ Vidas: {max_errors - errors} | ⭐ Puntos: {score} | 🔥 Combo: {combo}")

    for i in range(3, 0, -1):
        print(f"🎙️ Grabando en {i}...")
        time.sleep(1)

    print("🎤 ¡Habla ahora!")

    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")
    sd.wait()
    wav.write("output.wav", sample_rate, recording)

    print("✅ Grabación completa, reconociendo...")

    try:
        with sr.AudioFile("output.wav") as source:
            audio = recognizer.record(source)
            recognised = recognizer.recognize_google(audio, language="en-US").lower()

            print("📝 Dijiste:", recognised)

            translation = translator.translate(word, src='es', dest='en').text.lower()
            print("🔍 Traducción correcta:", translation)

            similarity = similar(recognised, translation)

            if similarity > 0.75:
                combo += 1
                points = 1 + combo
                score += points
                print(f"🎉 ¡Correcto! +{points} puntos (Combo x{combo})")
            else:
                errors += 1
                combo = 0
                print(f"❌ Incorrecto ({round(similarity*100)}% parecido)")
                print(f"👉 Respuesta correcta: '{translation}'")

                if errors >= max_errors:
                    print("💀 Has alcanzado el límite de errores. Fin del juego.")
                    break

    except sr.UnknownValueError:
        errors += 1
        combo = 0
        print(f"😕 No se pudo reconocer el habla. Errores: {errors}/{max_errors}")

        if errors >= max_errors:
            print("💀 Has alcanzado el límite de errores. Fin del juego.")
            break

    except sr.RequestError as e:
        print(f"❗ Error del servicio: {e}")
        break

# === Resultados ===
print("\n==============================")
print("🏁 Juego terminado")
print("⭐ Puntuación final:", score)

# 🔥 SISTEMA DE RÉCORD
if score > record:
    print("🎉 ¡NUEVO RÉCORD!")
    save_record(score)
else:
    print(f"🏆 Récord a superar: {record}")

# Mensajes finales
if score >= 10:
    print(" ¡El mejor hay que meterte a profesor de ingles!🏆🏆")
elif score >= 5:
    print(" Buen trabajo viejo👏")
else:
    print("Sigue practicando menol 📚")

print("==============================")