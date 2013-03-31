#!/bin/bash
cd `dirname $0`
format_day=`date -d '7 days ago' +"%Y-%m-%d"`
echo ${format_day}
python clearFile.py
rm -rf /home/app_bestgames/content_engine/sina/${format_day}
