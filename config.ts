// app/config.ts

const API_URL = process.env.EXPO_PUBLIC_API_URL;

// Dodajemy ten sprawdzający log, żeby zobaczyć, czy na tym etapie zmienna jest odczytywana
if (!API_URL) {
    console.log("Plik config.ts: Zmienna EXPO_PUBLIC_API_URL nie została znaleziona!");
}

export const Config = {
    API_URL,
};