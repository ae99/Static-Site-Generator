import templater
import json

with open('src/context.json', 'r') as f:
    context = json.load(f)

with open('src/index.html', 'r') as f:
    template = ''
    for line in f:
    	template += line

out = templater.template_to_string(template, context)

with open('out/index.html', 'w+') as f:
	f.write(out)