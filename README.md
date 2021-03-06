[![CI](https://github.com/lfvilella/valora-challenge/workflows/CI/badge.svg?event=push)](https://github.com/lfvilella/valora-challenge/actions?query=event%3Apush+branch%3Amaster+workflow%3ACI)
[![license](https://img.shields.io/github/license/lfvilella/valora-challenge.svg)](https://github.com/lfvilella/valora-challenge/blob/master/LICENSE)

# Valora Challenge
Valora's Company Selective process challenge.

[Go to Orders on Website](http://valora.lfvilella.com/admin/commerce/order)
```
User: root
Password: 123
```

Tech Stack:
- Python
- Django
- Django-REST
- Docker / docker-compose


# Running locally

    $ make build

    $ make createsuperuser

    $ make up

Optional:

    $ make test

Open admin: http://localhost:8000/admin

# Postman Test

Import this [Postman Collection](./docs/postman/valora-challenge.postman_collection.json) to test locally.

Commented Test: [See the Video on YouTube](https://www.youtube.com/watch?v=apaY1ptgUDY)

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/apaY1ptgUDY/0.jpg)](https://www.youtube.com/watch?v=apaY1ptgUDY)

# Changing Order Status
![valora-giphy](https://user-images.githubusercontent.com/45940140/89242027-ed596d80-d5d6-11ea-9a1c-8f335b76d0a8.gif)
