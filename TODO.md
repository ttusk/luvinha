# Demandas

- [ ] Formular tela do jogo em execução
  - [ ] Fazer input e histórico de palavras digitadas
  - [ ] Dentro do histórico é necessário mostrar a distância de contexto entre a palavra alvo
  - [ ] Adicionar botão de desistência, que mostra a palavra alvo, número de tentativas e uma mensagem gerada aleatoriamente para o usuário (ex: Você chegou perto)
  - [ ] Na parte de histórico, especificamente na distância, se possível, colocar a palavra dentro de um progress bar, de tal forma o progresso representa o quão longe a palavra está
- [ ] Formular leaderboard de usuários que jogaram e quantas tentativas levaram para alcançar a palavra alvo. Só serão colocados no leaderboard usuários que não desistiram
  - [ ] O leaderboard deve ser armazenado em um arquivo dentro do projeto de forma semiestruturada ou estruturada (ex: YAML, SQLite)
  - [ ] Quando conseguir achar a palavra, o usuário tem que ter a possibilidade de cadastrar um username para ser colocado no leaderboard
  - [ ] Adicionar um botão secreto para burlar e achar a palavra, essa função tem o papel de dinamizar a apresentação das funções do joguinho para a turma
- [ ] Embelezar a UI
- [ ] Se possível, aplicar melhores padrões de projeto dentro do código, ex: classes reaproveitáveis, assim como o `BaseScreen`
- [ ] Acoplar modelo do Huggingface dentro de um package no projeto
  - [ ] Criar modulo dentro do package para o modelo
  - [ ] Worker loop basico para polling de recebimento das mensagens, enfileirando para realização das análises
- [ ] Verificar como rodar o modelo internamente no projeto sem necessidade de um container
