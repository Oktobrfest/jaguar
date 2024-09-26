#!/bin/sh
echo "ENTRYPOINT SCRIPT STARTED..."

echo $(pwd)

cd static

echo $(pwd)


npm run build

cd ..
cd ..
echo "Working directory before startup: $(pwd)"

APP_PORT=${APP_PORT:-5021}
DEBUG_PORT=${DEBUG_PORT:-5022}

echo "IDE IS: ${IDE}"
if [ "$FLASK_ENV" = "development" ] || [ "$FLASK_DEBUG" = "1" ]; then
    echo "Development environment detected"
    if [ "$IDE" = "vscode" ]; then
        echo "VSCODE DEBUGGING:::::: Installing debugpy & Starting the
        application with: python -m debugpy --wait-for-client --listen 0.0.0.0:${DEBUG_PORT} -m flask run --host=0.0.0.0 --port=${APP_PORT} ;; the debugger is ${DEBUG_PORT}  and app port is ${APP_PORT} ; FLASK_APP env is ${FLASK_APP}"
        pip install debugpy
        # --without-threads  --no-reload
        python -Xfrozen_modules=off -m debugpy --wait-for-client --listen 0.0.0.0:${DEBUG_PORT} -m flask run --host=0.0.0.0 --port=${APP_PORT} --no-reload
    elif [ "$IDE" = "pycharm" ]; then
        pip install pydevd-pycharm==242.10180.30
        echo "PYCHARM DEBUGGING:::: Starting the application with:"
        # echo "(uwsgi --py-autoreload 1 uwsgi.ini).."
        # uwsgi --py-autoreload 1 --pyargv "-Xfrozen_modules=off" /app/uwsgi.ini
        python -m flask run --host=0.0.0.0 --port=${APP_PORT}
    fi
    if [ "$IDE" = "vsdev" ]; then
     echo "STARTING DEVELOPMENT USING: ${IDE} ; EXCECUTED: flask run --host=0.0.0.0 --port=${APP_PORT} --debugger --reload"
     flask run --host=0.0.0.0 --port=${APP_PORT} --debugger --reload
    fi
else
    echo "Starting the application without debugger..."
    uwsgi /app/uwsgi.ini # flask run --host=0.0.0.0  --port=5020(OLD PORT)
fi

