# Baking

https://gist.github.com/dakk/bdf6efe42ae920acc660b20080a506dd

> Source set up required: https://tezos.gitlab.io/introduction/howtoget.html#environment

## Set-up
```shell
sudo apt-get install build-essential git m4 unzip rsync curl libev-dev libgmp-dev pkg-config libhidapi-dev
sudo apt-get install bubblewrap
sudo adduser tezos
wget https://github.com/ocaml/opam/releases/download/2.0.8/opam-2.0.8-x86_64-linux  
sudo mv opam-2.0.8-x86_64-linux /usr/local/bin/opam 
sudo chmod a+x /usr/local/bin/opam
opam init --comp=4.09.1 --disable-sandboxing
opam switch 4.09.1
opam update
eval $(opam env)

wget https://sh.rustup.rs/rustup-init.sh
chmod +x rustup-init.sh 
./rustup-init.sh --profile minimal --default-toolchain 1.44.0 -y   
source $HOME/.cargo/env     

make build-deps
make
```

## Build node
```shell
cd tezos-sources
git checkout latest-release
git pull
make build-deps
make
```

## Download snapshot for node
Go to https://snapshots-tezos.giganode.io/ and download latest snapshot then:

Retrieve the node version from the snamshot description:
```
Node version:
8f0b3220 (2021-02-19 17:22:18 +0100) (8.2+dev)
```


## Node config

```shell
git checkout 8f0b3220
make build-deps
make

## IMPORTANT !!! Need to configure the node for the desired network first
./tezos-node config init --data-dir ~/tezos-edonet --network edo2net
./tezos-node identity generate --data-dir ~/tezos-edonet
./tezos-node snapshot import ../baking/snapshot-* --data-dir ~/tezos-edonet --network edo2net
./tezos-node run --rpc-addr 127.0.0.1:8732 --connections 10 --data-dir ~/tezos-edonet --network edo2net
```

> ./tezos-client -E http://localhost:8732 activate account "baker_account" with "../baking/faucet.json" --force

> ./tezos-client -E http://localhost:8732 get balance for baker_account
9401.766724 ꜩ