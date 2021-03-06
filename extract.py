import os, os.path
import numpy

def extract_to_txt(base_dir):
    for name in ["polarizability_df.npz",
                 "polarizability_tetra.npz"]:
        fname = os.path.join(base_dir, name)
        if os.path.exists(fname):
            print("Found {}".format(fname))
            f = numpy.load(fname)
            freq = f["frequencies"]
            alphax = f["eps_x"]
            alphay = f["eps_y"]
            alphaz = f["eps_z"]
            numpy.savetxt(os.path.join(base_dir,
                                       name.replace("_", "_x_imag_").replace(".npz", ".txt")),
                          X=numpy.vstack([freq, alphax.imag]).T,
                          header="Freq (eV); Imaginary alpha x (AA)")
            numpy.savetxt(os.path.join(base_dir,
                                       name.replace("_", "_y_imag_").replace(".npz", ".txt")),
                          X=numpy.vstack([freq, alphay.imag]).T,
                          header="Freq (eV); Imaginary alpha y (AA)")
            numpy.savetxt(os.path.join(base_dir,
                                       name.replace("_", "_z_imag_").replace(".npz", ".txt")),
                          X=numpy.vstack([freq, alphaz.imag]).T,
                          header="Freq (eV); Imaginary alpha z (AA)")
            
            numpy.savetxt(os.path.join(base_dir,
                                       name.replace("_", "_x_real_").replace(".npz", ".txt")),
                          X=numpy.vstack([freq, alphax.real]).T,
                          header="Freq (eV); real alpha x (AA)")
            numpy.savetxt(os.path.join(base_dir,
                                       name.replace("_", "_y_real_").replace(".npz", ".txt")),
                          X=numpy.vstack([freq, alphay.real]).T,
                          header="Freq (eV); real alpha y (AA)")
            numpy.savetxt(os.path.join(base_dir,
                                       name.replace("_", "_z_real_").replace(".npz", ".txt")),
                          X=numpy.vstack([freq, alphaz.real]).T,
                          header="Freq (eV); Real alpha z (AA)")
            f.close()


if __name__ == "__main__":
    root_dir = "/cluster/scratch/ttian/bulk/"
    for directory in os.listdir(root_dir):
        base_dir = os.path.join(root_dir, directory)
        extract_to_txt(base_dir)
        
