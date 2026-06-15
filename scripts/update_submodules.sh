#!/bin/bash
# Utility to pull the latest changes for all OSINT submodules
echo "Updating all OSINT submodules to their latest remote commits..."
git submodule update --remote --merge
echo "Update complete! Don't forget to commit the bumped pointers."
