#!/bin/bash
watchmedo shell-command --recursive --ignore-directories --patterns="*.py" --wait --command='fab test'
