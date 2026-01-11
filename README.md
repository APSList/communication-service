# Communication storitev

**Communication storitev** je gRPC strežnik, zasnovan v Pythonu, namenjen pošiljanju email sporočil strankam.

## Predpogoji
- Python 3.12+
- Pip
- `venv` za navidezna okolja
- (opcijsko) Docker za uporabo v kontejnerjih

---

## Lokalni zagon

### 1. Zagon strežnika
1. Ustvarite navidezno okolje:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
2. Namestite odvisnosti:
    ```bash
    pip install -r requirements.txt
    ```
3. Zaženite strežnik:
    ```bash
    make run
    ```

### 2. Docker možnost
1. Ustvarite Docker sliko:
    ```bash
    docker build -t communication-service .
    ```
2. Zaženite kontejner:
    ```bash
    docker run -p 50051:50051 communication-service
    ```
   
---

## Testiranje
Testi so v mapi `tests/`. Zaženite jih s:
```bash
pytest
```