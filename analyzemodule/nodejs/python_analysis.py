#!/usr/bin/env python3
import os
import sys
import requests
import math


# Kubernetes Environment Variables
kube_service_host = os.environ['KUBERNETES_SERVICE_HOST']
kube_port = os.environ['KUBERNETES_PORT_443_TCP_PORT']

with open("/var/run/secrets/kubernetes.io/serviceaccount/token", "r") as f:
    kube_token = f.read()

headers = {
    'Authorization': 'Bearer ' + kube_token,
    'Accept': 'application/json',
}


# Global CONST Variables: do not change in code.
NODE_MAX_vCPU_CAPACITY = 0
TASK_ID = sys.argv[1]
FRAMES_IN_SCENE = int(sys.argv[2])
REQUESTED_FRAMERATE = float(sys.argv[3])
APROX_FRAME_RENDER_TIME = float(sys.argv[4])
ANALYSER_vCPU = int(sys.argv[5])
REQUIRED_vCPU = APROX_FRAME_RENDER_TIME *  ANALYSER_vCPU * REQUESTED_FRAMERATE # vCPU = FrameEstimateSec * vCPUanalyser * FPS 


# Global Variables
cluster_nodes = []


# Classes
class ClusterNode:
    name = ""
    vCPU_capacity = 0
    occupied_vCPU = 0
    available_vCPU = 0

    def __init__(self, name, vCPU_capacity, currently_used_vCPU): 
        self.name = name
        self.vCPU_capacity = vCPU_capacity
        self.occupied_vCPU = currently_used_vCPU
        self.available_vCPU = self.vCPU_capacity - self.occupied_vCPU

        global NODE_MAX_vCPU_CAPACITY
        if vCPU_capacity > NODE_MAX_vCPU_CAPACITY:
            NODE_MAX_vCPU_CAPACITY = vCPU_capacity

        cluster_nodes.append(self)


# Functions
def GetClusterNodes():
    nodes_response = requests.get("https://" + kube_service_host + ":" + kube_port + "/api/v1/nodes/", headers=headers, verify=False).json()
    pods_response = requests.get("https://" + kube_service_host + ":" + kube_port + "/api/v1/pods", headers=headers, verify=False).json()

    for node in nodes_response["items"]:
        node_name = node["metadata"]["name"]
        node_cpu_usage = 0

        for pod in pods_response["items"]:
            if pod["spec"]["nodeName"] == node_name and pod["status"]["phase"] != "Succeeded" and pod["status"]["phase"] != "Failed":
                for container in pod["spec"]["containers"]:
                    if container["resources"]:
                        node_cpu_usage += int(''.join(c for c in container["resources"]["requests"]["cpu"] if c.isdigit()))
        ClusterNode(node_name, int(''.join(c for c in node["status"]["allocatable"]["cpu"] if c.isdigit())), node_cpu_usage)

def ScaleClusterHorizontal(scale_amount):
    print("STATUS: Cluster has been scaled by: ", scale_amount)

def AddRenderWorkersToQueue(number_of_workers, render_worker_required_vCPU):
    available_render_worker_hosts_spots = 0

    for node in cluster_nodes:

        available_render_worker_hosts_spots += math.floor(node.available_vCPU / render_worker_required_vCPU)

    if REQUIRED_vCPU > NODE_MAX_vCPU_CAPACITY or number_of_workers > available_render_worker_hosts_spots:
        if number_of_workers > FRAMES_IN_SCENE or number_of_workers > 99999:  #TODO: use mem_peak or mem_avg to calulate max number of worker pods
            #TODO: Error handling? something something
            print( REQUIRED_vCPU, NODE_MAX_vCPU_CAPACITY, number_of_workers, available_render_worker_hosts_spots, FRAMES_IN_SCENE)
            print("Error: Too many required render workers, to complete the submitted render task.")
        else:
            # TODO: Add sub-frames logic here ( render_workers_required * 2)
            AddRenderWorkersToQueue(number_of_workers * 2, render_worker_required_vCPU/2)
    else:
        resourceRequirements = "C" + str(int(math.ceil(REQUIRED_vCPU / number_of_workers))) 
        # Enqueue task to TaskQueue
        os.system("python3 ./nodejs/enqueueTaskToTaskQueue.py " + str(TASK_ID) + " " + str(number_of_workers) + " " + resourceRequirements)


# Main
def main():
    GetClusterNodes()
  
    SUM_available_vCPU = 0
    for node in cluster_nodes:
        SUM_available_vCPU += node.available_vCPU

    if REQUIRED_vCPU > SUM_available_vCPU:
        print("STATUS: vCPU demand is higher than available... Calling ScaleClusterHorizontal")
        cluster_missing_vCPU = REQUIRED_vCPU - SUM_available_vCPU
        ScaleClusterHorizontal(cluster_missing_vCPU)

    # Check case to determine $render_workers_required
    if REQUESTED_FRAMERATE < 1:
        render_workers_required = 1 # REQUESTED_FRAMERATE * (1 / REQUESTED_FRAMERATE)
        render_workers_vCPU = REQUIRED_vCPU
    else:
        render_workers_required = round(REQUESTED_FRAMERATE)
        render_workers_vCPU = REQUIRED_vCPU / render_workers_required
    
    # Calulate number of render workers required, and add to TaskQueue
    AddRenderWorkersToQueue(render_workers_required, render_workers_vCPU)


main()