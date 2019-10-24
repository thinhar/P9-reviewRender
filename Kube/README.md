# P7-DimensionalShopping
To get our kubernetes configuration running, follow the steps in this file.

## Steps to Setup Cluster
1. Start a kubernetes cluster in Azure that allows for HTTP access. Just follow the instructions to create a basic Azure Kubernetes Service. 
2. Fill in the secret-template.yml file with ipvanish login information and rename it "sek.yaml"
3. Download the Azure Command-Line-Interface here: https://aka.ms/installazurecliwindows 
4. Download the Kubernetes Command-Line-Interface. Windows users can execute the following powershell command to install the choco package manager: "Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))". Then, to download Kubernetes-CLI, execute "choco install kubernetes-cli".
5. Now, delete the folder "C:\Users\USERNAME\.kube". As far as we know, it's only necessary to delete the config file within, but who cares, as the files are generated again. 
6. Login to azure with command: "az login", follow its instructions
7. Login to a specific cluster (the one we created in step 1) with the command: "az aks get-credentials --resource-group CLUSTERRESOURCEGROUP --name CLUSTERNAME". The config file in the directoriy .kube (step 5) saves our cluster information, and will therefore have to be deleted every time we wish to access a new cluster with this command. 
8. Build the cluster with our configurations with command: "kubectl apply -f PATHTOREPOSITORY\P7-DimensionalShopping\Backend\Kubernetes\dimensionalKubeDeployments.yaml"

## Status
Check the status of the cluster with commands: "kubectl get all", "kubectl describe ITEM", "kubectl logs ITEM", etc. 

## Delete Cluster
Delete the cluster with command: "az aks delete --resource-group CLUSTERRESOURCEGROUP --name CLUSTERNAME --no-wait"