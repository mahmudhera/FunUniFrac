import subprocess
import numpy as np
import os
from scipy import sparse
import sparse
import data


def test_small_edge_lengths():
    """
    Uses a complete binary tree with 4 leaf nodes, all branch lengths set to 1
    :return: None
    """
    edge_list = data.get_data_abspath("small_edge_list_with_lengths.txt")
    profile1 = "small_sim_10_KOs_gather.csv"
    profile2 = "small_sim2_10_KOs_gather.csv"
    profile3 = "small_sim3_10_KOs_gather.csv"
    file_pattern_dir = data.get_data_abspath(".")
    out_file = data.get_data_abspath("test_output/pairwise_dists.npy")
    # remove the out file if it exists
    basis_file = f"{out_file}.basis.txt"
    brite = "ko00001"
    cmd = f"python ../scripts/compute_fununifrac.py -e {edge_list} -fd {file_pattern_dir} " \
        f" -o {out_file} --force -b {brite} -a median_abund"
    res = subprocess.run(cmd, shell=True, check=True)
    
    # check that the output file is correct
    pw_dists = np.load(out_file)
    # This has been computed by hand
    known_pw_dists = np.array([[0.0, 13/14, 10/21], [13/14, 0.0, 4/3], [10/21, 4/3, 0.0]])
    assert np.allclose(pw_dists, known_pw_dists, atol=1e-3)
    # check that the basis file has been created and is correct
    fun_files = []
    with open(basis_file, "r") as f:
        basis = os.path.basename(f.readline().strip())
        fun_files.append(basis)
        assert basis == os.path.basename(profile2)  # Q
        basis = os.path.basename(f.readline().strip())
        fun_files.append(basis)
        assert basis == os.path.basename(profile3)  # R
        basis = os.path.basename(f.readline().strip())
        fun_files.append(basis)
        assert basis == os.path.basename(profile1)  # P
        # check that the end of the file has been reached
        assert f.readline() == ""

    # now also check the diffabs
    cmd = f"python ../scripts/compute_fununifrac.py -e {edge_list} -fd {file_pattern_dir} " \
              f" -o {out_file} --force -b {brite} -a median_abund --diffab"
    res = subprocess.run(cmd, shell=True, check=True)
    # check that the output file exists
    diffab_out_file = data.get_data_abspath("test_output/pairwise_dists.npy.diffab.npz")
    basis_file = f"{out_file}.basis.txt"
    # check that the output file is correct
    pw_dists = np.load(out_file)
    # This has been computed by hand
    known_pw_dists = np.array([[0.0, 13/14, 10/21], [13/14, 0.0, 4/3], [10/21, 4/3, 0.0]])
    assert np.allclose(pw_dists, known_pw_dists, atol=1e-3)
    # check that the basis file has been created and is correct
    fun_files = []
    with open(basis_file, "r") as f:
        basis = os.path.basename(f.readline().strip())
        fun_files.append(basis)
        assert basis == os.path.basename(profile2)  # Q
        basis = os.path.basename(f.readline().strip())
        fun_files.append(basis)
        assert basis == os.path.basename(profile3)  # R
        basis = os.path.basename(f.readline().strip())
        fun_files.append(basis)
        assert basis == os.path.basename(profile1)  # P
        # check that the end of the file has been reached
        assert f.readline() == ""
    # Check that the diffabs file is correct
    diffabs = sparse.load_npz(diffab_out_file)
    known_diffab = np.array([-1/14, -1/21, -5/42, 5/42, 0, 5/42, 0])
    zeros = np.zeros_like(known_diffab)
    vec = diffabs[0, 2, :].todense()
    assert np.allclose(vec, known_diffab, atol=1e-3)
    vec = diffabs[2, 0, :].todense()
    assert np.allclose(vec, - known_diffab, atol=1e-3)
    vec = diffabs[0, 0, :].todense()
    assert np.allclose(vec, zeros, atol=1e-3)
    vec = diffabs[1, 1, :].todense()
    assert np.allclose(vec, zeros, atol=1e-3)

def test_diffab_order():
    edge_list = data.get_data_abspath("small_edge_list_with_lengths.txt")
    profile1 = "small_sim_10_KOs_gather.csv"  # P
    profile2 = "small_sim2_10_KOs_gather.csv"  # Q
    profile3 = "small_sim3_10_KOs_gather.csv"  # R
    file_pattern_dir = data.get_data_abspath(".")
    out_file = data.get_data_abspath("test_output/pairwise_dists.npy")
    brite = "ko00001"
    cmd = f"python ../scripts/compute_fununifrac.py -e {edge_list} -fd {file_pattern_dir} " \
          f"-o {out_file} --force -b {brite} -a median_abund --diffab"
    res = subprocess.run(cmd, shell=True, check=True)
    
    # file paths
    basis_file = f"{out_file}.basis.txt"
    diffab_out_file = data.get_data_abspath("test_output/pairwise_dists.npy.diffab.npz")
    diffabs = sparse.load_npz(diffab_out_file)
    fun_files = []
    with open(basis_file, "r") as f:
        basis = os.path.basename(f.readline().strip())
        fun_files.append(basis)
        assert basis == os.path.basename(profile2)  # Q
        basis = os.path.basename(f.readline().strip())
        fun_files.append(basis)
        assert basis == os.path.basename(profile3)  # R
        basis = os.path.basename(f.readline().strip())
        fun_files.append(basis)
        assert basis == os.path.basename(profile1)  # P
        # check that the end of the file has been reached
        assert f.readline() == ""
    known_diffab_PQ = np.array([1/14, 1/21, 5/42, -5/42, 0, -5/42, 0])
    known_diffab_QP = - np.array([1/14, 1/21, 5/42, -5/42, 0, -5/42, 0])
    known_diffab_PR = np.array([1/4, 1/12, 1/3, -1/12, -1/4, -1/3, 0])
    known_diffab_RP = - np.array([1 / 4, 1 / 12, 1 / 3, -1 / 12, -1 / 4, -1 / 3, 0])
    known_diffab_QR = np.array([5/28, 1/28, 3/14, 1/28, -1/4, -3/14, 0])
    known_diffab_RQ = - np.array([5 / 28, 1 / 28, 3 / 14, 1 / 28, -1 / 4, -3 / 14, 0])
    known_diffab_ii = np.zeros_like(known_diffab_PQ)
    # basis is [Q, R, P]
    vec = diffabs[0, 1, :].todense()
    assert np.allclose(vec, known_diffab_QR, atol=1e-3)
    vec = diffabs[1, 0, :].todense()
    assert np.allclose(vec, known_diffab_RQ, atol=1e-3)
    vec = diffabs[0, 0, :].todense()
    assert np.allclose(vec, known_diffab_ii, atol=1e-3)
    vec = diffabs[1, 1, :].todense()
    assert np.allclose(vec, known_diffab_ii, atol=1e-3)
    vec = diffabs[0, 2, :].todense()
    assert np.allclose(vec, known_diffab_QP, atol=1e-3)
    vec = diffabs[2, 0, :].todense()
    assert np.allclose(vec, known_diffab_PQ, atol=1e-3)
    vec = diffabs[1, 2, :].todense()
    assert np.allclose(vec, known_diffab_RP, atol=1e-3)
    vec = diffabs[2, 1, :].todense()
    assert np.allclose(vec, known_diffab_PR, atol=1e-3)
    vec = diffabs[2, 2, :].todense()
    assert np.allclose(vec, known_diffab_ii, atol=1e-3)


def test_small_edge_lengthsL2():
    """
    Uses a complete binary tree with 4 leaf nodes, all branch lengths set to 1
    :return: None
    """
    edge_list = data.get_data_abspath("small_edge_list_with_lengths.txt")
    profile1 = "small_sim_10_KOs_gather.csv"
    profile2 = "small_sim2_10_KOs_gather.csv"
    profile3 = "small_sim3_10_KOs_gather.csv"
    file_pattern_dir = data.get_data_abspath(".")
    out_file = data.get_data_abspath("test_output/pairwise_dists.npy")
    brite = "ko00001"
    # command
    cmd = f"python ../scripts/compute_fununifrac.py -e {edge_list} -fd {file_pattern_dir} " \
          f"-o {out_file} --force -b {brite} -a median_abund --L2"
    res = subprocess.run(cmd, shell=True, check=True)
    
    # data paths
    basis_file = f"{out_file}.basis.txt"
    # check that the output file is correct
    pw_dists = np.load(out_file)
    # This has been computed by hand
    known_pw_dists = np.array([[0.0, np.sqrt(37)/14, np.sqrt(22)/21], [np.sqrt(37)/14, 0.0, np.sqrt(13)/6],
                               [np.sqrt(22)/21, np.sqrt(13)/6, 0.0]])**2
    assert np.allclose(pw_dists, known_pw_dists, atol=1e-3)
    # open the basis file
    fun_files = []
    with open(basis_file, "r") as f:
        basis = os.path.basename(f.readline().strip())
        fun_files.append(basis)
        assert basis == os.path.basename(profile2)  # Q
        basis = os.path.basename(f.readline().strip())
        fun_files.append(basis)
        assert basis == os.path.basename(profile3)  # R
        basis = os.path.basename(f.readline().strip())
        fun_files.append(basis)
        assert basis == os.path.basename(profile1)  # P
        # check that the end of the file has been reached
        assert f.readline() == ""

    diffab_out_file = data.get_data_abspath("test_output/pairwise_dists.npy.diffab.npz")
    basis_file = f"{out_file}.basis.txt"
    out_file = data.get_data_abspath("test_output/pairwise_dists.npy")
    
    # command
    cmd = f"python ../scripts/compute_fununifrac.py -e {edge_list} -fd {file_pattern_dir} " \
              f"-o {out_file} --force -b {brite} -a median_abund --diffab --L2"
    res = subprocess.run(cmd, shell=True, check=True)
    
    # check that the output file exists
    data.check_data_abspath(basis_file)
    data.check_data_abspath(diffab_out_file)
    data.check_data_abspath(out_file)
    
    # check that the output file is correct
    pw_dists = np.load(out_file)
    # This has been computed by hand
    known_pw_dists = np.array([[0.0, np.sqrt(37) / 14, np.sqrt(22) / 21], [np.sqrt(37) / 14, 0.0, np.sqrt(13) / 6],
                               [np.sqrt(22) / 21, np.sqrt(13) / 6, 0.0]]) ** 2
    assert np.allclose(pw_dists, known_pw_dists, atol=1e-3)
    # open the basis file
    fun_files = []
    with open(basis_file, "r") as f:
        basis = os.path.basename(f.readline().strip())
        fun_files.append(basis)
        assert basis == os.path.basename(profile2)  # Q
        basis = os.path.basename(f.readline().strip())
        fun_files.append(basis)
        assert basis == os.path.basename(profile3)  # R
        basis = os.path.basename(f.readline().strip())
        fun_files.append(basis)
        assert basis == os.path.basename(profile1)  # P
        # check that the end of the file has been reached
        assert f.readline() == ""
    #diffabs = np.load(diffab_out_file)
    diffabs = sparse.load_npz(diffab_out_file)
    # QP diffab
    known_diffab = np.array([1/196, 1/441, 25/1764, 25/1764, 0, 25/1764, 0])
    zeros = np.zeros_like(known_diffab)
    nodes_in_order = [0, 1, 2, 3, 4, 5, 6]
    vec = diffabs[0, 2, :].todense()
    assert np.allclose(vec, known_diffab, atol=1e-3)
    vec = diffabs[2, 0, :].todense()
    assert np.allclose(vec, - known_diffab, atol=1e-3)
    vec = diffabs[0, 0, :].todense()
    assert np.allclose(vec, zeros, atol=1e-3)
    vec = diffabs[1, 1, :].todense()
    assert np.allclose(vec, zeros, atol=1e-3)