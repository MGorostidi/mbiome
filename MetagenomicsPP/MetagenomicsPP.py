#!/usr/bin/env python
from __future__ import print_function

from ion.plugin import *
import re 
import json
import os


scriptdir = os.path.dirname(os.path.realpath(__file__))

cutprimers = scriptdir + "/mgpp.sh"
header=['V2.FR', 'V3.FR', 'V4.FR', 'V67.FR', 'V8.FR', 'V9.FR', 'noadapter','total']

block_file='MetagenomicsPP_block.html'

COLDRUN = False

def sanitaze_name(name):
    trim=name.strip()
    p=re.compile(' |\t|\*|&')
    no_spaces=p.sub("_",trim)
    return no_spaces

def run(*args):
    if COLDRUN:
        return -1
    else:
        cmd=" ".join(args)
        #print(cmd)
        return os.system(cmd)

class MetagenomicsPP(IonPlugin):
    "Metagenomics Post Processor"
    version = '2.1.14'

    def __init__(self):
        print("Script dir '" + scriptdir + "'")
        self.matrix={}
        IonPlugin.__init__(self)

    def load_env(self):
        self.env = dict(os.environ)

    def load_barcodes(self):
        with open('barcodes.json') as fin:
            self.barcodes = json.load(fin)

    def readStatus(self,sample,barcode,path):
        print("readStatus:",sample,barcode,path)
        self.matrix[barcode]={}
        with open(path,"r") as f:
            for line in f:
                xs=line.strip().split("\t")
                if len(xs)>=2:
                    c=int(xs[1])
                    m=re.search(r"\.(V.*?|noadapter|total)\.fastq$",xs[0])
                    p=m.group(1) if m else xs[0]
                    self.matrix[barcode][p]=(sample,c)

    def analyzeBAM(self,bam,outputdir,barcode,sample):
        sample_name=sanitaze_name(sample)
        print('\t'.join([barcode,sample_name,bam]))
        ret = run(cutprimers,
                "-s",sample_name,
                "-o",outputdir,
                "-i",bam)
        print("Ret = " + str(ret))
        self.readStatus(sample_name,barcode,outputdir + "/" + sample_name + "/counts.txt")
        return ret

    def write_table(self):
        print(self.matrix)
        with open("results_table.tsv","w") as f:
            print("barcode",end="\t",file=f)
            print("sample",end="\t",file=f)
            for i in header:
                print(i,end="\t",file=f)
            print("",file=f)
            barcodes=list(self.matrix.keys())
            barcodes.sort()
            for barcode in barcodes:
                print(barcode,end="\t",file=f)
                m=self.matrix[barcode]
 
                print(m[header[0]][0],end="\t",file=f)
                for i in header:
                    if m.has_key(i):
                        x=m[i]
                    else:
                        x=[i,0] 

                    print(x[1],end="\t",file=f)
                print("",file=f)

    def launch(self,data=None):
        if not os.path.isfile(cutprimers):
            raise RuntimeError("Script {0} not found".format(cutprimers))

        #self.load_startplugin()
        self.load_barcodes()
        print("Metagenomics")
        #print(json.dumps(self.startplugin,indent=4))
        self.url=self.startplugin['runinfo']['url_root']
        self.pluginresult=self.startplugin['runinfo']['pluginresult']

        outputdir=sanitaze_name(self.startplugin['expmeta']['results_name'])
        self.i=1
        self.n=len(self.barcodes)
        for k in self.barcodes:
            self.barcode_num=k
            self.block_update()
            barcode=self.barcodes[k]
            bam=barcode['bam_filepath']
            sample=barcode['sample']
            ret=self.analyzeBAM(bam,outputdir,k,sample)
            self.i+=1
        
        self.write_table()

        self.block_zip()
        self.zipfile=outputdir+".split_primers.zip"
        run("zip","-r",self.zipfile,outputdir)
        if os.path.isfile(self.zipfile):
            self.block_output()
            return -1
        else:
            return 0

    def block_update(self):
        with open(block_file,'w') as out:
            out.write('<div>')
            out.write("Processing Barcode %s (%d/%d)" % (self.barcode_num,self.i,self.n))
            out.write('</div>')

    def block_zip(self):
        with open(block_file,'w+') as out:
            out.write('<div>')
            out.write("Zipping...")
            out.write('</div>')

    def block_output(self):
        with open(block_file,'w+') as out:
            out.write('<p style="font-size:large">\n')
            out.write("<span>Reads Splitted by primers:</span> <a href='%s/plugin_out/MetagenomicsPP_out.%d/%s'>%s</a>" % (self.url,
                                                                                        self.pluginresult,
                                                                                        self.zipfile,
                                                                                        self.zipfile))
            
            out.write("</p>")

            out.write('<p style="font-size:large">\n')
            out.write("<span>Read Counts Table:</span> <a href='%s/plugin_out/MetagenomicsPP_out.%d/%s'>%s</a>" % (self.url,
                                                                                        self.pluginresult,
                                                                                        "results_table.tsv",
                                                                                        "results_table.tsv"))
            
            out.write("</p>")

            out.write("""
<p><table class='metagenomics'>
<style scoped>
    table {
        border-collapse: collapse;
    }
    th {
    padding: 10px;
    border: 1px blue solid;
    border-margin: 0px;
    }
    td {
        border: 1px black solid;
        padding: 10px;
        text-align: right;
    }
    .top th {
        text-align: right;
    }
    th.left {
    text-align: left;
    }
</style>
            """)

            out.write("<tr><th>Barcode</th>")
            out.write("<th>Sample</th>")
            for i in header: 
                out.write("<th colspan='2'>{0}</th>".format(i))
            out.write("</tr>\n")

            barcodes=list(self.matrix.keys())
            barcodes.sort()
            for barcode in barcodes:
                out.write("<tr>\n")
                out.write("<th class='left'>{0}</th>".format(barcode))
                m=self.matrix[barcode]
                out.write("<th class='left'>{0}</th>".format(m[i][0]))
                for i in header:
                    if m.has_key(i):
                        val=m[i][1]
                    else:
                        val=0
                    out.write("<td>{:,}</td>".format(val))
                    if i!="total":
                        out.write("<td>{:.1f}%</td>".format(val*100.0/m["total"][1]))
                out.write("</tr>\n")

            out.write("</table>\n")

            out.write('</p>\n')

if __name__ == '__main__': PluginCLI()
