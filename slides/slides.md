---
theme: slides/solarized-light.json
author: Luiz Gustavo
date: MMMM dd, YYYY
paging: Slide %d / %d
---

# Luvinha

Jogo de adivinhação semântica em terminal usando GloVe

Luiz Gustavo, Leonardo Brito, Karoline Rodrigues, Raquel, Enzo, Breno e André

---

# O que é

Jogo inspirado no Contexto. Adivinhe uma palavra secreta em português baseado em proximidade semântica.

Cada palpite recebe uma pontuação de 0 a 1000. 1000 = palavra exata.

```
> gato        →  850  ████████░░
> abelha      →  120  █░░░░░░░░░
> cachorro    → 1000  ██████████
```

---

# Fundamentação

**Hipótese distribucional** (Firth, 1957): palavras em contextos similares têm significados similares.

Isso se traduz em representações vetoriais — word embeddings. Cada palavra é um ponto em um espaço de 300 dimensões. Proximidade no espaço = proximidade semântica.

Modelo: **GloVe 300d** (NILC, português brasileiro), 930k palavras, via HuggingFace Hub.

---

# GloVe

GloVe modela **probabilidades condicionais** de co-ocorrência no corpus. A similaridade semântica entre duas palavras é derivada da razão entre suas probabilidades de aparecerem em contextos comuns.

```
┌─────────────────────────────────────────────────────
│  Corpus: "cachorro late no quintal"                 │
│                                                     │
│  P("late" | "cachorro") = 0.85  ← alta              │
│  P("mia"  | "cachorro") = 0.02  ← baixa             │
│                                                     │
│  O embedding aprende:                               │
│  vet("cachorro") · vet("late") ≈ log(0.85)          │
│  vet("cachorro") · vet("mia")  ≈ log(0.02)          │
└─────────────────────────────────────────────────────┘
```

Captura padrões globais do corpus — não só janelas locais. Vetor final: `wi + w̃i`.

---

# Similaridade de cossenos

Mede o ângulo θ entre dois vetores de embedding:

```
       ↑
       │  cachorro
       │ 
       │╱  θ
       │──────→ gato
      ╱ │
     ╱  │
    ╱   │
  abelha
```

- θ entre **cachorro** e **gato**: pequeno → similaridade alta
- θ entre **cachorro** e **abelha**: grande → similaridade baixa

Retorna valor em [−1, 1]. No jogo, normalizamos para [0, 1000].

A busca por palavras mais similares é feita via multiplicação de matrizes (`vectors @ vec`), calculando similaridade contra todo o vocabulário de uma vez.

---

# Demo: similaridade

```python
import math, random

def sim(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x**2 for x in a)) *
                  math.sqrt(sum(y**2 for y in b)))

random.seed(42)
base = [random.gauss(0, 1) for _ in range(10)]
cachorro = base
gato = [x + random.gauss(0, 0.2) for x in base]
abelha = [random.gauss(0, 1) for _ in range(10)]

print(f"cachorro × gato:    {sim(cachorro, gato)*1000:.0f}")
print(f"cachorro × abelha:  {sim(cachorro, abelha)*1000:.0f}")
```

_Ctrl+E para rodar_

---

# Arquitetura

```
luvinha/
├── main.py
├── glove/
│   ├── glove.py          # embeddings + similaridade
│   └── validator.py      # spellchecker + vocabulário
├── leaderboard/
│   └── leaderboard.py    # SQLite
├── app/
│   ├── app.py            # Textual App
│   └── screens/
│       ├── main_menu/
│       ├── classic_mode/
│       ├── win/
│       ├── give_up/
│       ├── leaderboard/
│       └── cheat/
└── tests/
```

Separação entre motor semântico, persistência e interface.

---

# Carregamento do modelo

Dois arquivos do HuggingFace Hub (`nilc-nlp/glove-300d`):

- `embeddings.safetensors` → array NumPy `(930k × 300)`
- `vocab.txt` → lista de palavras + dicionário `word_to_index`

Roda em thread separada — a UI não bloqueia. 1.12 GB baixado na primeira execução, cacheado localmente.

---

# Similaridade e palavra secreta

```python
class GloveModel:
    def similarity(self, w1, w2):
        vec1 = self._vectors[self._word_to_index[w1]]
        vec2 = self._vectors[self._word_to_index[w2]]
        dot = float(np.dot(vec1, vec2))
        return dot / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

    def random_word(self):
        if self._eligible_words is None:
            self._eligible_words = [w for w in self._vocab
                                    if is_valid_word(w)]
        return random.choice(self._eligible_words)
```

`_eligible_words` é cacheado — evita refiltrar a cada sorteio.

---

# Validação

Duas camadas: spell checker (português) + pertinência ao vocabulário GloVe.

```python
from spellchecker import SpellChecker

_spell = SpellChecker(language="pt")

def is_valid_word(word):
    return len(word) >= 2 and word.lower() in _spell.known({word.lower()})

class WordValidator:
    def is_known(self, word):
        return is_valid_word(word) and self._glove.has_word(word)
```

O spell checker também filtra o vocabulário do GloVe — os 930k tokens incluem lixo (fragmentos, números, typos). Sem filtragem, `random_word()` poderia sortear `xqq` ou `3.14`. O cache de `_eligible_words` reduz para ~100k palavras válidas.

Palavras compostas com hífen são um edge case — o spell checker e o GloVe tokenizam de formas diferentes.

---

# Loop do jogo

```python
def _process_guess(self, guess):
    if not self._validator.is_known(guess):
        self._show_invalid_word()       # 1.5s de feedback
        return

    self.tentativas += 1
    score = round(self.glove.similarity(guess, self.secret) * 1000)
    self.guesses = {**self.guesses, guess: score}

    if score > (self.maior_proximidade or -1):
        self.melhor_palpite = guess
        self.maior_proximidade = score

    if guess == self.secret:
        self._on_win()                  # push WinScreen
```

A lógica toda cabe em ~15 linhas. O resto é UI.

---

# Interface

Textual: framework TUI reativo com CSS-like styling. `reactive` attributes disparam watchers automaticamente — quando `guesses` muda, o ranking se atualiza sozinho.

Cada palpite gera um `GuessItem` com `ProgressBar`. Navegação completa por teclado.

---

# Obrigado

**Luvinha** — jogo de adivinhação semântica com GloVe

```python
# uv run luvinha
print("Boa sorte.")
```
