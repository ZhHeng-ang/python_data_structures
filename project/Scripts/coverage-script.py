#!c:\users\16787\desktop\project\project\scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'coverage==5.0.3','console_scripts','coverage'
__requires__ = 'coverage==5.0.3'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('coverage==5.0.3', 'console_scripts', 'coverage')()
    )
