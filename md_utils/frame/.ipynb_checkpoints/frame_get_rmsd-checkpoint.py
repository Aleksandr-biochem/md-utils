{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "1c729e79",
   "metadata": {},
   "outputs": [],
   "source": [
    "from pyxmolpp2 import Frame, AtomPredicate, calc_rmsd\n",
    "from select import get_sec_str_residues_predicate\n",
    "import numpy as np\n",
    "import sys\n",
    "\n",
    "def frame_get_rmsd(reference_frame: Frame,\n",
    "              probe_frame: Frame,\n",
    "              by_atoms: AtomPredicate,\n",
    "              ) -> float:\n",
    "    \"\"\"\n",
    "    Comparison similarity in teo three-dimensional structures by the RMSD after optimal rigid body superposition\n",
    "    https://en.wikipedia.org/wiki/Root-mean-square_deviation_of_atomic_positions\n",
    "\n",
    "    :param reference_frame: for example X-ray structure or any other case\n",
    "    :param probe_frame: for example frame from MD trajectory or any other case\n",
    "    :param by_atoms: rigid body superposition is carried out by this atoms. In case of proteins,\n",
    "                     this often calculated for the secondary-structure Cα atoms.\n",
    "    :return: rmsd value by_atoms between reference_frame and probe_frame\n",
    "    \"\"\"\n",
    "    # Extract frames by predicates from reference and probe structures\n",
    "    reference = reference_frame.atoms.frame(by_atoms)\n",
    "    probe = probe_frame.atoms.frame(by_atoms)\n",
    "    \n",
    "    # Similarity estimation by residue - correlation matrix\n",
    "    prob_ref_alignment = probe.alignment_to(reference)\n",
    "    \n",
    "    # Obtain new coordinates considering alignment\n",
    "    imposition = np.dot(probe.coords.values, prob_ref_alignment.matrix3d().T) + prob_ref_alignment.vector3d().values\n",
    "    \n",
    "    return calc_rmsd(reference.coords.values, impositions)\n",
    "\n",
    "\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    from pyxmolpp2 import PdbFile\n",
    "    p1 = sys.args[1]\n",
    "    p2 = sys.args[2]\n",
    "    \n",
    "    ref = PdbFile(p1).frames()[0]\n",
    "    target = PdbFile(p2).frames()[0]\n",
    "    pred = get_sec_str_residues_predicate(frame=ref, molnames=[\"B\"])\n",
    "    \n",
    "    print(get_rmsd(ref, target, pred))"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.10"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}