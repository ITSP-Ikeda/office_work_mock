#!/bin/sh

set -e

wait_for_postgres() {
  echo "PostgreSQL の起動を待機中..."
  i=0
  max=30
  while [ "$i" -lt "$max" ]; do
    if ruby -rsocket -e "TCPSocket.new('db', 5432).close" 2>/dev/null; then
      echo "PostgreSQL に接続可能"
      return 0
    fi
    i=$((i + 1))
    echo "  待機中 (${i}/${max})..."
    sleep 2
  done
  echo "PostgreSQL (db:5432) に接続できませんでした"
  exit 1
}

wait_for_postgres

# 下記処理は別ファイルに記載するのがあるべき姿なので、ゆくゆくは修正したい
while true; do
  if rails db:version >/dev/null 2>&1; then
    echo "既にDBが存在しているので、「rails db:create」等の処理をスキップ"
    break
  else
    echo "DBが存在しないので、DB初期化処理を実行"
    echo "コマンド「rails db:create」を実行して処理待ち"
    rails db:create
    echo "コマンド「rails db:migrate」を実行して処理待ち"
    rails db:migrate
    echo "コマンド「rails db:seed」を実行して処理待ち"
    rails db:seed
    
  fi

  if rails db:version >/dev/null 2>&1; then
    break
  else
    echo "DBの初期化待ち（15秒）"
    sleep 15
  fi
done

rm -f tmp/pids/server.pid
rails s -p 3000 -b '0.0.0.0'

exec "$@"
