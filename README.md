openssl genpkey -algorithm RSA -out app/core/keys/jwt-private.pem -pkeyopt rsa_keygen_bits:2048

openssl rsa -pubout -in app/core/keys/jwt-private.pem -out app/core/keys/jwt-public.pem