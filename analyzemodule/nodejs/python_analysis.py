#!/usr/bin/env python3
import os
import sys

first= sys.argv[1]
numbertwo= sys.argv[2]


# Math Section
### x = (FrameEstimateSec / vCPUanalyser) / (1/FPS) 
requested_framerate=0.02
analyser_vCPU=1000
aprox_frame_render_time=3000

#required_vCPU = (aprox_frame_render_time / 0.1) / (1 / requested_framerate) 
required_vCPU = (aprox_frame_render_time/analyser_vCPU)/(1/requested_framerate)

print(required_vCPU)
print(required_vCPU)

available_vCPU_on_node=[1,2,3,4,5,6,7,8,9,10]
#kubectl describe nodes | grep -A 2 -e "^\s*CPU Requests"
SUM_available_vCPU=0
for i in available_vCPU_on_node:
    SUM_available_vCPU+=i
print(SUM_available_vCPU)

SUM_available_vCPU=$(IFS=+; echo "$((${available_vCPU_on_node[*]}))")

render_workers_vCPU=1 # UNSURE: do we need to declare it, before use?

# Check if cluster requires scaling
logic="print("$required_vCPU">"$SUM_available_vCPU")" | python3
if [ logic ]
then
    cluster_missing_vCPU= echo "print("$required_vCPU"-"$SUM_available_vCPU")" | python3
    
    #ScaleClusterHorizontal cluster_missing_vCPU
fi
echo $cluster_missing_vCPU

# Check case to determine $render_workers_required
if [ requested_framerate < 1 ]
then
    render_workers_required = 1 # requested_framerate * (1/requested_framerate)
    render_workers_vCPU = required_vCPU
else
   render_workers_required = math.Round(requested_framerate)
   render_workers_vCPU = vCPU / render_workers_required
fi




AddRenderWorkersToQueue render_workers_required

AddRenderWorkersToQueue()
{
    available_render_worker_hosts_spots = 0

    for i in nodes
    do
        NUMBER = Node_List[i].available_vCPU_on_a_single_node / render_workers_vCPU
        x = python -c "from math import floor; print floor($NUMBER)"
        x = x + available_render_worker_hosts_spots

        #available_render_worker_hosts_spots += (int)math.Floor(Node_List[i].available_vCPU_on_a_single_node / render_workers_vCPU)
    done


    if [required_vCPU > Node_vCPU_Capacity] || [ $1 > available_render_worker_hosts_spots ]
    then
        if [ $1 > frames_in_scene ] || [ $1 > 99999 ]  #TODO: use mem_peak or mem_avg to calulate max number of worker pods
        then
            sa
        else
            # Make sub-tasks with sub-frames ( render_workers_required * 2)
            # TODO: Add sub-frames logic here
            AddRenderWorkersToQueue ($1 * 2)
        fi
    else
        # enqueue task to tasklist
        resourceRequirements = required_vCPU / $1
        $(python3 ./nodejs/enqueueTaskToTaskQueue.py $podname $1 $resourceRequirements >> /home/enqueueStdout)
    fi
}





#----------------------------------------------------------#
#!/usr/bin/env python3
import os
import sys

# Global CONST Variables: do not change in code.
NODE_vCPU_CAPACITY = 10 # TODO: Get from kube?
TASK_ID = sys.argv[1]
REQUESTED_FRAMERATE = sys.argv[2]
APROX_FRAME_RENDER_TIME = sys.argv[3]
ANALYSER_vCPU = sys.argv[4]
REQUIRED_vCPU = APROX_FRAME_RENDER_TIME *  ANALYSER_vCPU * REQUESTED_FRAMERATE # vCPU = FrameEstimateSec * vCPUanalyser * FPS 


# Global Variables
node_list = []


# Classes
class ClusterNode:
    available_vCPU_on_node = 0

    def __init__(self, available_vCPU): 
        self.available_vCPU_on_node = available_vCPU
        node_list.append(self)


# Functions
def ScaleClusterHorizontal(scale_amount):
    print("STATUS: Cluster has been scaled by: ", scale_amount)

def AddRenderWorkersToQueue(number_of_workers):
    available_render_worker_hosts_spots = 0

    for node in node_list:
        available_render_worker_hosts_spots += floor(node.available_vCPU_on_node / render_workers_vCPU)

    if REQUIRED_vCPU > NODE_vCPU_CAPACITY or number_of_workers > available_render_worker_hosts_spots:
        if number_of_workers > frames_in_scene or number_of_workers > 99999:  #TODO: use mem_peak or mem_avg to calulate max number of worker pods
            #TODO: Error handling? something something
            print("Error: Too many required render workers, to complete the submitted render task.")
        else:
            # TODO: Add sub-frames logic here ( render_workers_required * 2)
            AddRenderWorkersToQueue (number_of_workers * 2)
    else:
        resourceRequirements = "C" + str(int(ceil(REQUIRED_vCPU / number_of_workers))) 
        # Enqueue task to TaskQueue
        os.system("./nodejs/enqueueTaskToTaskQueue.py ", TASK_ID, " ", number_of_workers, " ", resourceRequirements)
        #$(python3 ./nodejs/enqueueTaskToTaskQueue.py $podname $1 $resourceRequirements >> /home/enqueueStdout)



# Main
def main():
    #available_vCPU_on_node = [1,2,3,4,5,6,7,8,9,10]
    #kubectl describe nodes | grep -A 2 -e "^\s*CPU Requests"

    node_1 = ClusterNode(1)
    node_2 = ClusterNode(2)
    node_3 = ClusterNode(3)   

    SUM_available_vCPU = 0
    for node in node_list:
        SUM_available_vCPU += node.available_vCPU_on_node

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
    AddRenderWorkersToQueue(render_workers_required)















