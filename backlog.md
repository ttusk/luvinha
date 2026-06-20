# Backlog

## Done

- [x] Criar package `glove` para carregar embeddings GloVe e calcular similaridade
- [x] Validar palavras em português com `pyspellchecker`
- [x] Tela do jogo em execução com input e histórico de palavras
- [x] Histórico ordenado por similaridade com progress bar
- [x] Estrutura de telas com `BaseScreen` reaproveitável
- [x] Estilos por tela (`.tcss`) e layout responsivo
- [x] Testes para `GloveModel` e `WordValidator`
- [x] Botão de desistência: mostrar palavra alvo, número de tentativas e mensagem aleatória
- [x] Detectar vitória quando o usuário digita a palavra exata
- [x] Leaderboard de usuários (somente quem não desistiu)
  - [x] Armazenar em SQLite (`~/.luvinha/leaderboard.db`)
  - [x] Permitir cadastrar username ao vencer
  - [x] Tela de ranking acessível pelo menu principal
- [x] Botão secreto de cheat (`ctrl+shift+c`) para dinamizar apresentações
- [x] Correção de bugs: navegação por Esc, desistência que fechava o app, placeholder de palavra inválida, ids duplicados em "Como Jogar", cache de palavras elegíveis

## To do

- [ ] Continuar embelezando a UI
- [ ] Modo Cronometrado (botão existe na seleção de modo mas não implementa nada)
