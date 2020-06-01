import os
import math
import random
import time
import json
import sys
import csv

time1=time.time()


def dictionary_check(cluster_dict,K,dataset,data_dict):
    classification_dict=initial_initialization(K)
    for points in dataset:
        index_cluster=euclidean(points,cluster_dict,data_dict)
        classification_dict[index_cluster].append(points)
    list_len=[len(v) for v in classification_dict.values()]
    if min(list_len)>3:
        print('A')
        flag=True
    else:
        print('B')
        flag=False
    return flag

def counting_sets(DS):
    count_num=0
    if len(DS)==0:
        return 0
    else:
        for items in DS.values():
            count_num+=items[0]
        return count_num

def euclidean_calculation(point1,point2):
    difference=[]
    for points in zip(point1,point2):
        difference.append(points[1]-points[0])
    difference=[x**2 for x in difference]
    sum_diff=sum(difference)
    sum_diff=(sum_diff**(1/2))
    return sum_diff


def updating_set_values(list1,list2):
    listt=[]
    for points in zip(list1,list2):
        listt.append(points[0]+points[1])
    return listt

def Set_update(list_tuples,first_Set,data_dic):
    for items in list_tuples:
        point=data_dic[items[1]]
        first_Set[items[0]][0]+=1
        first_Set[items[0]][1]=updating_set_values(first_Set[items[0]][1],point)
        first_Set[items[0]][2]=[v**2 for v in first_Set[items[0]][1]]
    return first_Set

def random_initializtion2(K,splitted1,data_dict):
    cluster_point={}
    for clusterings in range(K):
        selected=random.choice(splitted1)
        cluster_point[clusterings]=data_dict[selected]
    return cluster_point

def initial_initialization(K):
    classification_dict={}
    for values in range(K):
        classification_dict[values]=[]
    return classification_dict


def euclidean(point,cluster_dict,data_dict):
    point=data_dict[point]
    difference=[]
    distance_lists=[]
    for clusters in cluster_dict.values():
        #clusters=data_dict[clusters]
        difference=[]
        for points in zip(clusters,point):
            difference.append(points[1]-points[0])
        difference=[x**2 for x in difference]
        sum_diff=sum(difference)
        sum_diff=(sum_diff**(1/2))
        distance_lists.append(sum_diff)
    index_cluster=distance_lists.index(min(distance_lists))
    return index_cluster   

def centroid_calc(classification_dict,data_dict):
    final_list=[]
    for values in classification_dict.keys():
        average_result=[]
        for list_items in zip(*[data_dict[v] for v in classification_dict[values]]):
            average_result.append(sum(list_items))
        average_result=[v/len(classification_dict[values]) for v in average_result]
        final_list.append(average_result)
    return final_list

def final_euclidean(final_centroid,prev_centroid):
    difference=[]
    for points in zip(final_centroid,prev_centroid):
        difference.append(points[0]-points[1])
    difference=[x**2 for x in difference]
    sum_diff=sum(difference)
    sum_diff=(sum_diff**(1/2))
    return sum_diff


def centroid_centroid(cluster_dict):
    average_result=[]
    for list_items in zip(*[v for v in cluster_dict.values()]):
        average_result.append(sum(list_items))
    average_result=[v/len(cluster_dict.values()) for v in average_result]
    return average_result

def average_cluster(values,classification_dict,data_dict):
    average_result=[]
    L_A=[data_dict[v] for v in classification_dict[values]]
    for list_items in zip(*[v for v in L_A]):
        average_result.append(sum(list_items))
    return average_result




def discard_set(classification_dict,data_dict):
    Discard_Set={}
    for keys in classification_dict.keys():
        N=len(classification_dict[keys])
        sum_list=average_cluster(keys,classification_dict,data_dict)
        list1=[v**2 for v in sum_list]
        DS_set=[N,sum_list,list1]
        Discard_Set[keys]=DS_set
    return Discard_Set



def Maha(list_keys,data_dict2,Discard_Set):    
    DS_list=[]
    remaining_list=[]
    for point in list_keys:
        point_calc=data_dict2[point]
        P=[]
        for keys in Discard_Set.keys():
            difference=[]
            N=Discard_Set[keys][0]
            centroid=[v/N for v in Discard_Set[keys][1]]
            dim=len(centroid)
            M=[]
            for points in zip(centroid,Discard_Set[keys][2]):
                M.append(((points[1]/N)-(points[0]**2))**(1/2))
            for points in zip(centroid,point_calc,M):
                try:
                    difference.append(((points[1]-points[0])/points[2])**2)
                except:
                    difference.append(((points[1]-points[0]))**2)
                #difference.append(((points[1]-points[0])/points[2])**2)
            sum_diff=sum(difference)
            mahalanobis=(sum_diff)**(1/2)
            P.append(mahalanobis)
        index_min=P.index(min(P))
        if min(P)<(2*(math.sqrt(dim))):
            DS_list.append((index_min,point))
        else:
            remaining_list.append(point)
    return DS_list,remaining_list



def Kmeansplus(K,dataset,data_dict):
    centroids=[]
    point1=random.choice(dataset)
    centroids.append(point1)
    for cent in range(K-1):
        print(cent)
        dist=[]
        for points in dataset:
            d=[]
            for j in range(len(centroids)):
                distance=euclidean_calculation(data_dict[centroids[j]],data_dict[points])
                d.append(distance)
            dist.append(min(d))
        index_dist=dist.index(max(dist))
        centroids.append(dataset[index_dist])
    class_dict={}
    for values in range(len(centroids)):
        class_dict[values]=data_dict[centroids[values]]
    if K<11:
        valz=dictionary_check(class_dict,K,dataset,data_dict)
        if valz:
            return class_dict
        else:
            K_result=KMeans(dataset,5*K,data_dict,5,outliers=set())
            filtered_datapoints=[]
            for values in K_result.items():
                if len(values[1])>10:
                    filtered_datapoints.append(values[0])
                    filtered_datapoints.extend(values[1])
            Z=Kmeansplus(K,list(set(filtered_datapoints)),data_dict)
            return Z
    else:
        return class_dict

def KMeans11(dataset,K,data_dict,no_it,outliers=set()):
    cluster_dict=Kmeansplus(K,dataset,data_dict)
    #cluster_dict=random_initializtion(K,dataset,data_dict,outliers)
    for iterations in range(no_it):
        classification_dict=initial_initialization(K)
        for points in dataset:
            index_cluster=euclidean(points,cluster_dict,data_dict)
            classification_dict[index_cluster].append(points)
        average_clusters=centroid_calc(classification_dict,data_dict)
        average_dict=dict(enumerate(average_clusters))
        final_centroid=centroid_centroid(average_dict)
        prev_centroid=centroid_centroid(cluster_dict)
        diff_distance=final_euclidean(final_centroid,prev_centroid)
        if diff_distance<0.001:
            break
        else:
            print(diff_distance)
            cluster_dict=average_dict
    return classification_dict


def KMeans(dataset,K,data_dict,no_it,outliers=set()):
    cluster_dict=initialization(K,dataset,data_dict,outliers)
    for iterations in range(no_it):
        classification_dict=initial_initialization(K)
        for points in dataset:
            index_cluster=euclidean(points,cluster_dict,data_dict)
            classification_dict[index_cluster].append(points)
        average_clusters=centroid_calc(classification_dict,data_dict)
        average_dict=dict(enumerate(average_clusters))
        final_centroid=centroid_centroid(average_dict)
        prev_centroid=centroid_centroid(cluster_dict)
        diff_distance=final_euclidean(final_centroid,prev_centroid)
        if diff_distance<0.001:
            break
        else:
            print(diff_distance)
            cluster_dict=average_dict
    return classification_dict


def rem_outliers(number_clusters,length,outliers=set()):
    random_num = set()
    while (len(random_num)!=number_clusters or len(random_num.intersection(outliers))!= 0):
        random_num = set(random.sample(range(0, length, 1), number_clusters))
    return random_num

def initialization(K,splitted1,data_dict,outliers=set()):
    cluster_point={}
    list_points=rem_outliers(K,len(splitted1),outliers)
    i=0
    for items in list_points:
        cluster_point[i]=data_dict[items]
        i+=1
    return cluster_point



if __name__ == "__main__":
    start_time = time.time()
    Path = sys.argv[1]
    print(Path)
    n_clusters = int(sys.argv[2])
    out_file1 = sys.argv[3]
    out_file2 = sys.argv[4]
    
    
    csv_file = open(out_file2, 'w')
    csvwriter = csv.writer(csv_file)
    csvwriter.writerow(['round_id', "nof_cluster_discard", "nof_point_discard", "nof_cluster_compression", "nof_point_compression",'nof_point_retained'])

    file_count=0
    first_file=True
    data_files = os.listdir(Path)
    for file in sorted(data_files):
        file_count+=1
        file_path = os.path.join(Path, file)
        if (first_file):
            first_file=False
            data_dict={}
            file1 = open(file_path,"r") 
            for components in file1:
                splitted=(components.split('\n')[0]).split(',')
                data_dict[int(splitted[0])]=[float(x) for x in splitted[1:]]
            keys_list=list(data_dict.keys())
            random.shuffle(keys_list)
            def check():
                flag=1
                while flag==1:
                    universal_dict={}
                    if len(keys_list)<100000:
                        K=KMeans(keys_list,5*n_clusters,data_dict,3,outliers=set())
                    else:
                        K=KMeans(keys_list,3*n_clusters,data_dict,5,outliers=set())
                    filtered_datapoints=[]
                    for values in K.items():
                        if len(values[1])>3:
                            filtered_datapoints.append(values[0])
                            filtered_datapoints.extend(values[1])
                        else:
                            for v in values[1]:
                                universal_dict[v]=-1
                            universal_dict[values[0]]=-1
                    print('K') 
                    K=KMeans11(list(set(filtered_datapoints)),n_clusters,data_dict,10)
                    if n_clusters<11:
                        for values in K.values():
                            if len(values)<2:
                                flag=1
                        list_len=[len(v) for v in K.values()]
                        if min(list_len)>10:
                            flag=0
                    else:
                        flag=0
                return K,universal_dict
            K=check()
            universal_dict=K[1]
            K=K[0]
            for keys in K.keys():
                for values in K[keys]:
                    universal_dict[values]=keys

            DS=discard_set(K,data_dict)
            CS={}
            RS=[]
            csvwriter.writerow([file_count,len(DS),counting_sets(DS),len(CS),counting_sets(CS),len(RS)])
            print(file_count,len(DS),counting_sets(DS),len(CS),counting_sets(CS),len(RS))
            
        else:
            file2 = open(file_path,"r") 
            data_dict2={}
            for components in file2:
                splitted=(components.split('\n')[0]).split(',')
                if int(splitted[0])!=-1:
                    data_dict2[int(splitted[0])]=[float(x) for x in splitted[1:]]
            list_keys=list(data_dict2.keys())
            K=Maha(list_keys,data_dict2,DS)
            print(len(K[1]),'a')
            DS=Set_update(K[0],DS,data_dict2)
            for values in K[0]:
                universal_dict[values[1]]=values[0]
            for values in K[1]:
                universal_dict[values]=-1
            
            conditionz=False
            if conditionz:
                K_meanss=KMeans(K,5*n_clusters,data_dict,10,outliers=set())
                anot_dict={}
                for values in K_meanss.items():
                    if len(values[1])>3:
                        anot_dict[values[0]]=values[1]
                    else:
                        RS11=[]
                        RS11.append(values[0])
                        RS11.append(values[1])
                CS=discard_set(anot_dict,data_dict2)
                
            csvwriter.writerow([file_count,len(DS),counting_sets(DS),len(CS),counting_sets(CS),len(RS)])
            print(file_count,len(DS),counting_sets(DS),len(CS),counting_sets(CS),len(RS))
            
            
    
    DD=sorted(universal_dict.items(), key = lambda kv:(kv[0]))
    D2={k:v for k,v in DD}
    with open(out_file1, 'w') as fp:
        json.dump(D2, fp)
    print('U ',len(universal_dict))    
    print('Duration:',time.time()-start_time)