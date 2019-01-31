import mitmproxy

def response(context, flow):
	with decoded(flow.response):
		flow.response.content = flow.response.assemble

def request(context, flow):
	with decoded(flow.request):
		flow.request.content = flow.request.assemble
