# iniciar o ambiente de teste/desenvolvimento

é necessário ter o [docker](https://docs.docker.com/get-docker/), docker-compose e [aws-cli](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html#cliv2-linux-install) instalados

primeiro abra o arquivo `docker-compose.yml` e troque o endpoint_url para o endpoint da sua máquina

```yml
  backend:
    build: .
    environment:
      - AWS_ACCESS_KEY_ID=123
      - AWS_SECRET_ACCESS_KEY=456
      - ENDPOINT_URL=http://192.168.1.101:4566 #coloque seu ip aqui
      - APP_ENV=dev
    volumes:
      - .:/app
    ports:
      - "5000:5000"
      - "8000:80"
```

então execute os comandos na ordem:

```sh
makefile start
```

O endpoint do flask ficará na porta 5000 e o swagger ficará na 8080

> A variável APP_ENV=dev india que o server que irá rodar no docker é o do flask, que fica recarregando com mudanças, se quiser, pode usar o do nginx, ai é só não passar a variável