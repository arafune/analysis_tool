# -*- coding: utf-8 -*-
'''.. py:module:: splab

Module to read splab xml data files and analyze them.

lxml package is required to treat xml file.
'''

import os
import bz2
import numpy as np
from lxml import etree


class SPLab(object):
    '''..py:class:: SPlab(xmlfile)

Treat a SPLab xml file as the Python Object

    Parameters
    -----------
    
    xmlfile: filename or file handle of a Specs xml file

    Attributes
    -----------
    root: lxml.etree._Element

    version: text
        version number of SPlab.

    groups: list
        list object stores SPGroup object
    '''
    def __init__(self, file):
        xml = etree.parse(file)
        self.root = xml.getroot()
        self.version = self.root.get('version')
        self.groups = []
        for gr in self.root[0]:
            if gr.get('type_name') == "RegionGroup":
                self.groups.append(SPGroup(gr))


class SPGroup(object):
    '''.. py:class:: SPGroup(group)

    Capsulated a "RegionGroup" struct

    Attributes
    ----------
    name: text
        group name

    regions: list
        list object stores SPRegion object    
    '''
    def __init__(self, xmlgroup):
        self.name = xmlgroup[0].text
        self.regions = []
        for region in xmlgroup[1]:
            if region.get('type_name') == "RegionData":
                self.regions.append(SPRegion(region))


class SPRegion(object):
    '''.. py:class:: SPRegion(region)

    Capsulated a "RegionData" struct

    Attributes
    -----------
    name: text
        region name

    param: dictionary
        dictionary object stores measurement parameters

    mcd_head_tail: tuple
        value of mcd head and tail

    analyer_info: dictionary
        dictionary object stores name and dispersion element  for detector

    counts: numpy.ndarray
        row_count.  The first axis is ch#.  
        The second energy, the third (non-dispersion, usually axis).

    

    
    '''
    def __init__(self, xmlregion):
        self.xmlregion = xmlregion
        self.name = xmlregion[0].text
        self.param = {}
        for elm in xmlregion[1]:
            if 'scan_mode' == elm.get('name'):
                self.param[elm.get('name')] = elm[0].text
            elif elm.get('name') in  ['num_scans', 'curves_per_scan',
                                    'values_per_curve']:
                self.param[elm.get('name')] = int(elm.text)
            else:
                try:
                    self.param[elm.get('name')] = float(elm.text)
                except ValueError:
                    self.param[elm.get('name')] = elm.text
        self.mcd_head_tail = (int(xmlregion[2].text), int(xmlregion[3].text))
        self.analyzer_info = {}
        analyzer = xmlregion.find('.//struct[@type_name="AnalyzerInfo"]')
        self.analyzer_info["name"] = analyzer[0].text
        detectors = xmlregion.find('.//sequence[@type_name="DetectorSeq"]')
        self.analyzer_info['Detector'] = np.array([[float(elm2.text)
                                                    for elm2 in elm
                                                    if elm2.tag == 'double']
                                                   for elm in detectors])
        counts = np.array([int(tmp) for tmp in
                           xmlregion.find('.//ulong[@type_name="Counts"]').
                           text.split()])
        self.counts = counts.reshape(self.param["curves_per_scan"],
                                     self.param["values_per_curve"]+
                                     self.mcd_head_tail[0]+
                                     self.mcd_head_tail[1],
                                     len(self.analyzer_info['Detector']))
                       

def load(splab_xml):
    '''.. py:function:: load(filename)

    Load Splab xml file to make SPLab object

    Parameters
    -----------
    splab_xml: str
        Filename of SPLab xml file. Bzipped file is acceptable
'''
    if os.path.splitext(splab_xml)[1] == ".bz2":
        try:
            xml = bz2.open(splab_xml, mode='rt')
        except AttributeError:
            xml = bz2.BZ2File(splab_xml, mode='r')
    else:
        xml = open(splab_xml)
    splab = SPLab(xml)
    return splab
