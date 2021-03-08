# Sapling
## Resources
https://tezos.gitlab.io/alpha/sapling.html?highlight=sapling
https://tezos.gitlab.io/user/sandbox.html#sandboxed-mode
https://tezos.gitlab.io/introduction/howtoget.html#build-from-sources
https://opam.ocaml.org/doc/Install.html

## set up
```shell
> sudo apt install opam
> opam init
> eval $(opam env)
> opam switch create for_tezos 4.09.1
> opam install depext
> opam depext tezos
> opam install -y tezos

> sudo apt install -y rsync git m4 build-essential patch unzip wget pkg-config libgmp-dev libev-dev libhidapi-dev libffi-dev opam jq
> wget https://sh.rustup.rs/rustup-init.sh
> chmod +x rustup-init.sh
> ./rustup-init.sh --profile minimal --default-toolchain 1.44.0 -y
> source $HOME/.cargo/env

> git clone https://gitlab.com/tezos/tezos.git tezos-sources
> cd tezos-sources
> make build-deps
> eval $(opam env)
> make
> export PATH=~/tezos:$PATH
> source ./src/bin_client/bash-completion.sh
> export TEZOS_CLIENT_UNSAFE_DISABLE_DISCLAIMER=Y


> sudo add-apt-repository ppa:serokell/tezos && sudo apt-get update
> sudo apt install -y tezos-client     
> sudo apt install -y tezos-node                        
> sudo apt install -y tezos-baker-008-ptedo2zk                
> sudo apt install -y tezos-endorser-008-ptedo2zk 
> sudo apt install -y tezos-accuser-008-ptedo2zk
```

## sapling
```shell
## set up the sandboxed local node
> cd tezos-sources
> ./src/bin_node/tezos-sandboxed-node.sh 1 --connections 0 &
> eval `./src/bin_client/tezos-init-sandboxed-client.sh 1`
> tezos-autocomplete
> tezos-activate-alpha

## Create the sapling smart contract on the node
## originate the contract with its initial empty sapling storage,
## bake a block to include it.
## { } represents an empty Sapling state.
> tezos-client originate contract shielded-tez transferring 0 from bootstrap1 \
running src/proto_alpha/lib_protocol/test/contracts/sapling_contract.tz \
--init '{ }' --burn-cap 3 &

## Bake one block to include the smart contract
> tezos-client bake for baker1_key
> tezos-client sapling man

## Generate user keys
## generate two shielded keys for Alice and Bob and use them for the shielded-tez contract
## the memo size has to be indicated
> tezos-client sapling gen key alice
> tezos-client sapling use key alice for contract shielded-tez --memo-size 8
> tezos-client sapling gen key bob
> tezos-client sapling use key bob for contract shielded-tez --memo-size 8

## generate an address for Alice to receive shielded tokens.
> tezos-client sapling gen address alice
## Generated address:
## zet12nFEzWLxTCLmSGtLChYWgJN5S4pAaFqmaUJPa3gDKWhCcB88C2Q6GrxFd3Zrir1bq
## at index 1


## shield 10 tez from bootstrap1 to alice
> tezos-client sapling shield 10 from bootstrap1 to zet12nFEzWLxTCLmSGtLChYWgJN5S4pAaFqmaUJPa3gDKWhCcB88C2Q6GrxFd3Zrir1bq using shielded-tez --burn-cap 2 &
## bake again to include the transaction
> tezos-client bake for baker1_key

> tezos-client sapling get balance for alice in contract shielded-tez
# Total Sapling funds 10ꜩ

## generate an address for Bob to receive shielded tokens.
> tezos-client sapling gen address bob
# Generated address:
# zet13xKs15X9T1t7kQAx5cH1suB1sjy4UmJ3G5Ex2Rh2Q5Nno4vvLyxcXje22zUR6KrGL
# at index 1

## forge a shielded transaction from alice to bob that is saved to a file
> tezos-client sapling forge transaction 10 from alice to zet13xKs15X9T1t7kQAx5cH1suB1sjy4UmJ3G5Ex2Rh2Q5Nno4vvLyxcXje22zUR6KrGL using shielded-tez

## submit the shielded transaction from any transparent account
> tezos-client sapling submit sapling_transaction from bootstrap2 using shielded-tez --burn-cap 1 &
> tezos-client bake for baker1_key
> tezos-client sapling get balance for bob in contract shielded-tez
# Total Sapling funds 10ꜩ

## unshield from bob to any transparent account
> tezos-client sapling unshield 10 from bob to bootstrap1 using shielded-tez --burn-cap 1
> ctrl + z
> tezos-client bake for baker1_key
> fg
```