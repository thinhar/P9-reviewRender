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


# Math Section
### x = (FrameEstimateSec / vCPUanalyser) / (1/FPS) 
requested_framerate=60
analyser_vCPU=0.1
aprox_frame_render_time=1 # s/frame
#requested_framerate = frame/s

#required_vCPU = (aprox_frame_render_time / 0.1) / (1 / requested_framerate) 
something = (aprox_frame_render_time * analyser_vCPU)
required_vCPU = aprox_frame_render_time *  analyser_vCPU * requested_framerate

something2 = (aprox_frame_render_time / analyser_vCPU ) 



print(required_vCPU)

available_vCPU_on_node=[1,2,3,4,5,6,7,8,9,10]
#kubectl describe nodes | grep -A 2 -e "^\s*CPU Requests"
SUM_available_vCPU=0
for i in available_vCPU_on_node:
    SUM_available_vCPU+=i
print(SUM_available_vCPU)

if required_vCPU>SUM_available_vCPU:
    print("more than available")
    cluster_missing_vCPU= required_vCPU - SUM_available_vCPU
    #ScaleClusterHorizontal cluster_missing_vCPU

# Check case to determine $render_workers_required
if requested_framerate < 1:
    render_workers_required = 1 # requested_framerate * (1/requested_framerate)
    render_workers_vCPU = required_vCPU
else:
   render_workers_required = round(requested_framerate)
   render_workers_vCPU = required_vCPU / render_workers_required
   
print(render_workers_required)
print(render_workers_vCPU)

def AddRenderWorkersToQueue():
    print("hello")
    available_render_worker_hosts_spots = 0

    for i in nodes:
        NUMBER = Node_List[i].available_vCPU_on_a_single_node / render_workers_vCPU
        x =floor(NUMBER)
        x = x + available_render_worker_hosts_spots

        #available_render_worker_hosts_spots += (int)math.Floor(Node_List[i].available_vCPU_on_a_single_node / render_workers_vCPU)


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

AddRenderWorkersToQueue()















