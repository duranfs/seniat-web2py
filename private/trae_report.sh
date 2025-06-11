#!/bin/bash
export SSHPASS='Oracle$123'
echo "iniciando proceso y copia de reportes RMAN..."
sshpass  -e  ssh oracle12@sun2315p /export/home/oracle12/monitorbd/reporte_rman.sh > ./error.log
sshpass  -e  ssh oracle12@sun2315p /export/home/oracle12/monitorbd/reporte_rman12.sh >> ./error.log
sshpass  -e  sftp oracle12@sun2315p <<EOF >> ./error.log
get monitorbd/*.txt
exit
EOF

echo "Proceso finalizado..."
#sshpass scp sun2315p:/export/home/oracle12/monitorbd/reporte_rman.txt .
#sshpass scp sun2315p:/export/home/oracle12/monitorbd/reporte_rman12.txt .
