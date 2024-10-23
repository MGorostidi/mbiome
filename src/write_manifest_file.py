import os
import pandas as pd
import argparse

def writeManifestFiles(path_to_sorted_samples_byV,
                       output_path_manifest):
    
    def getFastqFiles(path):
        files = []
        v_regions = set()
        for root, dirs, filenames in os.walk(path):
            for file in filenames:
                if file[-6:].lower() == '.fastq' or file[-9:].lower() == '.fastq.gz':
                    files.append(os.path.join(root,file))
                    v_regions.add(root.split(os.sep)[-1])
        return [os.path.normpath(f) for f in files],v_regions

    ### write manifest files
    def writeRegionManifest(writeFile,filesNew,v,sep='\t'):  #tab:'\t' 
        # writeFile has two columns: first is the sample ID, next is the absolute path
        # of the file on the biowulf cluster
        files = [f for f in filesNew if v + '.' in f]
        fp = [(output_path_manifest+f).replace(os.sep,'/') for f in files]
        sID = [os.path.basename(f).split('.')[0] for f in files]    
        manifest = pd.DataFrame({'sample-id': sID, 'absolute-filepath': fp})
        manifest.to_csv(writeFile,index=False,sep=sep)
        print('\tManifest file written to {}'.format(manifestFile))
    
    ## execute functions
    filesNew,v_regions = getFastqFiles(path_to_sorted_samples_byV)
    # print(v_regions)
    for v in sorted(v_regions):
        manifestFile = os.path.join(path_to_sorted_samples_byV,'manifest_{}.txt'.format(v))
        writeRegionManifest(manifestFile,filesNew,v)
    print()
    
## If the lines below are not commented out, then the two functions will run automatically 
## based on user input
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Reorganize files by V region')
    parser.add_argument('path_to_sorted_samples_byV', type=str, help='Path to folder where files are organized by region')
    parser.add_argument('output_path_manifest', type=str, help='Path to folder where manifest files will be saved')
    
    args = parser.parse_args()

    writeManifestFiles(args.path_to_sorted_samples_byV,args.output_path_manifest)