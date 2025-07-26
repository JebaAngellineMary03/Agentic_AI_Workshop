from graph.langgraph_workflow import build_langgraph_workflow

workflow = build_langgraph_workflow()

query = input("Enter your question: ")
response = workflow.invoke({"query": query})
print("\n📘 Final Summary:\n", response)