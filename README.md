# Part 1

Please inspect [the script](https://github.com/qwrtln/url-parser/blob/main/main.py).
To see it in action, see [the workflow output](https://github.com/qwrtln/url-parser/actions/runs/12109126187/job/33757905211) (steps starting with 'Run image').


# Part 2

Refer to the [Dockerfile](https://github.com/qwrtln/url-parser/blob/main/Dockerfile).
The build process is in [this workflow](https://github.com/qwrtln/url-parser/actions/runs/12109126187/job/33757897437).
It also adds [a snippet](https://github.com/qwrtln/url-parser/blob/main/daemon_snippet.txt) to make the script sleep indefinitely.
The other build job builds without the snippet for singlle run executions.
Both images are uploaded as artifacts.

You can see the k8s manifest [here](https://github.com/qwrtln/url-parser/blob/main/deployment.yaml).

# Part 3

See the workflow [here](https://github.com/qwrtln/url-parser/blob/main/.github/workflows/ci.yml).
You can see the runs in the [Actions tab](https://github.com/qwrtln/url-parser/actions).

# Part 4

Please see the output of the "Show 2 ways..." step in [the workflow](https://github.com/qwrtln/url-parser/actions/runs/12109126187/job/33757905211).

# Bonus

Regexp and parsing, concurrency (async), security and trust models, system orchestration, pipelines and automation.
