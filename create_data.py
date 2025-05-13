import numpy as np
import pandas as pd
import anndata as ad

def create_synthetic_data(
    n_genes=50,
    n_control_cells=40,
    n_drugs=6,
    dosages_per_drug=3,
    cells_per_condition=50,
    n_cell_types=30,
    cell_type_embed_dim=50,
    drug_embed_dim=50,
):
    """
    Creates a synthetic AnnData object with multiple dosages per drug.

    Parameters
    ----------
    n_genes : int
        Number of genes to simulate
    n_control_cells : int
        Number of control cells per cell type
    n_drugs : int
        Total number of distinct drugs
    dosages_per_drug : int
        Number of different dosages for each drug
    cells_per_condition : int
        Number of cells per drug-dosage condition
    n_cell_types : int
        Number of cell types
    cell_type_embed_dim : int
        Embedding dimension for cell types
    drug_embed_dim : int
        Embedding dimension for drugs

    Returns
    -------
    dict
        Dictionary containing all DataManager parameters
    """

    # Create cell type names
    n_batches = n_cell_types
    cell_type_names = [f"cell_line_{chr(97 + i)}" for i in range(n_cell_types)]
    batch_names = [f"batch_{i+1}" for i in range(n_batches)]  # New: create batch names

    # Calculate total cells
    total_conditions = n_drugs * dosages_per_drug  # Total conditions excluding control
    total_cells_per_type = n_control_cells + (total_conditions * cells_per_condition)
    n_cells = n_cell_types * total_cells_per_type

    # Initialize lists for observation data
    cell_type_list = []
    control_list = []
    drug_list = []
    dosage_list = []
    batch_list = []

    # Generate data for each cell type
    # shuffle batch_names
    batch_names = np.random.permutation(batch_names)

    for i,cell_type in enumerate(cell_type_names):
        # Add control cells for this cell type
        cell_type_list.extend([cell_type] * total_cells_per_type)
        # Controls
        control_list.extend([True] * n_control_cells)
        drug_list.extend(["control"] * n_control_cells)
        dosage_list.extend([0.0] * n_control_cells)
        # batch_assignments = np.random.choice(batch_names[i], size=total_cells_per_type)
        batch_list.extend([batch_names[i]] * total_cells_per_type)
        # ensure that at lease one type is present 


        # Add perturbed cells for each drug-dosage combination
        control_list.extend([False] * (total_conditions * cells_per_condition))

        # Add drug-dosage combinations
        for drug_idx in range(1, n_drugs + 1):
            for dosage_idx in range(1, dosages_per_drug + 1):
                # Calculate dosage value (e.g., 0.1, 0.5, 1.0)
                dosage_value = dosage_idx / dosages_per_drug  # Normalize to [0,1] range

                # Add this drug-dosage combination
                drug_list.extend([f"drug{drug_idx}"] * cells_per_condition)
                dosage_list.extend([dosage_value] * cells_per_condition)

    # Generate random expression data
    X = np.random.normal(size=(n_cells, n_genes))

    # Create observation DataFrame
    obs = pd.DataFrame(
        {
            "control": control_list,
            "cell_type": pd.Categorical(cell_type_list),
            "drug": pd.Categorical(drug_list),
            "dosage": dosage_list,
            "batch": pd.Categorical(batch_list),
        }
    )



    # Create AnnData object
    adata = ad.AnnData(X, obs=obs)

    # Add representations to uns (for covariate embeddings)
    adata.uns["drug"] = {
        "control": np.zeros(drug_embed_dim),
    }

    # Add drug embeddings
    for i in range(1, n_drugs + 1):
        adata.uns["drug"][f"drug{i}"] = np.random.normal(size=(drug_embed_dim,))

    # Add cell type embeddings
    adata.uns["cell_type"] = {}
    adata.uns["batch"] = {}
    for cell_type in cell_type_names:
        adata.uns["cell_type"][cell_type] = np.random.normal(
            size=(cell_type_embed_dim,)
        )
    for batch in batch_names:
        adata.uns["batch"][batch] = np.random.normal(
            size=(cell_type_embed_dim,)
        )

    # Define parameters for DataManager
    sample_rep = "X"
    control_key = "control"
    split_covariates = ["cell_type","batch"]

    # Here we use a simpler structure with just one drug and dosage column
    perturbation_covariates = {"drug": ["drug"], "dosage": ["dosage"]}
    perturbation_covariate_reps = {"drug": "drug"}
    sample_covariates = ["cell_type", "batch"]
    sample_covariate_reps = {"cell_type": "cell_type", "batch": "batch"}



    # Return a dictionary with all required parameters
    return {
        "adata": adata,
        "sample_rep": sample_rep,
        "control_key": control_key,
        "split_covariates": split_covariates,
        "perturbation_covariates": perturbation_covariates,
        "perturbation_covariate_reps": perturbation_covariate_reps,
        "sample_covariates": sample_covariates,
        "sample_covariate_reps": sample_covariate_reps,
    }

if __name__ == "__main__":
    cells_per_condition = 200
    data = create_synthetic_data(cells_per_condition=cells_per_condition)
    print(data)
    adata = data["adata"]
    row_chunks = 5
    adata.write_zarr("benchmarks/data/synthetic_data.zarr")