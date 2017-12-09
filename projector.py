from kubernetes.client.rest import ApiException
from kubernetes import client as k_client
from pprint import pprint
from openshift import client, config
import yaml
#https://github.com/openshift/openshift-restclient-python/blob/master/openshift/README.md

config.load_kube_config()
oapi = client.OapiApi()
apiV1 = k_client.CoreV1Api()

def list_proj():
	project_list = oapi.list_project()
	for project in project_list.items:
	    print project.metadata

def create_proj():
	body = client.V1Project(metadata={'name': 'howdy1'}) # V1Project | 
	pretty = 'pretty_example' # str | If 'true', then the output is pretty printed. (optional)

	try: 
	    api_response = oapi.create_project(body, pretty=pretty)
	    return api_response
	except ApiException as e:
	    print("Exception when calling OapiApi->create_project: %s\n" % e)

def create_pvc():
   file = open('./pvc.yaml', 'r')
   pvc_data = file.read()
   file.close()
   pvc_yaml = yaml.load(pvc_data)

   try:
      api_response = apiV1.create_namespaced_persistent_volume_claim(body=pvc_yaml, namespace='howdy1')
      return api_response
   except ApiException as e:
	    print("Exception when calling OapiApi->create_pvc: %s\n" % e)

def create_dc(dc_name):
   file = open(dc_name, 'r')
   pvc_data = file.read()
   file.close()
   dc_yaml = yaml.load(pvc_data)

   try:
      api_response = oapi.create_namespaced_deployment_config(body=dc_yaml, namespace='howdy1')
      return api_response
   except ApiException as e:
	    print("Exception when calling OapiApi->create_dc: %s\n" % e)

create_proj()
create_pvc()
#create_dc('drupal.yaml')
resp = create_dc('mysql.yaml')
#create_svc('front-end.yaml')
#create_svc('db.yaml')
#create_route()

pprint(resp)
