import splitfolders

input_folder = 'C:\\Users\\user\\Desktop\\firstModel\\data'

# Split with a ratio and use group_prefix to avoid duplicate images in different sets.
splitfolders.ratio(input_folder, output="modelData", 
                   seed=42, ratio=(.7, .2, .1),
                   )  # Use a custom group_prefix value, e.g., 'group'

# Split val/test with a fixed number of items and use group_prefix to avoid duplicate images in different sets.
splitfolders.fixed(input_folder, output="modelData", 
                   seed=42, fixed=(35, 20), 
                   oversample=False)  # Use a custom group_prefix value, e.g., 'group'
