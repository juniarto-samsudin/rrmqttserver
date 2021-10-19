#!/bin/bash

pushd ${0%/*}/ >/dev/null && BASE_DIR=$PWD && popd >/dev/null
cd "$BASE_DIR"

conditions=(true)
services=(scaft-ml-server)
descriptions=("SC@FT ML Server")
commands=("/usr/local/bin/gunicorn --config gunicorn-conf.py run:app")
users=(scaft-admin)
installs=(true)

for ((i=0;i<${#services[*]};i++)) ; do
    ${conditions[$i]} || continue
    service=${services[i]}

    systemctl is-active $service >/dev/null && {
        echo -e "\x1b[32mStop current running service $service...\x1b[0m"
        $sudo systemctl stop $service
        sleep 2
    }

    systemctl is-active $service >/dev/null && {
        echo -e "\x1b[31mStop running service $service failed\x1b[0m"
        exit 1
    }

    ${installs[i]} || {
        [ -f /etc/systemd/system/$service.service ] && {
            echo -e "\x1b[32mDelete service $service\x1b[0m"
            $sudo systemctl disable $service
            $sudo rm -f /etc/systemd/system/$service.service
            $sudo systemctl daemon-reload
        }
        continue
    }

    echo -e "\x1b[32mGenerate Unit file for service $service...\x1b[0m"
    cat >/tmp/$service.service <<EOF
[Unit]
Description=${descriptions[i]}
After=syslog.target network.target

[Service]
WorkingDirectory=$BASE_DIR
ExecStart=${commands[i]}
User=${users[i]}
KillMode=control-group
Restart=on-failure
RestartSec=10s

[Install]
WantedBy=multi-user.target
EOF
    
    echo -e "\x1b[32mInstall service $service...\x1b[0m"
    $sudo mv /tmp/$service.service /etc/systemd/system/ || {
        echo -e "\x1b[31mInstall service $service failed\x1b[0m"
        exit 1
    }

    echo -e "\x1b[32mEnable service $service...\x1b[0m"
    $sudo systemctl enable $service || {
        echo -e "\x1b[31mEnable service $service failed\x1b[0m"
        exit 1
    }

    echo -e "\x1b[32mStart service $service...\x1b[0m"
    $sudo systemctl start $service || {
        echo -e "\x1b[31mStart service $service failed\x1b[0m"
        exit 1
    }

    sleep 3
    echo -e "\x1b[32mCheck status of service $service...\x1b[0m"
    systemctl status --no-pager $service
    systemctl is-active $service >/dev/null || {
        echo -e "\x1b[31mSrvice $service is not running after start\x1b[0m"
        exit 1
    }

done

exit 0
