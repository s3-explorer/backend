# iniciar o ambiente de teste/desenvolvimento

é necessário ter o [docker](https://docs.docker.com/get-docker/), docker-compose e [aws-cli](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html#cliv2-linux-install) instalados

então execute os comandos na ordem:

```sh
docker-compose up -d
sleep 60 # aguarde um pouco para que os containers subam normalmente
makefile start-localstack
```

O endpoint do flask ficará na porta 5000 e o swagger ficará na 8080