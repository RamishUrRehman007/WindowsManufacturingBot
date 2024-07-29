#!/bin/bash
# make the script fail when something fails
set -o errexit

username="user"
password="password"
hostname="localhost"
port="5432"

while getopts u:P:d:h:p:n: OPT
do
    case $OPT in
        "u" ) username="$OPTARG" ;;
        "P" ) password="-p $OPTARG" ;;
        "h" ) hostname="$OPTARG" ;;
        "p" ) port="-P $OPTARG" ;;
        "d" ) database="$OPTARG" ;;
        "n" ) number="$OPTARG" ;;
    esac
done

if [ -z "${database}" ]; then
    echo "ERROR: database is not specified"
    echo "$0 -d database"
    exit 1
fi

cd $(dirname $0)

touch ~/.pgpass
echo "${hostname}:${port}:${database}:${username}:${password}" > ~/.pgpass
chmod 0600 ~/.pgpass

if [ -z "${number}" ]; then
    for migration_file in *.sql
    do
        echo "Running ${migration_file} on ${database}..."
        psql -h ${hostname} -U ${username} -w ${database} -f ${migration_file}
    done
else
    prefix=`echo ${number} | awk '{printf("%04d", $1)}'`
    psql -h ${hostname} -U ${username} -w ${database} -f ${prefix}_*.sql
fi
