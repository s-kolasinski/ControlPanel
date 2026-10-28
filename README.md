# Rocket Mission Control Panel

Projekt przygotowany w ramach zadania rekrutacyjnego do zespołu **AGH Space Systems**.

Aplikacja stanowi panel kontrolny (GUI), służący do monitorowania telemetrii oraz sterowania podsystemami rakiety w czasie rzeczywistym.

## Opis

Aplikacja to graficzny interfejs użytkownika komunikujący się z symulatorem rakiety za pośrednictwem protokołu TCP.

**Główne funkcjonalności:**
* **Telemetria w czasie rzeczywistym:** Płynne wizualizacje danych z czujników z wykorzystaniem biblioteki ECharts (poziom paliwa i utleniacza) oraz niestandardowych animacji CSS (dynamiczny słupek wysokości, ciśnienie, kąt nachylenia).
* **Asynchroniczna komunikacja sieciowa:** Pętla nasłuchująca działa w tle (`asyncio`), gwarantując, że odbieranie ramek TCP nie blokuje odświeżania interfejsu w przeglądarce.
* **Sterowanie sprzętem:** Manualna kontrola nad serwomechanizmami (zawory tankowania za pomocą suwaków) oraz przekaźnikami (spadochron, zapalniki utleniacza za pomocą przełączników).
* **Zautomatyzowana procedura startowa:** Dedykowany przycisk **LAUNCH** uruchamia asynchroniczną sekwencję zapłonu. Skrypt dba o krytyczny timing operacji, otwierając zawory główne (paliwo, utleniacz) oraz uruchamiając zapalnik w ściśle określonych odstępach czasowych, chroniąc silnik przed zalaniem lub wybuchem.



## Dokumentacja

### Wymagania systemowe i biblioteki

Projekt do działania warstwy wizualnej wykorzystuje framework **NiceGUI**.
Dodatkowo aplikacja opiera się na wbudowanej w Pythona bibliotece `asyncio` (nie wymaga instalacji) oraz zewnętrznej, dostarczonej w ramach zadania paczce `communication_library`.
Dodatkowo do zadania został dołączony symulator rakiety oraz serwer proxy. Są one dostępne pod linkiem: https://github.com/AGH-Space-Systems/software_zadanie_rekrutacyjne_2026

### Instalacja środowiska

1. Sklonuj repozytorium na swój komputer.
2. Upewnij się, że posiadasz zainstalowanego Pythona (zalecana wersja 3.8 lub nowsza).
3. Zainstaluj wymagane pakiety za pomocą menedżera pakietów `pip`. Otwórz terminal w folderze projektu i wpisz poniższą komendę:

```bash
pip install nicegui
```


### Uruchomienie

Przed uruchomieniem aplikacji upewnij się, że symulator oraz jego serwer są włączone (domyślnie nasłuchuje na `127.0.0.1:3000`). 
Należy pamiętać, że folder z biblioteką `communication_library` musi znajdować się w głównym katalogu projektu.

Aby uruchomić panel kontrolny, wywołaj główny plik aplikacji:

```bash
python main.py
```

Aplikacja automatycznie otworzy się w domyślnej przeglądarce internetowej.
