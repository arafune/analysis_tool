# -*- coding: utf-8 -*-
'''.. py:module:: splab

Module to read splab xml data files and analyze them.

lxml package is required to treat xml file.
'''

import os
import bz2
import numpy as np
from scipy import interpolate
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
        for group in self.root[0]:
            if group.get('type_name') == "RegionGroup":
                self.groups.append(SPGroup(group))


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

    rawcounts: numpy.ndarray
        row count. 4-D array. rawcounts[scan#][detector_ch#][angle#][energy#]
    '''
    def __init__(self, xmlregion):
        self.xmlregion = xmlregion
        self.name = xmlregion[0].text
        self.param = {}
        for elm in xmlregion[1]:
            if elm.get('name') == 'scan_mode':
                self.param[elm.get('name')] = elm[0].text
            elif elm.get('name') in ['num_scans', 'curves_per_scan',
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
        num_detectors = len(self.analyzer_info['Detector'])
        counts_tag = './/ulong[@type_name="Counts"]'
        counts = np.array([[int(count)
                            for count
                            in elm.text.split()]
                           for elm
                           in xmlregion.findall(counts_tag)])
        # self.rawcount[scan#][ch#][angle#][energy#]
        self.rawcounts = counts.reshape(self.param['num_scans'],
                                        self.param['curves_per_scan'],
                                        self.param['values_per_curve'] +
                                        self.mcd_head_tail[0] +
                                        self.mcd_head_tail[1],
                                        num_detectors).transpose(0, 3, 1, 2)
        # energy_axis_ch
        # E_{0n} =E_0+s_n =E1–h*delta+sn
        E1 = self.param['kinetic_energy']
        mcdhead = self.mcd_head_tail[0]
        delta = self.param['scan_delta']
        # sn = dn * pass_energy
        #    = self.analyzer_info['Detector'][n][1] * self.param['pass_energy']

        # en = sn + (self.values_per_curve + self.mcd_head_tail[0] +
        # self.mcd_head_tail[1] -1) * self.param['scan_delta']
        # values_per_curve+
        # np.linspace(sn, en
        self.energy_axis = np.array([E1 + delta * i
                                     for i
                                     in range(self.param['values_per_curve'])])
        # energy_axis_ch would be local before release
        self.energy_axis_ch = np.array([[E1 - mcdhead * delta +
                                         self.analyzer_info['Detector'][i][1] *
                                         self.param['pass_energy'] +
                                         delta * j
                                         for j in
                                         range(self.param['values_per_curve'] +
                                               self.mcd_head_tail[0] +
                                               self.mcd_head_tail[1])]
                                        for i in range(num_detectors)])

        # Most cases, the required data is
        # * angle resolved
        #  but
        # summing up each detector data and each scan
        scan_integrated = np.sum(self.rawcounts, axis=0)
        apportioned = []
        for ch, data in enumerate(scan_integrated):
            interp_f = interpolate.interp1d(self.energy_axis_ch[ch],
                                            data,
                                            bounds_error=False,
                                            fill_value='extrapolate')
            # Note: As broadcast technique in interp1d is used, the
            # intensity at the highest energy is little bit different
            # from that in the output from SpecsLab originally.
            apportioned.append(interp_f(self.energy_axis))
#            correcteddata = self.allocateintensity(data,
#                                                   self.energy_axis_ch[ch])
#            apportioned.append(correcteddata)
        apportioned = np.array(apportioned)
        self.arpes = np.sum(apportioned, axis=0)
        for elm in xmlregion.findall(".//string[@name='name']"):
            if elm.text == "OrdinateRange":
                p = elm.getparent()
                anglespan = float(
                    p.find(".//any[@name='value']").find(".//double").text)
        self.anglespan = anglespan 

    def allocateintensity(self, counts_2d, energy_axis_ch):
        # Slow!  Use broadcast technique!!
        '''.. py:method:: allocateintensity(counts2D, energy_axis_ch)

        Return array allocated the signal by interpolating

        parameters
        ------------

        counts_2d: np.array
            ARPES mapping raw data. The values are usually int.

        energy_axis_ch: np.array
            numpy array. Use energy_axis_ch[ch#]
'''
        corrected = []
        for a_data in counts_2d:
            interpf = interpolate.interp1d(energy_axis_ch,
                                           a_data,
                                           bounds_error=False,
                                           fill_value=(a_data[0],
                                                       a_data[-1]))
            corrected.append(interpf(self.energy_axis))
        return np.array(corrected)


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
