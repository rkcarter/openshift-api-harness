from pprint import pprint
from openshift import client, config
from kubernetes import client as k_client
from kubernetes.client.rest import ApiException
import yaml
#https://github.com/openshift/openshift-restclient-python/blob/master/openshift/README.md

config.load_kube_config()
oapi = client.OapiApi()
apiV1 = k_client.CoreV1Api()
auth_api = client.AuthorizationOpenshiftIoV1Api()


def list_proj():
	project_list = oapi.list_project()
	for project in project_list.items:
	    print(project.metadata)

def create_proj(project):
	body = client.V1Project(metadata={'name': project}) # V1Project | 
	pretty = 'pretty_example' # str | If 'true', then the output is pretty printed. (optional)

	try: 
	    api_response = oapi.create_project(body, pretty=pretty)
	    return api_response
	except ApiException as e:
	    print("Exception when calling OapiApi->create_project: %s\n" % e)


def list_role_binding(project):

   try: 
      api_response = auth_api.list_namespaced_role_binding(namespace="chris-sandbox")
      return api_response
   except ApiException as e:
      print("Exception when calling AuthApi->create_namespaced_role_binding: %s\n" % e)


def create_role_binding(project):

   body = client.V1RoleBinding(
      metadata={'name': 'deployerBinding'},
      role_ref={'name': 'admin'},
      subjects=[{'kind':'ServiceAccount','name': 'deployer'}]
   )  

   try: 
      api_response = auth_api.create_namespaced_role_binding(body=body, namespace=project)
      return api_response
   except ApiException as e:
      print("Exception when calling AuthApi->create_namespaced_role_binding: %s\n" % e)

def create_secrets(project):
   file = open('./secrets/deployer-dockercfg-test', 'r')
   secret_data = file.read()
   file.close()
   secret_yaml = yaml.load(secret_data)

   try: 
      api_response = apiV1.create_namespaced_secret(body=secret_yaml, namespace=project)
      return api_response
   except ApiException as e:
      print("Exception when calling OapiApi->create_namespaced_service_account: %s\n" % e)

def create_svc_accounts(project):
   file = open('./svc-account-deployer.yaml', 'r')
   svc_account_data = file.read()
   file.close()
   svc_account_yaml = yaml.load(svc_account_data)

   try: 
      api_response = apiV1.create_namespaced_service_account(body=svc_account_yaml, namespace=project)
      return api_response
   except ApiException as e:
      print("Exception when calling OapiApi->create_namespaced_service_account: %s\n" % e)

def create_pvc(project):
   file = open('./pvc.yaml', 'r')
   pvc_data = file.read()
   file.close()
   pvc_yaml = yaml.load(pvc_data)

   try:
      api_response = apiV1.create_namespaced_persistent_volume_claim(body=pvc_yaml, namespace=project)
      return api_response
   except ApiException as e:
	    print("Exception when calling OapiApi->create_pvc: %s\n" % e)

def create_dc(project, dc_name):
   file = open(dc_name, 'r')
   pvc_data = file.read()
   file.close()
   dc_yaml = yaml.load(pvc_data)

   try:
      api_response = oapi.create_namespaced_deployment_config(body=dc_yaml, namespace=project)
      return api_response
   except ApiException as e:
      print("Exception when calling OapiApi->create_dc: %s\n" % e)

def rollout_dc(project):

   body = client.V1DeploymentRequest(
      force=True,
      latest=True,
      name='db'
   )  

   try:
      api_response = oapi.create_namespaced_deployment_config_instantiate(name='db', namespace=project, body=body)
      return api_response
   except ApiException as e:
      print("Exception when calling OapiApi->create_dc: %s\n" % e)


for i in range(1, 5):
   project = "howdy" + str(i)
   create_proj(project)
   create_role_binding(project)
   create_pvc(project)
   create_dc(project, 'dc-mysql.yaml')
   rollout_dc(project)
   #i += 1
   
#create_dc('drupal.yaml')
##create_secrets(project)
##create_svc_accounts(project)
#create_svc('front-end.yaml')
#create_svc('db.yaml')
#create_route()
#pprint(resp)
