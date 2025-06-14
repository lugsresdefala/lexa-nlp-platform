#!/bin/bash

# Script para fazer merge de todas as branches remotas no main
# Uso: bash merge_all_branches_to_main.sh

set -e

REPO_URL="https://github.com/lugsresdefala/lexa.git"
REPO_NAME="lexa"

# Clone o repositório, se ainda não existir
if [ ! -d "$REPO_NAME" ]; then
  git clone "$REPO_URL"
fi

cd "$REPO_NAME"

# Atualiza todas as referências remotas
git fetch --all

# Garante estar na branch main e atualizada
git checkout main
git pull origin main

# Lista todas as branches remotas, exceto main e HEAD
for branch in $(git branch -r | grep -v "origin/main" | grep -v "origin/HEAD" | sed 's/origin\///'); do
  echo "======================================="
  echo "Fazendo merge da branch: $branch"
  git merge origin/$branch || {
    echo "Conflito ao fazer merge da branch $branch. Resolva o conflito e continue.";
    exit 1
  }
done

# Push final para o repositório remoto
git push origin main

echo "Todos os merges foram feitos com sucesso!"
