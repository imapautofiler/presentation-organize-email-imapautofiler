#!/bin/bash

set -x

FILES="*.html css js lib plugin *.svg img fonts"

ssh doughellmann.com 'mkdir -p ~/doughellmann.com/presentations/working-with-imap-email-servers'

rsync -av --progress $FILES doughellmann.com:~/doughellmann.com/presentations/working-with-imap-email-servers/
