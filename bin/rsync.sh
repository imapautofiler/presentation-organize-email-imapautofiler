#!/bin/bash

set -x

FILES="*.html css js lib plugin img fonts"

ssh doughellmann.com 'mkdir -p ~/doughellmann.com/presentations/organize-email-imapautofiler'

rsync -av --progress $FILES doughellmann.com:~/doughellmann.com/presentations/organize-email-imapautofiler/
