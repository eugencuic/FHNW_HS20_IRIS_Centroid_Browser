from tqdm.auto import tqdm
from irisreader.data.mg2k_centroids import LAMBDA_MIN, LAMBDA_MAX, assign_mg2k_centroids
from irisreader import obs_iterator
import pandas as pd
import numpy as np

obsit = obs_iterator("/data2/iris/2014/01/01", read_v4=False) # iterate through 2014/01/01

#create empty variables for table centroid_count
col_names =  ['observation', 'step', 'centroid', 'count']
centroid_count_oneday  = pd.DataFrame(columns = col_names) #panda DF for table centroid_count
n_obs = 0

#create empty variables for table observation
obs_path = [] #list that will append the observation path


#create empty variables for table ypixels
col_names =  ['observation', 'step', 'ypixels', 'image']
ypixels_oneday  = pd.DataFrame(columns = col_names)



for obs in tqdm( obsit ): #iterate through each observation
    n_obs +=1 #used to for indexing observation
    obs_path.append(obs.path) # appends list with all observations path
    
    if obs.raster.has_line("Mg II k"):
        raster = obs.raster("Mg II k")
        steps = raster.n_steps

        for step in range( steps ): #iterate through each step 
            img = raster.get_interpolated_image_step( step, LAMBDA_MIN, LAMBDA_MAX, n_breaks=216 )
            centroids = assign_mg2k_centroids( img ) # assgin centroids to the image
            
            (unique, counts) = np.unique(np.array(centroids), return_counts=True) #two lists with the frequency and count
                        
            centroid_step_data = {'observation': n_obs, 'step': step, 'centroid': unique, 'count': counts}
            centroid_step = pd.DataFrame(centroid_step_data)
            centroid_count_oneday = centroid_count_oneday.append(centroid_step)
            
            ypixels_step_data = {'observation': n_obs, 'step': step, 'ypixels': [img], 'image': [obs.sji("Si IV")] }
            ypixels_step = pd.DataFrame(ypixels_step_data)
            ypixels_oneday = ypixels_oneday.append(ypixels_step)
            
observation = pd.DataFrame({'observation': obs_path}) #creates a panda DF to write to DB            
            
            
            