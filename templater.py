import re
import html
example_doc = """
<html>
{{name}}
    <ul>
    {% for item in range(0,10) %}
        {% if item > 4 %}
            <li>{{name + str(item)}}</li>
        {% endif %}
    {% endfor %}
    </ul>
</html>
"""

regexes = {
    'include': r'{%\s*(include\s+(\w+\.\w+))\s*%}',
    'if': r'{%\s*if\s+(.+)\s*%}',
    'endif': r'{%\s*endif\s*%}',
    'for': r'{%\s*for\s+(.+)\s+in\s+(.+)\s*%}',
    'endfor': r'{%\s*endfor\s*%}',
    'expr': r'{{\s*(.+)\s*}}',
}


class Node:
    def evaluate(self):
        pass
        # Returns a string

class TextNode(Node):
    """
    thisText = TextNode("Value of the thisText")
    thisText.evaluate()
    """
    def __init__(self, value):
        self.value = value.strip()


    def evaluate(self, context):
        return str(self.value)


class GroupNode(Node):
    def __init__(self):
        self.children = []

    def addChild(self, newNode):
        self.children.append(newNode)

    def evaluate(self, context):
        theString = ""
        for node in self.children:
            theString += node.evaluate(context)

        return theString

class PythonNode(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self, context):
        return html.escape(str(eval(self.value, {}, context)))


class IfNode(Node):
    def __init__(self, condition, child):
        self.condition = condition
        self.child = child

    def evaluate(self, context):
        if eval(self.condition, {}, context):
            return self.child.evaluate(context)
        else:
            return ""

class ForNode(Node):
    def __init__(self, variableName, iterable, child):
        self.variableName = variableName
        self.iterable = iterable
        self.child = child

    def evaluate(self, context):
        iterable = eval(self.iterable, {}, context)
        variableName = self.variableName
        newString = ""
        for item in iterable:
            context[variableName] = item
            newString += self.child.evaluate(context)

        return newString


def construct_tree(nodes, escapeRegex = None):
    group = GroupNode()
    while len(nodes) > 0:
        curretNode = nodes.pop(0)
        if (escapeRegex != None and re.match(escapeRegex, curretNode) != None):
            return group
        elif re.match(r'{%\s*for\s+(.+)\s+in\s+(.+)\s*%}', curretNode) != None:
            curretNode = curretNode[2:-2].strip()[3:].strip().split('in')
            group.addChild(ForNode(curretNode[0].strip(), curretNode[1].strip(), construct_tree(nodes, r'{%\s*endfor\s*%}')))
        elif re.match(r'{%\s*if\s+(.+)\s*%}', curretNode) != None:
            curretNode = curretNode[2:-2].strip()[3:].strip()
            group.addChild(IfNode(curretNode, construct_tree(nodes, r'{%\s*endif\s*%}')))
        elif re.match(r'{{\s*(.+)\s*}}', curretNode) != None:
            group.addChild(PythonNode(curretNode[2:-2]))
        else:
            group.addChild(TextNode(curretNode))
    return group

def template_to_string(template, context):
    nodes = re.split(r'({%.*%}|{{.*}})', template)
    tree = construct_tree(nodes)
    return tree.evaluate(context)


# print(template_to_string(example_doc, {'name': "Alex!"}))
