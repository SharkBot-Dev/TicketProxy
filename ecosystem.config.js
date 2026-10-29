const common = {
    cwd: __dirname,
    script: 'bot.py',
    interpreter: '.venv/bin/python3',
    interpreter_args: '-u',
    exec_mode: 'fork',
};

module.exports = {
    apps: [
        {
            ...common,
            name: 'ticket-proxy-bot',
        },
    ],
};