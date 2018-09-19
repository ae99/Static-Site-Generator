import re
import html

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

class VariableNode(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self, context):
        print(self.value, "----", context)
        return html.escape(str(eval(self.value, context.copy(), context)))

class PythonNode(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self, context):
        # Adjust for whitespace
        try:
            remove = re.match(r'^\s*', self.value).group().split('\n')[-1]
            self.value = self.value[len(remove)+1:].replace('\n' + remove , '\n')
        except AttributeError:
            pass
        exec(self.value, {}, context)
        return ""


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
            group.addChild(VariableNode(curretNode[2:-2]))
        elif re.match(r'{\$\s*((.|\n)+)\s*\$}', curretNode) != None:
            group.addChild(PythonNode(curretNode[2:-2]))
        else:
            group.addChild(TextNode(curretNode))
    return group

def template_to_string(template, context):
    splitter = re.compile(r'({%.*?%}|{{.*?}}|{\$.*?\$})', re.DOTALL)
    nodes = re.split(splitter, template)
    tree = construct_tree(nodes)
    return tree.evaluate(context)

