# Backlog

## Done

- [x] Criar package `glove` para carregar embeddings GloVe e calcular similaridade
- [x] Validar palavras em português com `pyspellchecker`
- [x] Tela do jogo em execução com input e histórico de palavras
- [x] Histórico ordenado por similaridade com progress bar
- [x] Estrutura de telas com `BaseScreen` reaproveitável
- [x] Estilos por tela (`.tcss`) e layout responsivo
- [x] Testes para `GloveModel` e `WordValidator`

## To do

- [ ] Botão de desistência: mostrar palavra alvo, número de tentativas e mensagem aleatória
- [ ] Detectar vitória quando o usuário digita a palavra exata
- [ ] Leaderboard de usuários (somente quem não desistiu)
  - [ ] Armazenar em arquivo semiestruturado (YAML ou SQLite)
  - [ ] Permitir cadastrar username ao vencer
- [ ] Botão secreto de cheat para dinamizar apresentações
- [ ] Continuar embelezando a UI
