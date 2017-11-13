from graphviz import Digraph
import sys


class TreeNode:
	def __init__(self, name):
		self.__name = name
		self.__parent = None
		self.__children = []
		
	def getName(self):
		return self.__name
		
	def getParent(self):
		return self.__parent
		
	def __setParent(self, p):
		self.__parent = p
		
	def addChild(self, c):
		self.__children.append(c)
		c.__setParent(self)
	
	def children(self):
		return self.__children
	

def treeToDot(parent, dot):
	n = dot.node(parent.getName())
	
	for c in parent.children():
		cn = treeToDot(c, dot)	
		dot.edge(parent.getName(), c.getName())
		
	return n
	

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Usage: TreeParse.py <file.tree>"
		quit()
	
	file = open(sys.argv[1])

	lines = file.readlines()

	dot = Digraph(comment=sys.argv[1])
	lastIndent = 0
	newIndent = 0
	lastNode = None
	root = None
	root_was_set = False
	for l in lines:
		nodename = l.strip()
		newIndent  = len(l) - len(l.lstrip('\t')) #count number of leading tabs
		
		if(len(nodename) == 0):
			continue
		
		node = TreeNode(nodename)
			
		# first node detected, setting up for root
		if root is None:
			if root_was_set:
				raise RuntimeError("Root was already set")
			root = node
			root_was_set = True

		else: # not root node
			if newIndent > lastIndent: #going deeper
				if newIndent - lastIndent != 1:
					raise RuntimeError("Can only step down one level at a time")
				lastNode.addChild(node)
			elif newIndent == lastIndent:
				lastNode.getParent().addChild(node)
			else: 
				currentParent = lastNode.getParent()
				for i in range(0, lastIndent - newIndent):
					currentParent = currentParent.getParent()
				currentParent.addChild(node)

		lastIndent = newIndent
		lastNode = node

	file.close()

	treeToDot(root, dot)


	dot.render("test.gv", view=True)
