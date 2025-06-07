#!/bin/bash

mkdir -p certs

# Generate Root CA key
openssl genrsa -out certs/rootCA.key 4096

# Generate Root CA certificate (self-signed)
openssl req -x509 -new -nodes -key certs/rootCA.key -sha256 -days 3650 \
    -out certs/rootCA.pem -subj "/CN=MyRootCA"

# Generate Mirror key and CSR
openssl genrsa -out certs/mirror.key 2048
openssl req -new -key certs/mirror.key -out certs/mirror.csr -subj "/CN=mirror.local"

# Sign Mirror CSR with Root CA
openssl x509 -req -in certs/mirror.csr -CA certs/rootCA.pem -CAkey certs/rootCA.key \
    -CAcreateserial -out certs/mirror.crt -days 825 -sha256

# Generate Staging key and CSR
openssl genrsa -out certs/staging.key 2048
openssl req -new -key certs/staging.key -out certs/staging.csr -subj "/CN=staging.local"

# Sign Staging CSR with Root CA
openssl x509 -req -in certs/staging.csr -CA certs/rootCA.pem -CAkey certs/rootCA.key \
    -CAcreateserial -out certs/staging.crt -days 825 -sha256

echo "✅ Certificates generated in certs/"
