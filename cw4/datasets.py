from collections import namedtuple

Dataset = namedtuple('Dataset', 'filepath columns')

bc_names = ['Class', 'age', 'menopause', 'tumor-size', 'inv-nodes', 'node-caps', 'deg-malig', 'breast', 'breast-quad',
            'irradiat']

bc_namesXD = ['Class', 'age', 'menopause', 'tumor-size', 'node-caps', 'deg-malig', 'breast', 'breast-quad',
            'irradiat']

bc_names_2 = ['Class', 'age', 'menopause', 'inv-nodes', 'node-caps', 'deg-malig', 'breast', 'breast-quad',
            'irradiat']

al_names = ['Class', 'cap-shape', 'cap-surface', 'cap-color', 'bruises?', 'odor', 'gill-attachment', 'gill-spacing',
            'gill-size',
            'gill-color', 'stalk-shape', 'stalk-root', 'stalk-surface-above-ring', 'stalk-surface-below-ring',
            'stalk-color-above-ring',
            'stalk-color-below-ring', 'veil-type', 'veil-color', 'ring-number', 'ring-type', 'spore-print-color',
            'population', 'habitat']
al_names2 = ['Class', 'cap-shape', 'cap-surface', 'cap-color', 'bruises?', 'gill-attachment', 'gill-spacing',
            'gill-size',
            'gill-color', 'stalk-shape', 'stalk-root', 'stalk-surface-above-ring', 'stalk-surface-below-ring',
            'stalk-color-above-ring',
            'stalk-color-below-ring', 'veil-type', 'veil-color', 'ring-number', 'ring-type', 'spore-print-color',
            'population', 'habitat']
lec_names = ['Class', 'x1', 'x2']

bc_file = 'data/breast-cancer.data'
bc_fileXD = 'data/bc_without_best_column.data'
bc_file_test = 'data/bc-test.data'
bc_file_test2 = 'data/bc-test.data2.data'

al_file = 'data/agaricus-lepiota.data'
al_file2 = 'data/Out_19.csv'
lec_file = 'data/lecture_example.data'

BC = Dataset(bc_file, bc_names)
BC_2 = Dataset(bc_fileXD, bc_namesXD)
AL = Dataset(al_file, al_names)
AL2 = Dataset(al_file2, al_names2)
LEC = Dataset(lec_file, lec_names)
BC_T = Dataset(bc_file_test, bc_names)
BC_T2 = Dataset(bc_file_test2, bc_names_2)
