#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: maximilian c. koeller
@email: maximilian.koeller@meduniwien.ac.at
@topic: extracts the mean caliper of geometries contained wihtin GeoJSON files.
"""

# -----------------------------------------------------------------------------
""" LIBRARIES """

# SHIPPED
import os
import json

# THRID PARTY
import geopandas as gpd
import pandas as pd
from tqdm import tqdm
# COSTUM
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
""" FUNCTIONS """
def _util_func(geoms, px_res : float, cls_dec : dict):

    df = pd.DataFrame([], columns=cls_desc.keys())
    
    for key, desc in cls_desc.items():
        mask = geoms.name.isin(desc)
        bounds = geoms[mask].bounds
        caliper = (bounds.maxx - bounds.minx) * px_res
        mean_caliper = caliper.mean()
        df[key] = [mean_caliper]
        
    return df


def calculate_mean_caliper(path : str, px_res : float, cls_dec : dict,
                           slide : str):
    """
    Calculates the mean caliper of geometries contained in a GeoJSON file

    Parameters
    ----------
    path : str
        path to the GeoJSON file.
    px_res : TYPE
        pixel resolution of the original image.
    cls_desc : dict
        A description of the classes that should be used and how they are 
        combined.
        
    Returns
    -------
    mean_caliper : float
        the mean caliper of all geometries.

    """
    with open(path,'r') as f:
        feature_list = json.load(f)
    try:
        geoms = gpd.GeoDataFrame.from_features(feature_list)
        classification = geoms.classification.to_dict()
        classification = gpd.GeoDataFrame.from_dict(classification).T
        geoms = pd.concat([geoms,classification], axis=1)
        mean_caliper = _util_func(geoms, px_res, cls_desc)
        mean_caliper['slide'] = [slide]
        return mean_caliper
    except:
        mean_caliper = pd.DataFrame([], columns = cls_desc.keys())
        
        for key in cls_desc.keys():
            mean_caliper[key] = ['NA']
        mean_caliper['slide'] = [slide]
        return mean_caliper
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
""" MAIN SCRIPT """
if __name__ == "__main__":
    ### SET PARAMETERS ###
    path = 'PATH/TO/DIR'
    output_dir = 'PATH/TO/DIR'
    datasets = os.listdir(path)
    px_res = 0.1214
    
    ### DEFINE CLASS DESCRIPTION ###
    cls_desc = {
        '1+' : ['1+','2+','3+'],
        '2+' : ['2+','3+'],
        '3+' : ['3+'],
        'negative' : ['Negative'],
        'negative_and_1plus' : ['Negative', '1+'],
        'negative_and_1plus_and_2plus' : ['Negative', '1+', '2+']
        }
    
    
    ### EXTRACT MEAN CALIPER ###
    for dataset in tqdm(datasets):
        root = os.path.join(path, dataset)
    
        folders = os.listdir(root)
    
        
        for folder in tqdm(folders):
            slides = os.listdir(os.path.join(root,folder))
            results = pd.DataFrame([])
            for slide in tqdm(slides):  
                mean_caliper = calculate_mean_caliper(
                    os.path.join(root,folder,slide), px_res, cls_desc, slide)
                results = pd.concat([results, mean_caliper])
            results = results.set_index('slide')
                    
            results.to_csv(
                os.path.join(
                    output_dir,
                    f'mean_caliper_{dataset}_{folder}.csv')
                )


