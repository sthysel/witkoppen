#!/bin/bash
PGUSER=witkoppen
PGPASSWORD=witkoppen
export PGUSER PGPASSWORD
pg_dump -C -Fc -D -h localhost -U witkoppen -f ~/Desktop/Witkoppen/Patient-Record-Backup-`date "+%Y%m%d:%H:%M:%S"`.dat witkoppen
