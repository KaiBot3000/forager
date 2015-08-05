"""Utility file to seed unprocessed tree database from Friends of the Urban Forest"""

from fuf_model import Tree, Plot, Specie, connect_to_db, db
from server import app


def load_trees():
    """Load trees into database."""
    
    f = open("fuf_trees_trimmed")

    for line in f:
        split_line = line.rstrip().split()
        new_tree = Tree(user_id=split_line[0], 
			        	tree_species_id=split_line[2], 
			        	tree_plot_id=split_line[1])
        db.session.add(new_tree)

    db.session.commit()

def load_species():
    """Load species into database."""
    
    f = open("fuf_species_trimmed")

    for line in f:
        split_line = line.rstrip().split()
        new_species = Specie(species_id=split_line[0], 
			        	scientific_name=split_line[1],
			        	common_name=split_line[2],
			        	fruit_period=split_line[4])
        db.session.add(new_species)

    db.session.commit()

def load_plots():
    """Load plots into database."""
    
    f = open("fuf_plots_trimmed")

    for line in f:
        split_line = line.rstrip().split()
        new_plot = Plot(plot_id=split_line[1], 
			        	wkt=split_line[0],
			        	address_street=split_line[2],
			        	address_geocoded=split_line[3],
			        	lat_geocoded=split_line[4],
			        	lon_geocoded=split_line[5])
        db.session.add(new_plot)

    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)