import pandas as pd
import shutil
import os
import gzip
import argparse
import sys

def copy_files_and_decompress(tsv_file, run_num, destination_folder):
    # Leer el archivo TSV
    df = pd.read_csv(tsv_file, sep='\t')

    # Asegúrate de que la carpeta de destino existe
    os.makedirs(destination_folder, exist_ok=True)

    for index, row in df.iterrows():
        # Obtener el absolute_path del archivo
        absolute_path = row.iloc[1]  # Cambia el índice si la columna está en otra posición

        # Copiar el archivo a la carpeta de destino
        if os.path.exists(absolute_path):
            filename = os.path.basename(absolute_path)
            
            if not os.path.exists(os.path.join(destination_folder,'data_run'+run_num)):
                os.mkdir(os.path.join(destination_folder,'data_run'+run_num))

            dest_path = os.path.join(destination_folder,'data_run'+run_num, filename)

            shutil.copy2(absolute_path, dest_path)
            print(f'Preparing: {absolute_path}')

            # Si el archivo es .fastq.gz, descomprimirlo
            if absolute_path.endswith('.fastq.gz'):
                with gzip.open(dest_path, 'rb') as f_in:
                    with open(dest_path[:-3], 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                print(f'Decompressing: {dest_path[:-3]}')
                
                # Eliminar el archivo .gz
                os.remove(dest_path)  # Eliminar el archivo .gz
                print(f'Removing: {dest_path}')

        else:
            print(f'File not found: {absolute_path}')

def write_manifest_file(directory, manifest_file):
    """This function writes a manifest file for the fastq.gz files in a specific directory"""
    with open(manifest_file, "w") as man_f:
        man_f.write("sample-id\tabsolute-filepath\n")
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".fastq"):
                    filepath = os.path.join(root, file)
                    filename = os.path.basename(filepath).replace(".fastq", "")
                    absolute_path = os.path.abspath(filepath)
                    man_f.write(f"{filename}\t{absolute_path}\n")

def generate_manifest_files(data_dir, run, manifest_file):
    """This function generates a manifest file for fastq.gz files in the specified run directory."""
    
    # To verify that the directory data_dir exists.
    if not os.path.isdir(data_dir):
        print(f"The directory {data_dir} does not exist.")
        sys.exit(1)

    # Build the run directory path
    run_dir = os.path.join(data_dir, f"data_run{run}")
    
    # Check if the specified run directory exists
    if os.path.isdir(run_dir):
        write_manifest_file(run_dir, manifest_file)
        print(f"Manifest file created at: {manifest_file}")
    else:
        print(f"The run directory {run_dir} does not exist.")
        sys.exit(1)

# if __name__ == "__main__":
#     # Replace the following with actual arguments or use snakemake inputs if applicable
#     data_dir = "ruta/a/tu/directory"  # Cambia esto a la ruta de tu directorio
#     run = "run1"  # Cambia esto al run que deseas especificar
#     manifest_file = "ruta/a/tu/manifest.tsv"  # Cambia esto a la ruta donde deseas guardar el manifest

#     generate_manifest_files(data_dir, run, manifest_file)



if __name__ == '__main__':


    parser = argparse.ArgumentParser(description='Reorganize fastq.gz files by run')
    parser.add_argument('manifest_tsv_file', type=str, help='Manifest tsv file by run')
    parser.add_argument('run', type=str, help='Run number')
    parser.add_argument('destination_folder', type=str, help='Path to folder where files will be organized by run')
    
    args = parser.parse_args()

    manifest_file= os.path.join(args.destination_folder, f"manifest_data_run{args.run}.txt")

    copy_files_and_decompress(args.manifest_tsv_file, args.run,  args.destination_folder)
    generate_manifest_files(args.destination_folder,  args.run, manifest_file)


