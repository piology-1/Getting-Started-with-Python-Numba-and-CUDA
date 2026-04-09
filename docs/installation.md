# Installations-Logbuch: CUDA & Numba unter Windows 11

Diese Dokumentation beschreibt meinen persönlichen Setup-Prozess von GPU-beschleunigtem Python mit **Numba** und **uv** unter Windows 11. Dies ist kein universeller Guide, sondern eine Dokumentation meiner spezifischen Installation (ohne Conda).

## Die zentrale Hürde: CUDA Toolkit v13.x vs. v12.x

Mein ursprünglicher Plan war es, die aktuellste Version zu nutzen (**CUDA Toolkit 13.2**, Stand April 2026 [Download hier](https://developer.nvidia.com/cuda-downloads)). Trotz erfolgreicher Installation und aktueller Treiber konnte Numba die GPU zwar erkennen (`cuda.detect()`), aber die benötigten Bibliotheken nicht initialisieren (`cuda.is_available()` blieb `False`).

### Die Fehlerursache (Strukturänderung im Toolkit)

Wie in [GitHub Issue #452](https://github.com/NVIDIA/numba-cuda/issues/452) diskutiert, liegt das Problem wohl an einer geänderten Ordnerstruktur in neueren CUDA-Releases:

- **Erwartung von Numba:** Die Compiler-Bibliothek `nvvm64_*.dll` wird im Verzeichnis `...\nvvm\bin\` erwartet.
- **Realität in CUDA 13.x:** NVIDIA verschiebt diese Dateien in einen Unterordner `...\nvvm\bin\x64\`.
- **Kompatibilität:** Numba benötigt oft einige Zeit, um die LLVM-Schnittstellen an brandneue CUDA-Versionen anzupassen.

**Die Lösung:** Komplette Deinstallation von v13.2 und Downgrade auf das stabilere **CUDA Toolkit 12.8** ([CUDA Toolkit 12.8 Download Archive](https://developer.nvidia.com/cuda-12-8-0-download-archive)).

---

## Finaler Installations-Prozess

### 1. Download & Installation

Ich habe mich für die lokale Installation unter Windows 11 entschieden, um volle Kontrolle über die Pfade zu behalten.

- **Installer:** [CUDA Toolkit 12.8 Download Archive](https://developer.nvidia.com/cuda-12-8-0-download-archive?target_os=Windows&target_arch=x86_64&target_version=11&target_type=exe_local)
- **Vorgehen:** "Express Installation" wählen.
- **Wichtig:** Nach der Installation den PC neu starten, damit die Systemdienste korrekt geladen werden.

### 2. Validierung der Hardware-Kommunikation

In der PowerShell prüfen, ob der NVIDIA-Compiler (`nvcc`) im System-Path registriert ist:

```powershell
nvcc --version
```

### 3. Konfiguration der Umgebungsvariablen

Besonders nach einem Downgrade ist es essenziell, alte Pfad-Reste (z.B. von v13.2) zu entfernen. Numba verlässt sich primär auf `CUDA_HOME` und die `CUDA_PATH`-Variable.

Ich habe die Variablen via **PowerShell mit Administratorrechten** gesetzt:

```powershell
# Setzen der Pfade für Version 12.8
[System.Environment]::SetEnvironmentVariable("CUDA_HOME", "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.8", "Machine")
[System.Environment]::SetEnvironmentVariable("CUDA_PATH", "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.8", "Machine")
[System.Environment]::SetEnvironmentVariable("CUDA_PATH_V12_8", "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.8", "Machine")
```

**Check:**
Mit `echo $env:CUDA_HOME` bzw. `echo $env:CUDA_HOME` prüfen, ob die Pfade korrekt ausgegeben werden. Falls leer, PowerShell neu starten. Schaue auch im Windows Verzeich nach, ob die Dateien dort liegen.

**Manueller Check:**
Unter _Systemumgebungsvariablen bearbeiten_ -> _Umgebungsvariablen_ sicherstellen, dass unter den Systemvariablen alle Einträge mit `v13.2` gelöscht und die `v12.8`-Einträge vorhanden sind.
[Systemumgebungsvariablen](/docs/Systemvariablen.png)

---

## Python Setup & Validierung

### Conda vs. uv

In der offiziellen [Numba Dokumentation](https://numba.readthedocs.io/en/stable/user/installing.html#installation) wird oft `conda` empfohlen. Da ich jedoch **uv** (pip-basiert) nutze, liefert die Python-Umgebung das Toolkit nicht automatisch mit (vgl. [hier](https://numba.readthedocs.io/en/stable/user/installing.html#installing-using-pip)). Die oben beschriebene **systemweite Installation** des Toolkits ist daher erforderlich.

**Installation der Python-Pakete:**

```bash
uv add numba numba-cuda
```

**Erfolgstest:**
Erstelle eine Datei `check_gpu.py`:

```python
from numba import cuda

print(f"CUDA verfügbar: {cuda.is_available()}")
if cuda.is_available():
    cuda.detect()
```

Ausführen mit

```bash
uv run check_gpu.py
```

**Alternativ**:
Für den vollen Test kann auch [`test_cuda.py`](/examples/test_cuda.py) hilfreich sein

## Nützliche Befehle

- `numba -s`: Zeigt eine detaillierte Systemanalyse und listet alle gefundenen (oder fehlenden) CUDA-Bibliotheken auf.
- `nvidia-smi`: Prüft den Status des Grafiktreibers und die aktuell unterstützte CUDA-Version des Treibers.

## Nützliche Links

- [CUDA Downloads](https://developer.nvidia.com/cuda-downloads)
- [Numba for CUDA GPUs](https://numba.readthedocs.io/en/stable/cuda/index.html)
- [Setting CUDA Installation Path](https://numba.readthedocs.io/en/stable/cuda/overview.html#cudatoolkit-lookup)

---

_Letzte Aktualisierung: 9. April 2026_
