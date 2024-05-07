#!/usr/bin/env sh

GOFILE=rosInstall.go

printf "// GENERATED - DO NOT EDIT\npackage main\n\nconst (\n" > $GOFILE

SCRIPT_FOLDER="ros_install_scripts"
SCRIPTS=$( ls $SCRIPT_FOLDER/*.sh)

for SCRIPT in $SCRIPTS
do
    VAR=$(basename "$SCRIPT" .sh)
    printf "    %s = \`%s\`\n\n" "$VAR" "$(cat "$SCRIPT")" >> $GOFILE
done


printf ")" >> $GOFILE
