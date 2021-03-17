# Baking

https://gist.github.com/dakk/bdf6efe42ae920acc660b20080a506dd

> Source set up required

## Build node
```shell
cd tezos-sources
git checkout latest-release
git pull
make build-deps
make
```

## Node config
```
> ./tezos-node identity generate
Generating a new identity... (level: 26.00)        
Stored the new identity (idr6vr8mE8sQzpMV47qP2kmFKoPLWS) into '/home/florian/.tezos-node/identity.json'.
```

## Download snapshot for node
Go to https://snapshots-tezos.giganode.io/ and download latest snapshot then:

Retrieve the node version from the snamshot description:
```
Node version:
8f0b3220 (2021-02-19 17:22:18 +0100) (8.2+dev)
```

```shell
git checkout 8f0b3220
make build-deps
make

## IMPORTANT !!! Need to configure the node for the desired network first
./tezos-node config init --data-dir ~/tezos-edonet --network edo2net
./tezos-node snapshot import ../baking/snapshot-*
./tezos-node run --data-dir ~/tezos-edonet --network edo2net --rpc-addr 127.0.0.1:8732 --connections 10 
```

> ./tezos-client -E http://localhost:8732 activate account "baker_account" with "../baking/faucet.json" --force

> ./tezos-client -E http://localhost:8732 get balance for baker_account
9401.766724 ꜩ