# Discription
This Is a Script For Watch [ Hackerone - Bugcrowd - Intigriti - YesWeHack ] Programs And Send Notification When Scope Changed


# Config File

### Create This Path For Config File 
``` ~/.Watcher/config.ini ```

### Example OF Config File

``` 

[DISCORD]
WEBHOOK = { ENTER YOUR DISCORD WEBHOOK URL }

[PLATFORMS]
HACKERONE ={ True | False}
BUGCROWD = { True | False}
INTIGRITI ={ True | False}
YESWEHACK ={ True | False}

[MESSAGE]
NEW_TARGET_TITLE    = { MSG }
SCOPE_UPDATE_TITLE  = { MSG }
OUT_OF_SCOPE_UPDATE = { MSG }

[DB]
BASE_DB_PATH = { ENTER DB SAVE PATH }

[PERFORMANCE]
PRINT = { True | False}
SEND_NOTIFICATION = { True | False}
OS = { ENTER YOUR OS}

```

### CronTab

*/5 * * * * /usr/local/bin/python3 {SCRIPT PATH} >> /var/log/script.log 2>&1

