def iter_cif(handle, model_id: int, chain_id: str):
    yield 0, '#\n'
    yield 0, 'loop_\n'
    # Initialize headers
    columns = dict()
    # Header flag
    atom_site_visited = False
    # Loop through each line
    for line in handle:
        # Handle end of _atom_site loop
        if atom_site_visited and line[0] == '#':
            break
        # Handle start of _atom_site loop
        if line.startswith('_atom_site.'):
            # Get column name
            col_name = line.split('.')[1].strip()
            # Map key -> index
            columns.setdefault(col_name, len(columns))
            # Change visited flag
            atom_site_visited = True
            # Yield current line
            yield 0, line
        # Handle core of the _atom_site block
        elif atom_site_visited:
            # Split columns
            components = line.split()
            # Define index for chain identifier
            chain_ix = columns.get('auth_asym_id', columns.get('label_asym_id', -1))
            # Define index form model identifier
            model_ix = columns.get('pdbx_PDB_model_num', -1)
            # Get model, chain
            curr_model, curr_chain = int(components[model_ix]), str(components[chain_ix])
            # Case model and chain match, return line
            if (model_id is None or curr_model == model_id) and (curr_chain == chain_id or chain_id is None):
                # model_id, chain_id = curr_model, curr_chain
                yield 1, line
            # Case model is passed, exit loop
            if model_id is not None and curr_model > model_id:
                break
    # Yield last line
    yield 0, '#\n'
