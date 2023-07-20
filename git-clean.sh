#!/bin/bash

USE_CHOICE=""

function clean_tree() {
    git clean -xfd
}

function warn_user() {
    echo ""
    echo "!!!WARNING!!!"
    echo "Cleaning the git tree will remove *all* local files that are not on the remote."
    echo "This could lead to removal of files like .env or local dist/ builds."
    echo ""
    read -p "Please confirm you wish to remove all local files not found on the remote (Y/N): " usr_choice
    echo ""
}

function validate_choice() {
    case $usr_choice in
    [Yy])
        echo "Cleaning git tree"
        clean_tree
        ;;
    [Nn])
        echo "Cancelling git tree clean"
        ;;
    *)
        echo "Invalid choice: $usr_choice. Exiting."
        exit 1
        ;;
    esac
}

function main() {
    clear
    warn_user
    validate_choice
}

main

exit $?
