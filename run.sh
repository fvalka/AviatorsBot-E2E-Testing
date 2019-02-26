#!/bin/bash
echo $SESSIONS_KEY | gpg --batch --passphrase-fd 0 --output secrets/telegram.session --decrypt secrets/telegram.session.gpg

echo "+===============+"
echo "| Running TESTS |"
echo "+===============+"
python -m unittest