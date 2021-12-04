#!/bin/sh
autopep8 --in-place --aggressive src/application.py
echo "src/application.py complete"
autopep8 --in-place --aggressive src/apps.py
echo "src/apps.py complete"
autopep8 --in-place --aggressive src/test/tests.py
echo "src/test/tests.py complete"
autopep8 --in-place --aggressive src/forms.py
echo "src/forms.py complete"
autopep8 --in-place --aggressive models/recommend.py
echo "models/recommend.py complete"
autopep8 --in-place --aggressive models/stats.py
echo "models/stats.py complete"