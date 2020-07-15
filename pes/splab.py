# -*- coding: utf-8 -*-
"""Module to read splab xml data files and analyze them.

lxml package is required to treat xml file.
"""

import bz2
import os

import numpy as np
from lxml import etree
from scipy import interpolate

import pes.arpes as arpes


class SPLab:
    """Treat a SPLab xml file as the Python Object.

    Parameters
    -----------
    xmlfile: filename or file handle of a Specs xml file

    Attributes
    -----------
    root: lxml.etree._Element

    version: str
        version number of SPlab.

    groups: list
        list object stores SPGroup object

    """

    def __init__(self, xmlfile: str) -> None:
        """Initialization.
        
        Parameters
        ------------
        xmlfile: str
            filename of xmlfile.
        """
        xml = etree.parse(xmlfile)
        self.root = xml.getroot()
        self.version: str = self.root.get("version")
        self.groups = []
        for group in self.root[0]:
            if group.get("type_name") == "RegionGroup":
                self.groups.append(SPGroup(group))


class SPGroup:
    """Capsulated a "RegionGroup" struct.

    Parameters
    -------------
    xmlgroup: xml
        Group data by xml

    Attributes
    ------------
    name: text
        Group name

    regions: list
        List object stores SPRegion object

    """

    def __init__(self, xmlgroup) -> None:
        """Initialization.
        
        Parameters
        -------------
        xmlgroup: xml
            Group data by xml
        
        """
        self.name = xmlgroup[0].text
        self.regions = []
        for region in xmlgroup[1]:
            if region.get("type_name") == "RegionData":
                self.regions.append(SPRegion(region))


class SPRegion:
    """Capsulated a "RegionData" struct.

    Parameters
    ----------
    xmlregion: xml
        Region data by xml

    Attributes
    -----------
    name: str
        region name

    param: dictionary
        dictionary object stores measurement parameters

    mcd_head_tail: tuple
        value of mcd head and tail

    analyer_info: dictionary
        dictionary object stores name and dispersion element  for detector

    rawcounts: numpy.ndarray
        row count. 4-D array. rawcounts[scan#][detector_ch#][angle#][energy#]

    arpes: numpy.ndarray
        2D mapping data for ARPES

    energy_axis:numpy.ndarray

    energy_axis_ch:numpy.ndarray
        energy axis for each detector.
        energy_axis_ch[detector_ch] returns the np.array of the energy axis.

    angle_degs: numpy.ndarray
        angle axis of the data. Starts with zero and ends with the value
        of OrdinateRange

    """

    def __init__(self, xmlregion) -> None:
        """Initialization.
        
        Parameters
        ------------
        xmlregion: xml
            Region data
        """
        self.xmlregion = xmlregion
        self.name = xmlregion[0].text
        self.param = {}
        for elm in xmlregion[1]:
            if elm.get("name") == "scan_mode":
                self.param[elm.get("name")] = elm[0].text
            elif elm.get("name") in [
                "num_scans",
                "curves_per_scan",
                "values_per_curve",
            ]:
                self.param[elm.get("name")] = int(elm.text)
            else:
                try:
                    self.param[elm.get("name")] = float(elm.text)
                except ValueError:
                    self.param[elm.get("name")] = elm.text
        num_angles = self.param["curves_per_scan"]
        self.mcd_head_tail = (int(xmlregion[2].text), int(xmlregion[3].text))
        self.analyzer_info = {}
        analyzer = xmlregion.find('.//struct[@type_name="AnalyzerInfo"]')
        self.analyzer_info["name"] = analyzer[0].text
        detectors = xmlregion.find('.//sequence[@type_name="DetectorSeq"]')
        self.analyzer_info["Detector"] = np.array(
            [
                [float(elm2.text) for elm2 in elm if elm2.tag == "double"]
                for elm in detectors
            ]
        )
        num_detectors = len(self.analyzer_info["Detector"])
        counts_tag = './/ulong[@type_name="Counts"]'
        counts = np.array(
            [
                [int(count) for count in elm.text.split()]
                for elm in xmlregion.findall(counts_tag)
            ]
        )
        # self.rawcount[scan#][ch#][angle#][energy#]
        self.rawcounts = counts.reshape(
            self.param["num_scans"],
            num_angles,
            self.param["values_per_curve"]
            + self.mcd_head_tail[0]
            + self.mcd_head_tail[1],
            num_detectors,
        ).transpose(0, 3, 1, 2)
        # energy_axis_ch
        # E_{0n} =E_0+s_n =E1–h*delta+sn
        E1 = self.param["kinetic_energy"]
        mcdhead = self.mcd_head_tail[0]
        delta = self.param["scan_delta"]
        # sn = dn * pass_energy
        #    = self.analyzer_info['Detector'][n][1] * self.param['pass_energy']

        # en = sn + (self.values_per_curve + self.mcd_head_tail[0] +
        # self.mcd_head_tail[1] -1) * self.param['scan_delta']
        # values_per_curve+
        # np.linspace(sn, en
        self.energy_axis = np.array(
            [E1 + delta * i for i in range(self.param["values_per_curve"])]
        )
        # energy_axis_ch would be local before release
        self.energy_axis_ch = np.array(
            [
                [
                    E1
                    - mcdhead * delta
                    + self.analyzer_info["Detector"][i][1] * self.param["pass_energy"]
                    + delta * j
                    for j in range(
                        self.param["values_per_curve"]
                        + self.mcd_head_tail[0]
                        + self.mcd_head_tail[1]
                    )
                ]
                for i in range(num_detectors)
            ]
        )

        # Most cases, the required data is
        # * angle resolved
        #  but
        # summing up each detector data and each scan
        scan_integrated = np.sum(self.rawcounts, axis=0)
        apportioned = []
        for channel, data in enumerate(scan_integrated):
            interp_f = interpolate.interp1d(
                self.energy_axis_ch[channel],
                data,
                bounds_error=False,
                fill_value="extrapolate",
            )
            # Note: As broadcast technique in interp1d is used, the
            # intensity at the highest energy is a little bit different
            # from that in the output from SpecsLab originally.
            apportioned.append(interp_f(self.energy_axis))
        apportioned = np.array(apportioned)
        self.arpes = np.sum(apportioned, axis=0)
        for elm in xmlregion.findall(".//string[@name='name']"):
            if elm.text == "OrdinateRange":
                parent = elm.getparent()
                anglespan = float(
                    parent.find(".//any[@name='value']").find(".//double").text
                )
                self.angle_degs = np.linspace(0, anglespan, num=num_angles)

    def make_arpesmap(self):
        """Make APRESmap object.

        Returns
        --------
        ARPESmap: arpes.ARPESMap object

        """
        arpes_data = arpes.ARPESmap()
        arpes_data.intensities = self.arpes
        arpes_data.energy_axis = self.energy_axis
        arpes_data.second_axis = self.angle_degs
        arpes_data.second_axis_name = "Angle  (Degree)"
        return arpes_data


def load(splab_xml: str):
    """Load Splab xml file to make SPLab object.

    Parameters
    -----------
    splab_xml: str
        Filename of SPLab xml file. Bzipped file is acceptable

    """
    if os.path.splitext(splab_xml)[1] == ".bz2":
        try:
            xml = bz2.open(splab_xml, mode="rt")
        except AttributeError:
            xml = bz2.BZ2File(splab_xml, mode="r")  # Not teseted
    else:
        xml = open(splab_xml)
    splab = SPLab(xml)
    return splab
